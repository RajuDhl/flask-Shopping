# this is a standalone utility for uploading a current repo log to Firestore.
# file is not executed by app itself but used for development purposes

import csv
import os
from tqdm import tqdm
import datetime
import psycopg2
from import_repo import float_me_replace, build_date_cst, percentage
# establishing the connection

conn = psycopg2.connect(
    database="repolog", user='repouser', password='s3cret', host='127.0.0.1', port='5432'
)
# filename = 'pif.csv'
filename = os.path.join(os.path.dirname(__file__), 'data/pif.csv')


def sql_insert(row):
    cursor = conn.cursor()
    keys = row.keys()
    columns = ','.join(keys)
    values = ','.join(['%({})s'.format(k) for k in keys])
    insert = 'insert into pif_log ({0}) values ({1})'.format(columns, values)
    query = cursor.mogrify(insert, row)
    # print(f"the query {query}")
    cursor.execute(query)
    cursor.close()
    conn.commit()


with open(filename, 'r+', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    headers = [h.replace('/', '')
                .replace('%', '')
                .replace('?', '')
                .replace('$', '')
                .replace('#', '').strip().replace(' ', '_').lower()
               for h in next(reader)]
    print(headers)
    d = csv.DictReader(f, fieldnames=headers)
    counter = 0
    rows = [dict(row) for row in d]
    print(rows[0])
    for row in tqdm(rows):
        # import pdb;pdb.set_trace()
        try:
            row.pop("")
        except:
            pass
        row['customer_number'] = float_me_replace((row['customer_number'].split('-')[0]))
        row["account_number"] = (1)
        row['name'] = row['name']
        row['date_pif'] = build_date_cst(row['date_pif'])
        row['status'] = (row['status'])
        row['op'] = row['op']
        row['method'] = (row['method'])
        row["op_sent"] = build_date_cst(row['op_sent'].split(' ')[0])
        row["gap_or_warr_cancelation_required"] = row["gap_or_warr_cancelation_required"]
        row["date_canceled"] = build_date_cst(row["date_canceled"].split(' ')[0])
        row["ttl_cntrct_recd"] = build_date_cst(row["ttl_cntrct_recd"].split(' ')[0])
        row["ttl_cntrct_sent"] = build_date_cst(row["ttl_cntrct_sent"].split(' ')[0])
        row["comments"] = (row["comments"])
        # del row['']
        try:
            # r = db.collection('pif_log').document(f"{row['customer_number']}")
            # r.set(row)
            sql_insert(row)
            counter += 1
        except Exception as e:
            print(type(e), e)
