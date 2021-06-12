import json
import os
from datetime import datetime
import uuid

from app import db
from app.models import Repos, Category, User, PifLog, TitleFollowUp, ExtensionLog, Role
from app.services.import_utils import int_me_replace, float_me_replace, percentage, build_date_cst
from app.services.nrv import add_repo_month, build_all_historical_tables, add_accounting_values
from app.services.utils import hash_password, make_month_list

filename = os.path.join(os.path.dirname(__file__), 'data/archive/repolog.json')
# filename = os.path.join(os.path.dirname(__file__), 'data/repo.json')
json_data = open(filename).read()
json_obj = json.loads(json_data)


# do validation and checks before insert
def validate_string(val):
    if val is not None:
        if type(val) is int:
            # for x in val:
            #   print(x)
            return str(val).encode('utf-8')
        else:
            return val


def load_default_user():
    """ Populates database with a default user """
    email = 'dev@samedayauto.net'
    user = User.query.filter_by(email=email).first()
    if user is None:
        name = 'dev'
        password = 'S3cret1'
        u = str(uuid.uuid1())
        user = User(email=email,
                    name=name,
                    password=hash_password(password),
                    uuid=f'{u}',
                    verified=True)
        role = Role.query.filter(Role.name == 'Admin').first()
        if not role:
            user.roles.append(Role(name='Admin'))
        else:
            user.roles.append(role)
        db.session.add(user)
        db.session.commit()
    else:
        print('dev user exists aborting')


# Create 'admin@example.com' user with 'Admin' and 'Agent' roles
def load_test_users():
    if not User.query.filter(User.email == 'admin@example.com').first():
        u = str(uuid.uuid1())
        user = User(
            email='admin@example.com',
            created=datetime.utcnow(),
            password=hash_password('Password1'),
            active=True,
            uuid=f'{u}',
            verified=True
        )
        role = Role.query.filter(Role.name == 'Admin').first()
        if not role:
            user.roles.append(Role(name='Admin'))
        else:
            user.roles.append(role)
        db.session.add(user)
        db.session.commit()

    if not User.query.filter(User.email == 'test@example.com').first():
        u = str(uuid.uuid1())
        user = User(
            email='test@example.com',
            created=datetime.utcnow(),
            password=hash_password('Password1'),
            active=True,
            uuid=f'{u}',
            verified=True
        )
        role = Role.query.filter(Role.name == 'Repo').first()
        if not role:
            user.roles.append(Role(name='Repo'))
        else:
            user.roles.append(role)
        db.session.add(user)
        db.session.commit()


def load_categories():
    """ Populates database with Category data """
    categories = [
        'Abandoned', 'Bankruptcy', 'Divorce / Family', 'Drugs / Jail',
        'Illness / Death', 'Impound', 'Insurance Deficiency', 'Job Loss / Income',
        'Mechanical', 'No Insurance / Stolen', 'No Insurance / Wreck', 'Skip',
        'Abandoned', 'Impound', 'Stolen', 'Insurance deficiency', 'Mechanic'
    ]

    for c in categories:
        print(f'c --> {c}')
        category = Category.query.filter_by(category_name=c).first()
        if category:
            print(f"category {category} exists")
            # db.session.query(Category).filter_by(category_name=c).update()
        else:
            new_category = Category(category_name=c)
            db.session.add(new_category)
            db.session.commit()

    # c0 = Category(category_name="Abandoned")
    # c1 = Category(category_name="Bankruptcy")
    # c2 = Category(category_name="Buyback")
    # c3 = Category(category_name="Dealer Default")
    # c4 = Category(category_name="Impound")
    # c5 = Category(category_name="Insurance Deficiency")
    # c6 = Category(category_name="Mechanics Lien")
    # c7 = Category(category_name="No Insurance")
    # c8 = Category(category_name="Settled Account")
    # c9 = Category(category_name="Stolen")
    # c10 = Category(category_name="Totaled")
    # c11 = Category(category_name="Wrecked")
    # c12 = Category(category_name="Skip")
    # db.session.add(c0)
    # db.session.add(c1)
    # db.session.add(c2)
    # db.session.add(c3)
    # db.session.add(c4)
    # db.session.add(c5)
    # db.session.add(c6)
    # db.session.add(c7)
    # db.session.add(c8)
    # db.session.add(c9)
    # db.session.add(c10)
    # db.session.add(c11)
    # db.session.add(c12)
    # db.session.commit()
    #
    # """ Load default roles """
    # r1 = Role(name='Repo', display_name='Repo Log')
    # r2 = Role(name='Extension', display_name='Extension Log')
    # r3 = Role(name='Title', display_name='Title Follow-Up')
    # r4 = Role(name='PIF Log', display_name='Pif Log')
    # db.session.add(r1)
    # db.session.add(r2)
    # db.session.add(r3)
    # db.session.add(r4)
    # db.session.commit()


