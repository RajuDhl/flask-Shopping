import json
import os
import psycopg2
from datetime import datetime

from psycopg2.extras import DictCursor

# from import_utils import int_me_replace, float_me_replace, percentage
from app.services.import_utils import int_me_replace, float_me_replace, percentage

filename = os.path.join(os.path.dirname(__file__), 'data/repolog.json')
json_data = open(filename).read()
json_obj = json.loads(json_data)


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


# do validation and checks before insert
def validate_string(val):
    if val is not None:
        if type(val) is int:
            # for x in val:
            #   print(x)
            return str(val).encode('utf-8')
        else:
            return val


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
            # sql_insert(row)
            print("inserting")
        except Exception as e:
            print(type(e), e, row['loan'])
        if 'repo_category' in repo_obj and repo_obj['repo_category']:
            cat = repo_obj['repo_category']
            for c in cat:
                cursor = conn.cursor(cursor_factory=DictCursor)
                query = f"select id from repos where loan = '{str(repo_obj['loan'])}'"
                cursor.execute(query)
                for row in cursor.fetchall():
                    print(f"the row ---> {row['id']} the c ---> {c}")
                    insert = f"insert into category (category_name, repo_id) values ('{c}' , {row['id']})"
                    cursor.execute(insert)
                    # conn.commit()


if __name__ == '__main__':
    print(f'main file called')
    read_json()
