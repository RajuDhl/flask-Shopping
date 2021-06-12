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

# filename = 'NewExtensionLog.csv'
filename = os.path.join(os.path.dirname(__file__), 'data/NewExtensionLog.csv')


def sql_insert(row):
    cursor = conn.cursor()
    keys = row.keys()
    columns = ','.join(keys)
    values = ','.join(['%({})s'.format(k) for k in keys])
    insert = 'insert into extension ({0}) values ({1})'.format(columns, values)
    query = cursor.mogrify(insert, row)
    # print(f"the query {query}")
    cursor.execute(query)
    cursor.close()
    conn.commit()


with open(filename, 'r+', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    # headers[headers.index('reason__comments')] = 'reason'
    # print(headers)
    d = csv.DictReader(f)
    counter = 0
    rows = [dict(row) for row in d]
    for row in tqdm(rows):
        try:
            row.pop("")
        except:
            pass
        row['customer_number'] = int_me_replace(row['CUST_NUMBER'])
        row.pop('CUST_NUMBER')
        row['account_number'] = int_me_replace(row['ACCOUNT_NUMBER'])
        row.pop('ACCOUNT_NUMBER')
        row['requested_date'] = build_date_cst(row['RequestedDate'])
        row.pop('RequestedDate')
        row['final_status'] = (row['FinalStatus'])
        row.pop('FinalStatus')
        row['approved_date'] = build_date_cst(row['ApprovedDate'])
        row.pop('ApprovedDate')
        row['approved_by'] = (row['ApprovedBy'])
        row.pop('ApprovedBy')
        row["extension_type"] = (row['ExtensionType'])
        row.pop('ExtensionType')
        row["collector"] = row["Collector"]
        row.pop('Collector')
        row["prior_due_date"] = build_date_cst(row["PriorDueDate"])
        row.pop('PriorDueDate')
        row["new_due_date"] = build_date_cst(row["NewDueDate"])
        row.pop('NewDueDate')
        row["prior_maturity_date"] = build_date_cst(row["PriorMaturityDate"])
        row.pop('PriorMaturityDate')
        row["new_maturity_date"] = build_date_cst(row["NewMaturityDate"])
        row.pop('NewMaturityDate')

        # del row['']
        
        try:
            # r = db.collection('extension').document(f"{row['CUST_NUMBER']}")
            # r.set(row)
            sql_insert(row)
            counter += 1
        except Exception as e:
            print(type(e), e)
        