def load_nrv():
    add_repo_month()
    month_list = make_month_list(start_year=2018)
    # add_accounting_values()
    build_all_historical_tables(months=month_list,
                                var_diff='acct_diff',
                                var_b='acct_min_val',
                                collection_name='real_disc_to_nrv',
                                neg=True)


def load_val_allow():
    from app.services.cloud.daily_update_2 import make_month_list, add_accounting_values, build_all_historical_tables
    month_list = make_month_list(start_year=2018)
    add_accounting_values()
    build_all_historical_tables(months=month_list,
                                var_diff='pforma_diff',
                                var_b='pforma_nrv',
                                collection_name='val_allow')


def read_json():
    print(f'total length -->  {len(json_obj)}')
    for i, item in enumerate(json_obj):
        # print(json_obj[item])
        repo_obj = json_obj[item]
        if repo_obj['gaap_date']:
            gaap_date = datetime.fromtimestamp(repo_obj['gaap_date']['value']['_seconds'])
        print(f"{repo_obj['loan']} --->  {gaap_date}")
        row = {'loan': repo_obj['loan']}
        row['account_number'] = 1
        row['year'] = int_me_replace(repo_obj['year'])
        row['gaap_date'] = gaap_date
        if repo_obj['noi_sent'] is not None:
            row['noi_sent'] = datetime.fromtimestamp(repo_obj['noi_sent']['value']['_seconds'])
        if repo_obj['dafs'] is not None:
            row['dafs'] = datetime.fromtimestamp(repo_obj['dafs']['value']['_seconds'])
        if repo_obj['date_sold'] is not None:
            row['date_sold'] = datetime.fromtimestamp(repo_obj['date_sold']['value']['_seconds'])
        if repo_obj['co_date'] is not None:
            row['co_date'] = datetime.fromtimestamp(repo_obj['co_date']['value']['_seconds'])
        row['months_in_inventory'] = repo_obj['months_in_inventory']
        row['mileage'] = int_me_replace(repo_obj['mileage'])
        row['cr_grade'] = repo_obj['cr_grade']
        row['chargeable_damages'] = repo_obj['chargeable_damages'] or 0
        row['balance_repo_date'] = float_me_replace(repo_obj['balance_repo_date'])
        row['awv'] = float_me_replace(repo_obj['awv'])
        row['mmr'] = float_me_replace(repo_obj['mmr'])
        row['cash_price'] = float_me_replace(repo_obj['cash_price'])
        row['estimated_recovery'] = percentage(repo_obj['estimated_recovery'])
        row['current_mo_proceeds_estimate'] = float_me_replace(repo_obj['current_mo_proceeds_estimate'])
        row['eom_gaap_proceeds_estimate'] = float_me_replace(repo_obj['eom_gaap_proceeds_estimate'])
        row['actual_proceeds'] = float_me_replace(repo_obj['actual_proceeds'])
        if 'back_end_product_cancellations' in repo_obj:
            row['back_end_product_cancellation'] = float_me_replace(repo_obj['back_end_product_cancellations']) or 0
        row['insurance_claims'] = float_me_replace(repo_obj['insurance_claims']) or 0
        if 'gross_co_amt' in repo_obj and repo_obj['gross_co_amt'] != '':
            row['gross_co_amt'] = repo_obj['gross_co_amt']
        else:
            row['gross_co_amt'] = 0.0
        row['unearned_discount'] = float_me_replace(repo_obj['unearned_discount']) or 0
        row['net_loss_or_gain'] = float_me_replace(repo_obj['net_loss_or_gain'])
        if 'recovery' in repo_obj:
            row['recovery'] = int_me_replace(repo_obj['recovery'])
        if 'rem_bal' in repo_obj:
            row['rem_bal'] = float_me_replace(repo_obj['rem_bal'])
        if 'true_up_amount' in repo_obj:
            row['true_up_amount'] = float_me_replace(repo_obj['true_up_amount'])
        row['customer_name'] = repo_obj['customer_name']
        if 'name' in repo_obj and repo_obj['name'] and repo_obj['name'] != '':
            row['name'] = repo_obj['name']
        row['dealer'] = repo_obj['dealer']
        row['status'] = repo_obj['status']
        row['location'] = repo_obj['location']
        row['sold_to'] = repo_obj['sold_to']
        if 'trim' in repo_obj:
            row['trim'] = repo_obj['trim']
        if 'last_editor' in repo_obj:
            row['last_editor'] = repo_obj['last_editor']
        row['reason'] = repo_obj['reason']
        row['notes'] = repo_obj['notes']
        row['make'] = repo_obj['make']
        row['model'] = repo_obj['model']
        if repo_obj['date_sold']:
            row['date_sold'] = datetime.fromtimestamp(repo_obj['date_sold']['value']['_seconds'])
        if 'date_reinstate' in repo_obj and repo_obj['date_reinstate'] != None:
            row['date_reinstate'] = datetime.fromtimestamp(repo_obj['date_reinstate']['value']['_seconds'])
        if 'acct_gain_loss' in repo_obj:
            row['acct_gain_loss'] = repo_obj['acct_gain_loss']
        if 'acct_min_val' in repo_obj:
            row['acct_min_val'] = repo_obj['acct_min_val']
        if 'actual_proceeds' in repo_obj:
            row['actual_proceeds'] = repo_obj['actual_proceeds']
        if 'acct_diff' in repo_obj:
            row['acct_diff'] = repo_obj['acct_diff']
        if 'acct_sold_month' in repo_obj:
            row['acct_sold_month'] = repo_obj['acct_sold_month']
        if 'acct_repo_month' in repo_obj:
            row['acct_repo_month'] = repo_obj['acct_repo_month']

        row['vin'] = repo_obj['vin']

        if 'proforma_nrv' in repo_obj:
            row['pforma_nrv'] = float_me_replace(repo_obj['proforma_nrv'])
        if 'proforma_difference' in repo_obj:
            row['pforma_diff'] = float_me_replace(repo_obj['proforma_difference'])
        if 'repo_allow2_hist' in repo_obj:
            row['repo_allow2_hist'] = float_me_replace(repo_obj['repo_allow2_hist'])
        if 'proforma_gl' in repo_obj:
            row['proforma_gl'] = float_me_replace(repo_obj['proforma_gl'])
        if 'min_val' in row and row['min_val'] != '':
            row['min_val'] = float_me_replace(repo_obj['min_val'])
        else:
            row['min_val'] = 0.0
        if 'gain_loss' in repo_obj:
            row['gain_loss'] = float_me_replace(repo_obj['gain_loss'])
        if 'diff' in repo_obj:
            row['diff'] = float_me_replace(repo_obj['diff'])
        # row['repo_category'] = 'Skip'

        try:
            repo = Repos(**row)
            db.session.add(repo)
            print("inserting new repo")
        except Exception as e:
            print(type(e), e, row['loan'])
        if 'repo_category' in repo_obj and repo_obj['repo_category']:
            cat = repo_obj['repo_category']
            for c in cat:
                category = Category.query.filter_by(category_name=c).first()
                repo.categories.append(category)

        db.session.commit()


