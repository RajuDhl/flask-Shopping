import csv
import os

from tqdm import tqdm
import datetime
import psycopg2

from import_utils import float_me_replace, percentage, int_me_replace, build_date_cst

# filename = os.path.join(os.path.dirname(__file__), '20210116_repolog.csv')
filename = os.path.join(os.path.dirname(__file__), 'data/export-04262021.csv')
# filename = os.path.join(os.path.dirname(__file__), '../static/other/2020-09-22_Repo_Log.csv')
# establishing the connection
conn = psycopg2.connect(
    database="repolog", user='repouser', password='s3cret', host='127.0.0.1', port='5432'
)


def sql_insert(row):
    cursor = conn.cursor()
    keys = row.keys()
    columns = ','.join(keys)
    values = ','.join(['%({})s'.format(k) for k in keys])
    insert = 'insert into repos ({0}) values ({1})'.format(columns, values)
    query = cursor.mogrify(insert, row)
    cursor.execute(query)
    conn.commit()
    # print(f'second ---> {cursor.mogrify(insert, row)}')


with open(filename, 'r+', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    headers = [h.replace('/', '')
                   .replace('%', '')
                   .replace('?', '')
                   .replace('(', '')
                   .replace(')', '')
                   .replace('#', '').strip()
                   .replace(' ', '_').lower()
               for h in next(reader)]
    headers[headers.index('reason__comments')] = 'reason'
    # print(headers)

    d = csv.DictReader(f, fieldnames=headers)
    counter = 0
    rows = [dict(row) for row in d]
    for row in tqdm(rows):
        row['loan'] = float_me_replace(row['loan'])
        try:
            row['account_number'] = int_me_replace(str(row['loan']).split('.')[1])
        except:
            row['account_number'] = 1
        if row['loan'] == 3115.9:
            continue
        row['year'] = int_me_replace(row['year'])
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
        row['customer_name'] = row['name']
        row['vin'] = row['vin'].strip()
        prices = [row['awv'], row['mmr'], row['cash_price']]

        if 'proforma_nrv' in row:
            row['pforma_nrv'] = float_me_replace(row['proforma_nrv'])
        if 'proforma_difference' in row:
            row['pforma_diff'] = float_me_replace(row['proforma_difference'])
        if 'repo_allow2_hist' in row:
            row['repo_allow2_hist'] = float_me_replace(row['proforma_difference'])
        if 'proforma_gl' in row:
            row['proforma_gl'] = float_me_replace(row['proforma_gl'])
        if 'min_val' in row and row['min_val'] != '':
            row['min_val'] = float_me_replace(row['min_val'])
        else:
            row['min_val'] = 0.0
        if 'gain_loss' in row:
            row['gain_loss'] = float_me_replace(row['gain_loss'])
        if 'diff' in row:
            row['diff'] = float_me_replace(row['diff'])

        try:
            row['acct_min_val'] = min(i for i in prices if i is not None)
        except ValueError:
            row['acct_min_val'] = None
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
                row['acct_sold_month'] = row['date_sold'].strftime('%b-%y')
            except (TypeError, AttributeError):
                row['acct_sold_month'] = None
        try:
            row['acct_repo_month'] = row['gaap_date'].strftime('%b-%y')
        except (TypeError, AttributeError):
            row['acct_repo_month'] = None
        try:
            if row['loan'] not in (3155.9, '3155.9'):
                # r = db.collection('repos').document(f"{row['loan']}")
                # r.set(row)
                # if counter == 2:
                # print(f'the row --> {row}')
                row.pop('repo_month')
                row.pop('proforma_nrv')
                row.pop('proforma_difference')

                sql_insert(row)
                counter += 1
        except Exception as e:
            print(type(e), e, row['loan'])
