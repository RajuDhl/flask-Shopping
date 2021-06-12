import os
from datetime import datetime
import pytz
from dateutil.relativedelta import relativedelta
import logging
from app.services.utils import *
from app.models import RealDiscToNrv


def add_repo_month():
    # repo_ref = db.collection('repos').where('status', '==', 'Repo').where('gaap_date', '>=', datetime.datetime(
    # year=2018, month=1, day=1))
    repo_ref = Repos.query.filter(Repos.status == 'Sold') \
        .filter(Repos.gaap_date >= datetime.datetime(year=2018, month=1, day=1))
    repos = [d.to_dict() for d in repo_ref]
    # print(f'repos {repos}')
    counter = 0
    for d in repos:
        if 'acct_repo_month' not in d or d['acct_repo_month'] == '':
            d['acct_repo_month'] = d['gaap_date'].strftime('%b-%y')
            print(f'd in repos ---> {d}')
            # r = db.collection('repos').document(str(d['loan']))
            # r.update(d)
            counter += 1
    print(f"{counter} updated")


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
    for x in range(1, m):
        print(f'months -->  {[months[x], months[x + 1], months[x + 2]]}')
        try:
            # repo_ref = db.collection('repos')
            # query = repo_ref.where('status', '==', 'Sold').where('acct_sold_month', 'in',
            #                                                      [months[x], months[x + 1], months[x + 2]])

            query = Repos.query.filter(Repos.status == 'Sold') \
                .filter(Repos.acct_sold_month.in_([months[x], months[x+1], months[x+2]]))

            diff = []
            b = []
            # counter = len([d for d in query.count()])
            counter = query.count()
            print(f'counter {counter}')

            if counter != 0:
                for doc in query:
                    try:
                        if doc.to_dict()[var_diff] is not None:
                            diff.append(doc.to_dict()[var_diff])
                            b.append(doc.to_dict()[var_b])
                    except KeyError as e:
                        print(
                            f'build_all_historical_tables - KeyError: {e} loan: {doc.to_dict()["loan"]}, {doc.to_dict()["status"]} {months[x + 2]}')
                    except TypeError as e:
                        print(
                            f'build_all_historical_tables - TypeError: {e} loan: {doc.to_dict()["loan"]}, {doc.to_dict()["status"]} {months[x + 2]}')

                h = {
                    'code': months[x + 2],
                    'count': counter,
                    'avg': sum(diff) / len(diff),
                    'weighted_avg': round(sum(x * y for x, y in zip(b, diff)) / sum(b), 5),
                    'end': datetime.datetime.strptime(months[x + 2], '%b-%y'),
                    'start': datetime.datetime.strptime(months[x], '%b-%y'),
                    'months': [months[x], months[x + 1], months[x + 2]]
                }

                print(f'the h --> {h}')

                if neg:
                    h['weighted_avg'] = -h['weighted_avg']

                nrv = RealDiscToNrv.query.filter_by(code=months[x+2]).first()
                print(f'the nrv {nrv}')
                if nrv:
                    print(f'updating nrv {nrv.code} with h --->  {h}')
                    db.session.query(RealDiscToNrv).filter_by(code=months[x+2]).update(h)
                else:
                    print(f'Adding new entry to nrv with h --> ${h}')
                    nrv = RealDiscToNrv(**h)
                    db.session.add(nrv)
                db.session.commit()
                # r = db.collection(collection_name).document(months[x + 2])
                # r.set(h)
        except Exception as e:
            print(f"error {e}")


def add_accounting_values():
    """
    Goes through all Sold repos and adds Darren's values.
    :return:
    """
    # repo_ref = db.collection('repos')
    # query = repo_ref.where('status', '==', 'Sold').where('gaap_date', '>=', datetime(year=2018, month=1, day=1)).stream()
    # query = repo_ref.where('gaap_date', '>=', datetime.datetime(year=2015, month=1, day=1)).stream()
    query = Repos.query.filter(Repos.gaap_date >= datetime.datetime(year=2015, month=1, day=1))
    for d in query:
        row = d  # .to_dict()
        # print(datetime.datetime.strptime(row['date_sold'], '%Y-%m-%dT%H:%M:%S.%fZ').month, datetime.datetime.now().month)
        # if row['date_sold'].month == datetime.datetime.now().month
        if row.status == 'Sold':
            try:
                # s = db.collection('real_disc_to_nrv').document(row['acct_repo_month']).get()
                s = RealDiscToNrv.query.filter_by(code=row.acct_repo_month).first()

                print(f'the s --> {s} code {row.acct_repo_month}')

                row.repo_allow2_hist = float(s.weighted_avg)
                row.pforma_nrv = round(row.acct_min_val * (1 - row.repo_allow2_hist), 2)
                # print(f'pforma_nrv {row["pforma_nrv"]}')
                row.pforma_gain_loss = min(0, row.actual_proceeds - row.pforma_nrv)
                # print(f'pforma_gain_loss {row["pforma_gain_loss"]}')
                try:
                    row.pforma_diff = row.pforma_gain_loss / row.pforma_nrv
                except TypeError:
                    print(
                        f"pforma diff = pforma gain loss: {row.pforma_gain_loss} / pforma nrv: {row.pforma_nrv}")
                db.session.merge(row)
                db.session.commit()
                # d.reference.update(row)
                # print(f"{row['loan']} updated")

            except TypeError as e:
                print('add_accounting_values TypeError', row['loan'], e, row['status'])
                print(row)
            except KeyError as e:
                print('add_accounting_values KeyError', row['loan'], e, row['status'])
                print(row)


# def trigger(request):
if __name__ == '__main__':
    add_repo_month()
    then = datetime.datetime.now()
    month_list = make_month_list(start_year=2018)
    build_all_historical_tables(months=month_list, var_diff='acct_diff', var_b='acct_min_val',
                                collection_name='real_disc_to_nrv', neg=True)
    print(f"completed in {(datetime.datetime.now() - then).seconds} seconds")
