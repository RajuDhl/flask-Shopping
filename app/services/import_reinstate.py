# this is a standalone utility for uploading a current repo log to Firestore.
# file is not executed by app itself but used for development purposes

import pandas as pd
import os
import datetime
import psycopg2
from tqdm import tqdm

from import_utils import int_me_replace, build_date_cst, float_me_replace

conn = psycopg2.connect(
    database="repolog", user='repouser', password='s3cret', host='127.0.0.1', port='5432'
)

# filename = 'NewExtensionLog.csv'
filename = os.path.join(os.path.dirname(__file__), 'data/Reinstate.csv')


def sql_insert(row):
    cursor = conn.cursor()
    keys = row.keys()
    columns = ','.join(keys)
    values = ','.join(['%({})s'.format(k) for k in keys])
    insert = 'insert into repos ({0}) values ({1})'.format(columns, values)
    query = cursor.mogrify(insert, row)
    # print(f"the query {query}")
    cursor.execute(query)
    cursor.close()
    conn.commit()


# with open(filename, 'r+', encoding='utf-8-sig') as f:
#     reader = csv.reader(f)
#     # headers[headers.index('reason__comments')] = 'reason'
#     # print(headers)
#     d = csv.DictReader(f)
#     counter = 0
#     rows = [dict(row) for row in d]
#     for row in tqdm(rows):
#         try:
#             row.pop("")
#         except:
#             pass
#         # row['customer_number'] = int_me_replace(row['CUST_NUMBER'])
#         # row.pop('CUST_NUMBER')
#         # row['account_number'] = int_me_replace(row['ACCOUNT_NUMBER'])
#         # row.pop('ACCOUNT_NUMBER')
#         # row['requested_date'] = build_date_cst(row['RequestedDate'])
#         # row.pop('RequestedDate')
#         # row['final_status'] = (row['FinalStatus'])
#         # row.pop('FinalStatus')
#         # row['approved_date'] = build_date_cst(row['ApprovedDate'])
#         # row.pop('ApprovedDate')
#         # row['approved_by'] = (row['ApprovedBy'])
#         # row.pop('ApprovedBy')
#         # row["extension_type"] = (row['ExtensionType'])
#         # row.pop('ExtensionType')
#         # row["collector"] = row["Collector"]
#         # row.pop('Collector')
#         # row["prior_due_date"] = build_date_cst(row["PriorDueDate"])
#         # row.pop('PriorDueDate')
#         # row["new_due_date"] = build_date_cst(row["NewDueDate"])
#         # row.pop('NewDueDate')
#         # row["prior_maturity_date"] = build_date_cst(row["PriorMaturityDate"])
#         # row.pop('PriorMaturityDate')
#         # row["new_maturity_date"] = build_date_cst(row["NewMaturityDate"])
#         # row.pop('NewMaturityDate')
#
#
#         # del row['']
#
#         try:
#             # r = db.collection('extension').document(f"{row['CUST_NUMBER']}")
#             # r.set(row)
#             sql_insert(row)
#             counter += 1
#         except Exception as e:
#             print(type(e), e)

df = pd.read_csv('./data/Reinstate.csv', index_col=None, header=0)
df = df.drop(columns=['Column1'])

col_names = ['loan', 'dealer', 'name', 'year', 'make', 'model', 'vin', 'gaap_date', 'noi_sent', 'dafs',
             'balance_repo_date', 'date_reinstated']

d = {}
for thing in df.columns:
    print(df.head(2))
    i = df.columns.get_loc(thing)
    d[df.columns[i]] = col_names[i]
    print(f'd[{df.columns[i]}] = {col_names[i]}')
df = df.rename(columns=d)

counter = 0
for row in df.itertuples():
    x = {'loan': float_me_replace(row.loan), 'status': 'Reinstate', 'dealer': row.dealer, 'customer_name': row.name,
         'year': int_me_replace(row.year), 'make': row.make, 'model': row.model, 'vin': row.vin,
         'gaap_date': build_date_cst(row.gaap_date), 'noi_sent': build_date_cst(row.noi_sent),
         'dafs': build_date_cst(row.dafs), 'balance_repo_date': float_me_replace(row.balance_repo_date),
         'date_reinstate': build_date_cst(row.date_reinstated)}
    print(x)
    # r = db.collection('repos').document(f"{x['loan']}")
    # r.set(x)
    sql_insert(x)
    counter += 1
print(f"counter: {counter}")