def import_pif_json():
    print('starting pif import')
    pif_file = os.path.join(os.path.dirname(__file__), 'data/piflog.json')
    pif_json_data = open(pif_file).read()
    pif_json_obj = json.loads(pif_json_data)
    print(f'Total pif length --> {len(pif_json_obj)}')
    for i, item in enumerate(pif_json_obj):
        pif_obj = pif_json_obj[item]
        row = {'customer_number': pif_obj['customer_number']}
        row["account_number"] = 1
        row['name'] = pif_obj['name']
        if pif_obj['date_pif'] is not None:
            row['date_pif'] = datetime.fromtimestamp(pif_obj['date_pif']['value']['_seconds'])
        row['status'] = (pif_obj['status'])
        row['op'] = pif_obj['op']
        row['method'] = (pif_obj['method'])
        if pif_obj['op_sent'] is not None:
            row['op_sent'] = datetime.fromtimestamp(pif_obj['op_sent']['value']['_seconds'])
        row["gap_or_warr_cancelation_required"] = pif_obj["gap_or_warr_cancelation_required"]
        if pif_obj['date_canceled'] is not None:
            row['date_canceled'] = datetime.fromtimestamp(pif_obj['date_canceled']['value']['_seconds'])
        if pif_obj['ttl-cntrct_recd'] is not None:
            row['ttl_cntrct_recd'] = datetime.fromtimestamp(pif_obj['ttl-cntrct_recd']['value']['_seconds'])
        if pif_obj['ttl-cntrct_sent'] is not None:
            row['ttl_cntrct_sent'] = datetime.fromtimestamp(pif_obj['ttl-cntrct_sent']['value']['_seconds'])
        row["comments"] = (pif_obj["comments"])
        print(f'pif --> {row}')

        try:
            pif = PifLog(**row)
            db.session.add(pif)
            print(f"Inserting new pif {pif_obj['customer_number']}")
        except Exception as e:
            print(type(e), e, pif_obj['customer_number'])

        db.session.commit()


