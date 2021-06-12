import csv
import os
from tqdm import tqdm
import datetime
from app import db
from app.models import Repos, TitleFollowUp, PifLog, ExtensionLog

from app.services.import_utils import float_me_replace, int_me_replace, build_date_cst, percentage


def import_repo_csv():
    repo_filename = os.path.join(os.path.dirname(__file__), 'data/2021-05-13_Repo_Log.csv')
    start_time = datetime.datetime.now().replace(microsecond=0)
    with open(repo_filename, 'r+', encoding='latin-1') as file:
        reader = csv.reader(file)
        headers = [h.replace('/', '')
                       .replace('%', '')
                       .replace('?', '')
                       .replace('(', '')
                       .replace(')', '')
                       .replace('#', '').strip()
                       .replace(' ', '_').lower()
                   for h in next(reader)]
        headers[headers.index('reason__comments')] = 'reason'
        print(f'the headers --> \n {headers}')

        d = csv.DictReader(file, fieldnames=headers)
        rows = [dict(row) for row in d]
        for row in tqdm(rows):
            # row['loan'] = row['loan']
            print(f"the loan {row['loan']}")
            row['year'] = int_me_replace(row['year'])
            prices = [row['awv'].strip(), row['mmr'].strip(), row['cash_price'].strip()]
            try:
                row['acct_min_val'] = int_me_replace(min(i for i in prices if i is not None))
            except ValueError:
                row['acct_min_val'] = None
            print(f"the acct min val {row['acct_min_val']} , status {row['status']}, prices {prices}")
            if row['status'] in ('Sold', 'OCO'):
                try:
                    row['acct_gain_loss'] = row['actual_proceeds'] - row['acct_min_val']
                except TypeError:
                    row['acct_gain_loss'] = None
                try:
                    row['acct_diff'] = float(row['acct_gain_loss'] / row['acct_min_val'])
                except TypeError:
                    row['acct_diff'] = None
                try:
                    row['acct_sold_month'] = build_date_cst(row['date_sold']).strftime('%b-%y')
                except (TypeError, AttributeError):
                    row['acct_sold_month'] = None
            row['year'] = int_me_replace(row['year'])
            row['make'] = row['make'].strip()
            row['model'] = row['model'].strip()
            row['vin'] = row['vin'].strip()
            row['gaap_date'] = build_date_cst(row['gaap_date'])
            row['noi_sent'] = build_date_cst(row['noi_sent'])
            row['dafs'] = build_date_cst(row['dafs'])
            row['date_sold'] = build_date_cst(row['date_sold'])
            row['co_date'] = build_date_cst(row['co_date'])
            if row['gaap_date']:
                g = datetime.datetime.timestamp(datetime.datetime.now()) - datetime.datetime.timestamp(row['gaap_date'])
                row['months_in_inventory'] = round(((g / 86400) / 30), 1)
            else:
                print(f"no gaap_date for {row['loan']}")
            row['location'] = row['location'].strip()
            row['sold_to'] = row['sold_to'].strip()
            row['mileage'] = int_me_replace(row['mileage'])
            row['cr_grade'] = float_me_replace(row['cr_grade'])
            row['chargeable_damages'] = float_me_replace(row['chargeable_damages']) or 0
            row['balance_repo_date'] = float_me_replace(row['balance_repo_date'])
            row['awv'] = float_me_replace(row['awv'])
            row['mmr'] = float_me_replace(row['mmr'])
            row['cash_price'] = float_me_replace(row['cash_price'])
            row['estimated_recovery'] = percentage(row['estimated_recovery'])
            row['current_mo_proceeds_estimate'] = float_me_replace(row['current_mo_proceeds_estimate'])
            row['eom_gaap_proceeds_estimate'] = float_me_replace(row['eom_gaap_proceeds_estimate'])
            row['actual_proceeds'] = float_me_replace(row['actual_proceeds'])
            row['back_end_product_cancellation'] = float_me_replace(row['back_end_product_cancellation']) or 0
            row['insurance_claims'] = float_me_replace(row['insurance_claims']) or 0
            if 'gross_co_amt' in row and row['gross_co_amt'] != '':
                # print(f'gross -> {row["gross_co_amt"]}')
                row['gross_co_amt'] = round(float_me_replace(row['gross_co_amt']), 2)
            else:
                row['gross_co_amt'] = 0.0
            row['unearned_discount'] = float_me_replace(row['unearned_discount']) or 0
            row['net_loss_or_gain'] = float_me_replace(row['net_loss_or_gain'])
            row['recovery'] = float_me_replace(row['recovery'])
            row['rem_bal'] = float_me_replace(row['rem_bal'])
            if 'true_up_amount' in row:
                row['true_up_amount'] = float_me_replace(row['true_up_amount'])
            row['cash_or_new_ac'] = row['cash_or_new_ac'].strip()
            row['reason'] = row['reason'].strip()
            row['exception'] = row['exception'].strip()
            row['exception_detail'] = row['exception_detail'].strip()
            row['notes'] = row['notes'].strip()
            row['true_up_transaction'] = row['true_up_transaction'].strip()
            row['same_month_sale'] = row['same_month_sale'].strip()
            if 'true_up_amount' in row:
                row['true_up_amount'] = float_me_replace(row['true_up_amount'])

            repo = Repos.query.filter_by(loan=row['loan']).first()
            if repo:
                print(f"updating loan ==> {row['loan']}")  # acct_sold_mth ==> {row['acct_sold_month']}")
                db.session.query(Repos).filter_by(loan=row['loan']).update(row)
            else:
                print(f"add new loan ==> {row['loan']}")
                new_repo = Repos(**row)
                db.session.add(new_repo)
        db.session.commit()
        end_time = datetime.datetime.now().replace(microsecond=0)
        print(f' Total execution time {end_time - start_time}')


