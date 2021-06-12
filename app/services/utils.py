import json

from flask import jsonify, make_response
import binascii
import hashlib
import datetime
import os
from sqlalchemy import and_, desc, or_
import pytz
from dateutil.relativedelta import *
from app.models import User, Repos
from app import db


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                 salt, 100000)
    pwhash = binascii.hexlify(pwhash)
    return (salt + pwhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwhash = hashlib.pbkdf2_hmac('sha512',
                                 provided_password.encode('utf-8'),
                                 salt.encode('ascii'),
                                 100000)
    pwhash = binascii.hexlify(pwhash).decode('ascii')
    return pwhash == stored_password


def lookup_user(key, value):
    print(f'in here ---> {key}  ==  {value}')
    user = User.query.filter_by(email=value).first()
    if key == 'uuid':
        user = User.query.filter_by(uuid=value).first()
    print("the user %s" % user)
    if not user:  # or not check_password_hash(user.password, password):
        raise TypeError
    return user


def update_repo(loan_id, req):
    # Repos.query.filter_by(loan=loan_id).first().update(**req)
    repos = Repos.query.filter_by(loan=loan_id)
    repos(**req)
    db.session.commit()


def repolog(status, start, until, loan):
    repos = Repos.query.filter(
        and_(Repos.gaap_date >= start, Repos.gaap_date <= until, Repos.status == status)).order_by(
        desc(Repos.gaap_date))
    if status == "Sold":
        repos = Repos.query.filter(
            and_(Repos.date_sold >= start, Repos.date_sold <= until, Repos.status == status)).order_by(
            desc(Repos.date_sold))
    if loan is not None and loan != '':
        repos = Repos.query.filter(
            and_(Repos.loan.ilike(f'{loan}%'))) \
            .order_by(desc(Repos.date_sold))
        # repos = Repos.query.filter(Repos.loan.ilike(f'%{loan}%')).order_by(desc(Repos.date_sold))
    repos_arr = []
    count = 0
    for repo in repos:
        count = count + 1
        repo_dict = repo.to_dict()
        if repo.categories:
            cats = repo.categories
            repo_categories = []
            for c in cats:
                repo_categories.append(c.category_name)
            repo_dict['repo_category'] = repo_categories
        repos_arr.append(repo_dict)
    return make_response(jsonify(repos_arr))


def piflog():
    pif = PifLog.query.filter().order_by(desc(PifLog.date_pif))
    pif_arr = []
    for pifs in pif:
        pif_arr.append(pifs.to_dict())
    return make_response(jsonify(pif_arr))


def nrv_lookup(code):
    nrv = RealDiscToNrv.query.filter_by(code=code).all()
    nrv_arr = []
    for n in nrv:
        nrv_arr.append(n.to_dict())
    print(f'---> \n{nrv_arr}')
    return make_response(jsonify(nrv_arr))


def nrv_lookup2(months):
    months_arr = months.split(',')
    print(f'months {months_arr[0]}')

    repo = Repos.query.filter(Repos.status == 'Sold') \
        .filter(or_(Repos.acct_sold_month == months_arr[0], Repos.acct_sold_month == months_arr[1],
                    Repos.acct_sold_month == months_arr[2])) \
        .order_by(desc(Repos.loan)).all()

    repo_arr = []
    for n in repo:
        repo_arr.append(n.to_dict())
    # print(f'repo arr ---> \n{repo_arr}')
    return make_response(jsonify(repo_arr))


def extensionlog():
    all_extension = ExtensionLog.query.filter().order_by(desc(ExtensionLog.approved_date))
    ext_arr = []
    for ext in all_extension:
        ext_arr.append(ext.to_dict())
    return make_response(jsonify(ext_arr))


def title_follow_up(history):
    # all_follow_up = TitleFollowUp.query.order_by(TitleFollowUp.contract_date.desc()).all()
    start = datetime.datetime(2010, 1, 1)
    # all_follow_up = TitleFollowUp.query.filter(TitleFollowUp.app_received > start)\
    #     .order_by(TitleFollowUp.app_received.desc()).all()
    all_follow_up = TitleFollowUp.query.filter(and_(TitleFollowUp.app_received == None),
                                               (TitleFollowUp.contract_date != None)) \
        .order_by(TitleFollowUp.contract_date.desc()).all()
    if history:
        all_follow_up = TitleFollowUp.query.filter(TitleFollowUp.app_received >= start) \
            .order_by(TitleFollowUp.app_received.desc()).all()

    fup_arr = []
    for fup in all_follow_up:
        fup_arr.append(fup.to_dict())
    return make_response(jsonify(fup_arr))


def users():
    users_all = User.query.all()
    usr_arr = []
    for user in users_all:
        usr_arr.append(user.to_dict())
        return make_response(jsonify(usr_arr))


def build_date(d):
    if type(d) == datetime.datetime:
        return d
    elif type(d) == str:
        try:
            x = datetime.datetime.strptime(d, "%Y-%m-%dT%H:%M:%S.%fZ")
            new_date = x.replace(hour=0, minute=1, tzinfo=pytz.timezone('US/Central'))
            print(f'new date: ' + str(new_date))
            return new_date
        except ValueError:
            try:
                x = datetime.datetime.strptime(' '.join(d.split(' ')[0:4]), "%a %b %d %Y")
                new_date = x.replace(hour=0, minute=1, tzinfo=pytz.timezone('US/Central'))
                print(f'new date: ' + str(new_date))
                return new_date
            except ValueError:
                return None


def float_me(val):
    try:
        return float(val)
    except ValueError:
        return None


def int_me(val):
    try:
        return int(val)
    except ValueError:
        try:
            return int(float_me(val))
        except (ValueError, TypeError, OverflowError):
            return None


def set_data_types(d):
    # try:
    #     d['loan'] = round(float_me(d['loan']), 1)
    # except:
    #     d['loan'] = 0
    try:
        d['account_number'] = int_me(d['loan'].split('.')[1])
    except:
        d['account_number'] = 1
    d['year'] = int_me(d['year'])
    d['gaap_date'] = build_date(d['gaap_date'])
    d['customer_name'] = d['customer_name'].replace("'", "")
    d['dealer'] = d['dealer'].replace("'", "")
    d['sold_to'] = d['sold_to'].replace("'", "")
    d["repo_category"] = d['repo_category']
    d['noi_sent'] = build_date(d['noi_sent'])
    d['dafs'] = build_date(d['dafs'])
    d['date_sold'] = build_date(d['date_sold'])
    try:
        d['acct_sold_month'] = build_date(d['date_sold']).strftime('%b-%y')
    except (TypeError, AttributeError):
        d['acct_sold_month'] = None
    d['co_date'] = build_date(d['co_date'])
    d['mileage'] = int_me(d['mileage'])
    d['cr_grade'] = float_me(d['cr_grade'])
    d['chargeable_damages'] = int_me(d['chargeable_damages'])
    d['balance_repo_date'] = float_me(d['balance_repo_date'])
    d['awv'] = float_me(d['awv'])
    d['mmr'] = float_me(d['mmr'])
    d['cash_price'] = float_me(d['cash_price'])

    trial = float_me(d['estimated_recovery'])
    if trial:
        d['estimated_recovery'] = trial * 0.01
    else:
        d['estimated_recovery'] = 0.0
    if d["status"] == "Repo":
        d['current_mo_proceeds_estimate'] = float_me(d['current_mo_proceeds_estimate'])
    else:
        d['current_mo_proceeds_estimate'] = None
    d['actual_proceeds'] = float_me(d['actual_proceeds'])
    d['back_end_product_cancellation'] = float_me(d['back_end_product_cancellation'])
    d['insurance_claims'] = float_me(d['insurance_claims'])
    d['gross_co_amt'] = round(float_me(d['gross_co_amt']), 2)
    d['unearned_discount'] = float_me(d['unearned_discount'])
    d['acct_min_val'] = float_me(d['acct_min_val'])

    d['acct_gain_loss'] = float_me(d['acct_gain_loss'])
    b = [float_me(d['acct_diff']), 0.00]
    d['acct_diff'] = min(i for i in b if i is not None)
    d['net_loss_or_gain'] = float_me(d['net_loss_or_gain'])
    g = datetime.datetime.timestamp(datetime.datetime.now()) - datetime.datetime.timestamp(d['gaap_date'])
    if d['status'] == "Repo":
        d['months_in_inventory'] = round(((g / 86400) / 30), 1)
    else:
        d['months_in_inventory'] = None
    d['date_reinstate'] = build_date(d['date_reinstate'])
    d['acct_repo_month'] = build_date(d['gaap_date']).strftime('%b-%y')
    if d['date_sold']:
        d['acct_sold_month'] = build_date(d['date_sold']).strftime('%b-%y')
    d['eom_gaap_proceeds_estimate'] = float_me(d['eom_gaap_proceeds_estimate'])
    if not d['eom_gaap_proceeds_estimate'] and d['acct_repo_month']:
        try:
            acct_minimum_val = []
            if (d['mmr']) != None:
                acct_minimum_val.append(int_me(d['mmr']))
            if (d['cash_price']) != None:
                print(d['awv'])
                acct_minimum_val.append(int_me(d['cash_price']))
            if (d['awv']) != None:
                acct_minimum_val.append(int_me(d['awv']))
            """exclude firestore"""
            # discount = db.collection('real_disc_to_nrv').document(d['acct_repo_month']).get().to_dict()[
            # 'weighted_avg'] d['eom_gaap_proceeds_estimate'] = min(acct_minimum_val) * (1 - discount)
            """exclude firestore"""
        except Exception:
            pass

    return d


def set_data_type_pif(d):
    d['account_number'] = int_me(d['account_number'])
    d["name"] = d["name"]
    d["date_pif"] = build_date(d["date_pif"])
    d["status"] = d["status"]
    d["op"] = float_me(d["op"])
    d["method"] = d["method"]
    d["op_sent"] = d["op_sent"]
    d["gap_or_warr_cancelation_required"] = d["gap_or_warr_cancelation_required"]
    d["date_canceled"] = build_date(d["date_canceled"])
    d["ttl_cntrct_recd"] = build_date(d["ttl_cntrct_recd"])
    d["ttl_cntrct_sent"] = build_date(d["ttl_cntrct_sent"])
    d["comments"] = d["comments"]
    return d


def set_data_type_ext(d):
    d["customer_number"] = (d["customer_number"])
    d["account_number"] = int_me(d["account_number"])
    d["requested_date"] = build_date(d["requested_date"])
    d["final_status"] = d["final_status"]
    d["approved_date"] = build_date(d["approved_date"])
    d["approved_by"] = d["approved_by"]
    d["extension_type"] = d["extension_type"]
    d["collector"] = d["collector"]
    d["prior_due_date"] = build_date(d["prior_due_date"])
    d["new_due_date"] = build_date(d["new_due_date"])
    d["prior_maturity_date"] = build_date(d["prior_maturity_date"])
    d["new_maturity_date"] = build_date(d["new_maturity_date"])
    return d


def set_data_type_follow(d):
    d["customer_number"] = int_me(d["customer_number"])
    d["account"] = int_me(d["account"])
    d["dealer"] = d["dealer"]
    d["name"] = d["name"]
    d['app_received'] = build_date(d['app_received'])
    if d['app_received'] is None:
        d['app_received'] = ""
    d["contract_date"] = build_date(d["contract_date"])
    d["title_due"] = build_date(d["title_due"])
    d["white_slip_received"] = build_date(d["white_slip_received"])
    d["title_received"] = build_date(d["title_received"])
    d["follow_up_comments"] = d["follow_up_comments"]
    return d


def set_data_type_usr(d):
    d["email"] = d["email"]
    d["name"] = d["name"]
    d["admin"] = d["admin"]
    d["uuid"] = d["uuid"]
    return d


def make_month_list(start_year):
    """
    Returns list of all month-year between start_year and now.
    example ['Jan-18', 'Feb-18', ...]
    """
    start = datetime.datetime(start_year - 1, 10, 1).date()
    today = datetime.datetime.now(pytz.timezone('US/Central')).date()
    months = []
    while start < today:
        months.append(start.strftime('%b-%y'))
        start = start + relativedelta(months=+1)
    return months
