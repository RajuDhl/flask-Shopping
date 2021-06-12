# this is a standalone utility for uploading a current repo log to Firestore.
# file is not executed by app itself but used for development purposes

import csv
import os
import datetime
import psycopg2
from tqdm import tqdm
from import_utils import int_me_replace, build_date_cst

conn = psycopg2.connect(
    database="repolog", user='repouser', password='s3cret', host='127.0.0.1', port='5432'
)

# filename = 'followup2.csv'
filename = os.path.join(os.path.dirname(__file__), 'data/followup2.csv')


def sql_insert(row):
    cursor = conn.cursor()
    keys = row.keys()
    columns = ','.join(keys)
    values = ','.join(['%({})s'.format(k) for k in keys])
    insert = 'insert into title_follow_up ({0}) values ({1})'.format(columns, values)
    query = cursor.mogrify(insert, row)
    # print(f"the query {query}")
    cursor.execute(query)
    cursor.close()
    conn.commit()


with open(filename, 'r+', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    headers = [h.replace('/', '').replace('%', '').replace('?', '').replace('#', '').strip().replace(' ', '_').lower()
               for h in next(reader)]
    # headers[headers.index('reason__comments')] = 'reason'
    # print(headers)
    d = csv.DictReader(f, fieldnames=headers)
    counter = 0
    rows = [dict(row) for row in d]
    for row in tqdm(rows):
        try:
            row.pop("")
            row.pop("d_maloney-code")
            row.pop("Unnamed: 9")
        except:
            pass
        try:
            if not row["account"]:
                row["account"] = ""
            else:
                row["account"] = int(row["account"])
        except:
            pass

        row['customer_number'] = int_me_replace(row['customer_number'])
        row["account"] = (1)
        row["dealer"] = row["dealer"]
        row['name'] = row['name']
        row["app_received"] = build_date_cst(row["app_received"])
        if row["app_received"] is None:
            row["app_received"] = ""
        row['contract_date'] = build_date_cst(row['contract_date'])
        row['title_due'] = build_date_cst(row['title_due'])
        row['white_slip_received'] = build_date_cst(row['white_slip_received'].split(" ")[0])
        row['title_received'] = build_date_cst(row['title_received'].split(" ")[0])
        row["follow_up_comments"] = (row['follow_up_comments'])
        try:
            # r = db.collection('Title_FollowUp').document(f"{row['customer_number']}")
            # r.set(row)
            sql_insert(row)
            counter += 1
        except Exception as e:
            print(type(e), e.__traceback__, row)

    conn.close()