def import_title_log_csv():
    repo_filename = os.path.join(os.path.dirname(__file__), 'data/5.17.21_Title_log.csv')
    start_time = datetime.datetime.now().replace(microsecond=0)
    with open(repo_filename, 'r+', encoding='latin-1') as file:
        reader = csv.reader(file)
        headers = [
            h.replace('/', '').replace('%', '').replace('?', '').replace('-', '').replace('&', '').replace('#',
                                                                                                           '').strip().replace(
                ' ', '_').lower()
            for h in next(reader)]
        # headers[headers.index('reason__comments')] = 'reason'
        print(headers)
        d = csv.DictReader(file, fieldnames=headers)
        rows = [dict(row) for row in d]
        for row in tqdm(rows):
            # try:
            #     if not row["account"]:
            #         row["account"] = ""
            #     else:
            #         row["account"] = int(row["account"])
            # except:
            #     pass
            row['customer_number'] = int_me_replace(row['account'])
            row["account"] = (1)
            row["dealer"] = row["dealer"]
            row['name'] = row['name']
            row["app_received"] = build_date_cst(row["app_received"])
            if row["app_received"] is None:
                row["app_received"] = None
            row['contract_date'] = build_date_cst(row['contract_date'])
            row['title_due'] = build_date_cst(row['title_due'])
            row['white_slip_received'] = build_date_cst(row['white_slip_received'].split(" ")[0])
            row['title_received'] = build_date_cst(row['title_received'].split(" ")[0])
            row["follow_up_comments"] = row['follow_up_comments'] if row['follow_up_comments'] else ""

            title = TitleFollowUp.query.filter_by(customer_number=row['customer_number']).first()
            if title:
                print(f"updating title ==> {row['customer_number']}")
                db.session.query(TitleFollowUp).filter_by(customer_number=row['customer_number']).update(row)
            else:
                print(f"add new title followup customer_number ==> {row['customer_number']}")
                new_title = TitleFollowUp(**row)
                db.session.add(new_title)

        db.session.commit()
        end_time = datetime.datetime.now().replace(microsecond=0)
        print(f' Total execution time for title followup {end_time - start_time}')


