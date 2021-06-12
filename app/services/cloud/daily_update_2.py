from datetime import datetime
import pytz
from dateutil.relativedelta import relativedelta

from app.models import Repos, RealDiscToNrv, ValAllow
from app import db


def make_month_list(start_year):
    """
    Returns list of all month-year between start_year and now.
    example ['Jan-18', 'Feb-18', ...]
    """
    start = datetime(start_year - 1, 10, 1).date()
    today = datetime.now(pytz.timezone('US/Central')).date()
    months = []
    while start < today:
        months.append(start.strftime('%b-%y'))
        start = start + relativedelta(months=+1)
    return months


def build_all_historical_tables(months, var_diff, var_b, collection_name, neg=False):
    """
    Builds real_disc_allow2 table. Will be calcs
    for 1 / 1 / start_year
    :param start_year: int the year to start
    :return: Firestore collection built
    """
    last_month = datetime.now(pytz.timezone('US/Central')).date() + relativedelta(months=-1)
    m = months.index(last_month.strftime('%b-%y'))
    print(f"m: {m}")
    for x in range(1, m):
        print([months[x], months[x + 1], months[x + 2]])
        try:
            # repo_ref = db.collection('repos')
            # query = repo_ref.where('status', '==', 'Sold').where('acct_sold_month', 'in',
            #                                                      [months[x], months[x + 1], months[x + 2]])
            query = Repos.query.filter(Repos.status == 'Sold') \
                .filter(Repos.acct_sold_month.in_([months[x], months[x+1], months[x+2]]))
            diff = []
            b = []
            # counter = len([d for d in query.stream()])
            counter = query.count()
            print(f'counter in up -> {counter}')
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
                    'weighted_avg': sum(x * y for x, y in zip(b, diff)) / sum(b),
                    'end': datetime.strptime(months[x + 2], '%b-%y'),
                    'start': datetime.strptime(months[x], '%b-%y'),
                    'months': [months[x], months[x + 1], months[x + 2]]
                }

                if neg:
                    h['weighted_avg'] = -h['weighted_avg']

                print(f'daily update h ----> {h}')
                r = ValAllow.query.filter_by(code=months[x+2]).first()
                if r:
                    # update
                    db.session.query(ValAllow).filter_by(code=months[x+2]).update(h)
                else:
                    r = ValAllow(**h)
                    db.session.add(r)
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
    # query = repo_ref.where('status', '==', 'Sold')
    # .where('gaap_date', '>=', datetime(year=2018, month=1, day=1)).stream()
    # query = repo_ref.where('gaap_date', '>=', datetime(year=2018, month=1, day=1)).stream()
    # query = repo_ref.where('gaap_date', '>=', datetime(year=2021, month=1, day=1)).stream()
    query = Repos.query.filter(Repos.status == 'Sold') \
        .filter(Repos.gaap_date >= datetime(year=2015, month=1, day=1))
    print(f'counter --> {query.count()}')
    # query = [snapshot for snapshot in query]
    for d in query:
        row = d  # .to_dict()
        if row.status == 'Sold':
            try:
                code = row.acct_repo_month
                # print(f'code -> {code}')
                # s = db.collection('real_disc_to_nrv').document(codes).get()
                s = RealDiscToNrv.query.filter_by(code=code).first()
                if s is None:
                    continue
                # row['repo_allow2_hist']=row['repo_allow2_(hist)']
                # del row['repo_allow2_(hist)']
                row.repo_allow2_hist = float(s.to_dict()['weighted_avg'])
                row.pforma_nrv = round(row.acct_min_val * (1 - abs(row.repo_allow2_hist)), 2)
                # row['gain_loss']=row['gain_(loss)']
                row.pforma_gain_loss = (row.actual_proceeds - row.pforma_nrv)
                try:
                    row.pforma_diff = min(row.pforma_gain_loss / row.pforma_nrv, 0)
                except:
                    row.pforma_diff = 0
                # del row['gain_(loss)']
                # d.reference.update(row)
                loan = row.loan
                print(f" updating sold --> {loan} ")
                db.session.merge(row)
                db.session.commit()
            except TypeError as e:
                print('add_accounting_values TypeError', row['loan'], e, row['status'])
            except KeyError as e:
                print('add_accounting_values KeyError', row['loan'], e, row['status'])
        elif row['status'] == 'Repo':
            try:
                # s = db.collection('real_disc_to_nrv').document(row['acct_repo_month']).get()
                s = RealDiscToNrv.query.filter_by(acct_repo_month=row['acct_repo_month']).first()
                row['repo_allow2_hist'] = float(s.to_dict()['weighted_avg'])
                try:
                    del row['repo_allow2_(hist)']
                except:
                    pass
                try:
                    del row['gain_(loss)']
                except:
                    pass
                print(f" updating repo --> {loan} ")
                db.session.commit()
                # d.reference.update(row)
            except Exception as e:
                print(f"Error updating repo: {row['loan']} {e}")
