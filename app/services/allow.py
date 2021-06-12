from __future__ import print_function
import os
import pytz
import datetime
from dateutil.relativedelta import relativedelta
import logging
import sys

# google_init()
# db = firestore.Client()
# from .models import Repos
from app.services.utils import make_month_list
from app.models import Repos


def build_all_historical_tables(months, var_diff, var_b, collection_name, neg=False):
    """
    Builds real_disc_allow2 table. Will be calcs
    for 1 / 1 / start_year
    :param start_year: int the year to start
    :return: Firestore collection built
    """
    last_month = datetime.datetime.now(pytz.timezone('US/Central')).date() + relativedelta(months=-1)
    m = months.index(last_month.strftime('%b-%y'))
    print(f"m: {m}")
    # import pdb;pdb.set_trace()
    for x in range(1, m):
        print([months[x], months[x + 1], months[x + 2]])
        x_months = months[x]
        try:
            # repo_ref = db.collection('repos')
            # query = repo_ref.where('status', '==', 'Sold').where('acct_sold_month', 'in',
            # [months[x], months[x + 1], months[x + 2]])
            query = Repos.query.filter(Repos.acct_repo_month <= x_months).filter(Repos.status == 'Sold')
            # .filter(Repos.acct_repo_month <= f'{months[x + 1]}') \
            # .filter(Repos.acct_repo_month <= f'{months[x + 2]}') \

            print(f'query {query}')
            diff = []
            b = []
            counter = len([d for d in query])
            i = 1
            for doc in query:
                if i == 1:
                    print(f'doc {doc.to_dict()}')
                    i = i+1
                try:
                    # print(f"trying 1 {doc.to_dict()[var_diff]}")
                    # diff.append((doc.to_dict()[var_diff] is None) ? 0.0 : doc.to_dict()[var_diff])
                    if doc.to_dict()[var_diff] is None:
                        diff.append(0.0)
                    else:
                        diff.append(doc.to_dict()[var_diff])

                    if doc.to_dict()[var_b] is None:
                        b.append(0.0)
                    else:
                        b.append(doc.to_dict()[var_b])

                except KeyError as e:
                    print(
                        f'build_all_historical_tables - KeyError: {e} loan: {doc.to_dict()["loan"]}, {doc.to_dict()["status"]} {months[x + 2]}')
                except TypeError as e:
                    print(
                        f'build_all_historical_tables - TypeError: {e} loan: {doc.to_dict()["loan"]}, {doc.to_dict()["status"]} {months[x + 2]}')
                # except KeyError as e:
                #     print("except 1")
                #     c = doc.to_dict()
                #     c['pforma_diff'] = 0.0
                #     # print(doc.to_dict())
                #     diff.append(c[var_diff])
                #     print(f'build_all_historical_tables - KeyError: {e} loan: {doc.to_dict()["loan"]}')
                    # {doc.to_dict()["status"]} {months[x+2]}')
                # except TypeError as e: print(f'build_all_historical_tables - TypeError: {e} loan: {doc.to_dict()[
                # "loan"]}, {doc.to_dict()["status"]} {months[x+2]}')
                # try:
                #     b.append(doc.to_dict()[var_b])
                # except:
                #     v = doc.to_dict()
                #     v['pforma_nrv'] = 0.0
                #     print(f'in except ??? {v[var_b]}')
                #     b.append(v[var_b])
            print(f'eer her zip b  ? {b} diff {diff}')
            h = {
                'code': months[x + 2],
                'count': counter,
                'avg': sum(diff) / len(diff),
                'weighted_avg': sum(x * y for x, y in zip(b, diff)) / sum(b),
                'end': datetime.datetime.strptime(months[x + 2], '%b-%y'),
                'start': datetime.datetime.strptime(months[x], '%b-%y'),
                'months': [months[x], months[x + 1], months[x + 2]]
            }

            if neg:
                h['weighted_avg'] = -h['weighted_avg']
            print(f'document ==> {h}')
            # r = db.collection(collection_name).document(months[x + 2])
            # r.set(h)
        except Exception as e:
            print(f"error {e}")


def add_accounting_values():
    """
    Goes through all Sold repos and adds Darren's values.
    :return:
    """
    import pdb;
    pdb.set_trace()
    repo_ref = db.collection('repos')
    # query = repo_ref.where('status', '==', 'Sold').where('gaap_date', '>=', datetime(year=2018, month=1,
    # day=1)).stream()
    query = repo_ref.where('gaap_date', '>=', datetime.datetime(year=2018, month=1, day=1)).stream()
    query = [snapshot for snapshot in query]
    for d in query:
        row = d.to_dict()
        # print(row) print(datetime.datetime.strptime(row['date_sold'], '%Y-%m-%dT%H:%M:%S.%fZ').month,
        # datetime.datetime.now().month) if row['date_sold'].month == datetime.datetime.now().month
        if row['status'] == 'Sold':
            try:
                codes = row['acct_sold_month']
                s = db.collection('real_disc_to_nrv').document(codes).get()
                row['repo_allow2_hist'] = row['repo_allow2_(hist)']
                del row['repo_allow2_(hist)']
                row['repo_allow2_hist'] = float(s.to_dict()['weighted_avg'])
                row['pforma_nrv'] = round(row['acct_min_val'] * (1 + row['repo_allow2_hist']), 2)
                print(f'pforma_nrv {row["pforma_nrv"]}')
                row['gain_loss'] = row['gain_(loss)']

                row['pforma_gain_loss'] = (row['actual_proceeds'] - row['pforma_nrv'])
                # print(f'pforma_gain_loss {row["pforma_gain_loss"]}')
                try:
                    row['pforma_diff'] = min(row['pforma_gain_loss'] / row['pforma_nrv'], 0)
                except:
                    row['pforma_diff'] = 0
                # print(f"pforma diff = pforma gain loss: {row['pforma_gain_loss']} / pforma nrv: {row['pforma_nrv']}")
                del row['gain_(loss)']
                d.reference.update(row)
                # print(f"{row['loan']} updated")

            except TypeError as e:
                print('add_accounting_values TypeError', row['loan'], e, row['status'])

            except KeyError as e:
                print('add_accounting_values KeyError', row['loan'], e, row['status'])
                print(row)
        elif row['status'] == 'Repo':
            try:
                s = db.collection('real_disc_to_nrv').document(row['acct_repo_month']).get()
                row['repo_allow2_hist'] = float(s.to_dict()['weighted_avg'])
                # row['gain_loss']=row['gain_(loss)']

                # row['repo_allow2_hist']=row['repo_allow2_(hist)']
                try:
                    del row['repo_allow2_(hist)']
                except:
                    pass
                try:
                    del row['gain_(loss)']
                except:
                    pass
                d.reference.update(row)
            except Exception as e:
                print(f"Error updating repo: {row['loan']} {e}")

            # def trigger(request):


if __name__ == '__main__':
    logging.info('building real_disc_to_nrv table for last month')
    month_list = make_month_list(start_year=2018)
    print(month_list)
    # build_all_historical_tables(months=month_list, var_diff='acct_diff',
    #                           var_b='acct_min_val', collection_name='real_disc_to_nrv')

    # add_accounting_values()
    build_all_historical_tables(months=month_list,
                                var_diff='pforma_diff',
                                var_b='pforma_nrv',
                                collection_name='val_allow')