def import_ext_log_csv():
    ext_filename = os.path.join(os.path.dirname(__file__), 'data/Extension_Log5.17.21.csv')
    start_time = datetime.datetime.now().replace(microsecond=0)
    with open(ext_filename, 'r+', encoding='latin-1') as file:
        reader = csv.reader(file)
        d = csv.DictReader(file)
        rows = [dict(row) for row in d]
        for ext_obj in tqdm(rows):
            # ext_obj = row
            row = {'customer_number': int_me_replace(ext_obj['CUST_NUMBER']),
                   'account_number': int_me_replace(ext_obj['ACCOUNT_NUMBER']),
                   'requested_date': build_date_cst(ext_obj['RequestedDate']),
                   'final_status': (ext_obj['FinalStatus']),
                   'approved_date': build_date_cst(ext_obj['ApprovedDate']),
                   'approved_by': (ext_obj['ApprovedBy']),
                   "extension_type": (ext_obj['ExtensionType']),
                   "collector": ext_obj["Collector"],
                   "prior_due_date": build_date_cst(ext_obj["PriorDueDate"]),
                   "new_due_date": build_date_cst(ext_obj["NewDueDate"]),
                   "prior_maturity_date": build_date_cst(ext_obj["PriorMaturityDate"]),
                   "new_maturity_date": build_date_cst(ext_obj["NewMaturityDate"])}
            # row['customer_number'] = int_me_replace(ext_obj['CUST_NUMBER'])

            ext = ExtensionLog.query.filter_by(customer_number=row['customer_number']).first()
            if ext:
                print(f"updating ext ==> {row['customer_number']}")
                db.session.query(ExtensionLog).filter_by(customer_number=row['customer_number']).update(row)
            else:
                print(f"add new title followup customer_number ==> {row['customer_number']}")
                new_ext = ExtensionLog(**row)
                db.session.add(new_ext)
        db.session.commit()
        end_time = datetime.datetime.now().replace(microsecond=0)
        print(f' Total execution time for extension log {end_time - start_time}')


def import_pif_log_csv():
    pif_filename = os.path.join(os.path.dirname(__file__), 'data/PIF_Log_05-17-2021.csv')
    start_time = datetime.datetime.now().replace(microsecond=0)
    with open(pif_filename, 'r+', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        headers = [h.replace('/', '')
                    .replace('%', '')
                    .replace('?', '')
                    .replace('$', '')
                    .replace('#', '').strip().replace(' ', '_').lower()
                   for h in next(reader)]
        print(f'the headers {headers}')
        d = csv.DictReader(f, fieldnames=headers)
        rows = [dict(row) for row in d]
        print(rows[0])
        for row in tqdm(rows):
            row['customer_number'] = (row['acct'].split('-')[0]).strip()
            row.pop('acct')
            row.pop('back-end_products_financed')
            row['name'] = row['name'].strip()
            row['date_pif'] = build_date_cst(row['date_pif'])
            row['status'] = (row['status'])
            row['op'] = row['op'].strip()
            row['method'] = row['method'].strip()
            row["op_sent"] = build_date_cst(row['op_sent'].split(' ')[0])
            row["gap_or_warr_cancelation_required"] = row["gap_or_warr_cancelation_required"]
            row["date_canceled"] = build_date_cst(row["date_canceled"].split(' ')[0])
            row["ttl_cntrct_recd"] = build_date_cst(row["ttl-cntrct_recd"].split(' ')[0])
            row.pop('ttl-cntrct_recd')
            row["ttl_cntrct_sent"] = build_date_cst(row["ttl-cntrct_sent"].split(' ')[0])
            row.pop('ttl-cntrct_sent')
            row["comments"] = (row["comments"])

            pif = PifLog.query.filter_by(customer_number=row['customer_number']).first()
            if pif:
                print(f"updating pif ==> {row['customer_number']}")
                db.session.query(PifLog).filter_by(customer_number=row['customer_number']).update(row)
            else:
                print(f"add new pif log customer_number ==> {row['customer_number']}")
                new_pif = PifLog(**row)
                db.session.add(new_pif)

        db.session.commit()
        end_time = datetime.datetime.now().replace(microsecond=0)
        print(f' Total execution time for title followup {end_time - start_time}')