def import_tf_json():
    print('starting tf import')
    tf_file = os.path.join(os.path.dirname(__file__), 'data/titlefollowup.json')
    tf_json_data = open(tf_file).read()
    tf_json_obj = json.loads(tf_json_data)
    print(f'Total pif length --> {len(tf_json_obj)}')

    for i, item in enumerate(tf_json_obj):
        tf_obj = tf_json_obj[item]
        print(f"start processing title follow up =======>  {tf_obj['customer_number']}")
        row = {
            'customer_number': tf_obj['customer_number'],
            "account": 1,
            "dealer": tf_obj['dealer'],
            "name": tf_obj['name'],
            "follow_up_comments": tf_obj['follow-up_comments']
        }
        if tf_obj['app_received'] is not None and tf_obj['app_received'] != '':
            row['app_received'] = datetime.fromtimestamp(tf_obj['app_received']['value']['_seconds'])
        if tf_obj['contract_date'] is not None:
            row['contract_date'] = datetime.fromtimestamp(tf_obj['contract_date']['value']['_seconds'])
        if tf_obj['title_due'] is not None:
            row['title_due'] = datetime.fromtimestamp(tf_obj['title_due']['value']['_seconds'])
        if tf_obj['white_slip_received'] is not None:
            row['white_slip_received'] = datetime.fromtimestamp(tf_obj['white_slip_received']['value']['_seconds'])
        if tf_obj['title_received'] is not None:
            row['title_received'] = datetime.fromtimestamp(tf_obj['title_received']['value']['_seconds'])
        try:
            tf = TitleFollowUp(**row)
            db.session.add(tf)
            print(f"Inserting new tf {tf_obj['customer_number']}")
        except Exception as e:
            print(type(e), e, tf_obj['customer_number'])
        db.session.commit()


def import_ext_json():
    print('starting ext import')
    ext_file = os.path.join(os.path.dirname(__file__), 'data/extension.json')
    ext_json_data = open(ext_file).read()
    ext_json_obj = json.loads(ext_json_data)
    print(f'Total pif length --> {len(ext_json_obj)}')
    for i, item in enumerate(ext_json_obj):
        ext_obj = ext_json_obj[item]
        print(f"start processing ext =======>  {ext_obj['CUST_NUMBER']}")
        row = {
            'customer_number': ext_obj['CUST_NUMBER'],
            "account_number": 1,
            "extension_type": ext_obj['ExtensionType'],
            "approved_by": ext_obj['ApprovedBy'],
            "collector": ext_obj['Collector'],
            "final_status": ext_obj['FinalStatus']
        }

        if 'last_editor' in ext_obj and ext_obj['last_editor'] is not None:
            row['last_editor'] = ext_obj['last_editor']
        if 'last_update' in ext_obj and ext_obj['last_update'] is not None:
            row['last_update'] = datetime.fromtimestamp(ext_obj['last_update']['value']['_seconds'])
        if ext_obj['RequestedDate'] is not None:
            row['requested_date'] = datetime.fromtimestamp(ext_obj['RequestedDate']['value']['_seconds'])
        if ext_obj['ApprovedDate'] is not None:
            row['approved_date'] = datetime.fromtimestamp(ext_obj['ApprovedDate']['value']['_seconds'])
        if ext_obj['PriorDueDate'] is not None:
            row['prior_due_date'] = datetime.fromtimestamp(ext_obj['PriorDueDate']['value']['_seconds'])
        if ext_obj['NewDueDate'] is not None:
            row['new_due_date'] = datetime.fromtimestamp(ext_obj['NewDueDate']['value']['_seconds'])
        if ext_obj['PriorMaturityDate'] is not None:
            row['prior_maturity_date'] = datetime.fromtimestamp(ext_obj['PriorMaturityDate']['value']['_seconds'])
        if ext_obj['NewMaturityDate'] is not None:
            row['new_maturity_date'] = datetime.fromtimestamp(ext_obj['NewMaturityDate']['value']['_seconds'])

        try:
            ext = ExtensionLog(**row)
            db.session.add(ext)
            print(f"Inserting new ext {ext_obj['CUST_NUMBER']}")
        except Exception as e:
            print(type(e), e, ext_obj['CUST_NUMBER'])

        db.session.commit()


if __name__ == '__main__':
    print(f'main file called')
