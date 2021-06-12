import json

from flask import Blueprint, request, render_template, redirect, url_for, send_file
from flask_login import login_user, login_required
from flask_user import roles_required, current_user

from . import db
import pandas as pd
import logging
from datetime import datetime, date
from operator import itemgetter
from app.services.utils import *
from .models import Category, Role, repo_categories

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    """ Login to repo Log App and redirect to home page """
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = lookup_user('email', email)  # raises TypeError is no user
            stored_password = user.password
        except(TypeError, KeyError):
            return render_template('login.html', error='Unknown email or password.')
        try:
            assert verify_password(stored_password, provided_password=password), \
                'The email or password provided was incorrect.'
        except AssertionError as e:
            return render_template('login.html', error=e)

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=False)
        return redirect(url_for('main.repo_log'))


@main.route('/repo-log', methods=['GET'])
@login_required
def repo_log():
    """Display Repo log web page"""
    if request.method == 'GET':

        # logging.info('building real_disc_to_nrv table for last month')
        # month_list = make_month_list(start_year=2018)
        # print(month_list)
        # logging.info('building all historical tables')
        # build_all_historical_tables(months=month_list,
        #                             var_diff='pforma_diff',
        #                             var_b='pforma_nrv',
        #                             collection_name='val_allow')

        msg = request.args.get('msg')
        logging.info(f"message received: {msg} {type(msg)}")
        return render_template('repo-log.html',
                               user=current_user,
                               msg=msg,
                               end=datetime.datetime.now().strftime('%Y-%m-%d'))
        # return repos
    else:
        return redirect('/')


@main.route('/api/repo-log', methods=['GET'])
def api_repo_log():
    if request.args.get('start'):
        start = datetime.datetime.fromtimestamp(int_me(request.args.get('start')) / 1000.0)
        until = datetime.datetime.fromtimestamp(int_me(request.args.get('until')) / 1000.0)
    else:
        start = datetime.datetime(2010, 1, 1)
        until = datetime.datetime.now()

    if request.args.get('loan') is not None and request.args.get('loan') != '':
        loan = request.args.get('loan').strip()
    else:
        loan = None

    status = request.args.get('status', default='Repo')
    # print(f'the status Start and End dates --> {status} {start} {until}  loan --->{loan}<----')
    repos = repolog(status, start, until, loan)
    return repos


@main.route('/repo', methods=['GET'])
def add_repo():
    """repo log view"""
    # user = lookup_user('uuid', request.cookies.get('sda'))
    # if request.method == 'GET' and authenticated(request.full_path):
    return render_template('repo.html', data=None, user=current_user)


@main.route('/api/getRoles/<string:username>')
def get_roles(username):
    """Get roles for the user"""
    user = User.query.filter(User.email == username).first()
    print(f'user{user.to_json()}')
    return user.to_json()


@main.route('/repo/<string:loan>', methods=['GET'])
def change_repo(loan):
    """Update repo log loan view"""
    # data = db.collection('repos').document(f'{loan}').get().to_dict()
    data = Repos.query.filter_by(loan=loan).first()
    return render_template('repo.html', data=data, user=current_user)


@main.route('/delete-repo', methods=['POST'])
@login_required
def delete_record_repo():
    """Delete a repo log"""
    req = request.get_json()
    loan = req['loan']
    repo = Repos.query.filter_by(loan=loan).first()
    print("we here", loan)
    if repo:
        db.session.delete(repo)
        db.session.commit()
        msg = f'Repo {loan} deleted'
    return redirect('/repo-log', msg=msg)


"""Change column name in csv file in download repo download"""
repoAccountingView = {
    "loan": "Loan",
    "status": "Loan Status",
    "repo_category": "Repo Category",
    "gaap_date": "GAAP Date",
    "noi_sent": "NOI Sent",
    "dafs": "DAFS",
    "date_sold": "Date Sold",
    "co_date": "CO Date",
    "dealer": "Dealer",
    "months_in_inventory": "Months in inventory",
    "location": "Location",
    "balance_repo_date": "Balance Repo Date",
    "cr_grade": "CR Grade",
    "chargeable_damages": "Chargeable Damages",
    "awv": "AWV",
    "mmr": "MMR",
    "cash_price": "Cash Price",
    "estimated_recovery": "Estimated Recovery",
    "current_mo_proceeds_estimate": "Current Month Proceeds",
    "eom_gaap_proceeds_estimate": "EOM GAAP Proceeds",
    "actual_proceeds": "Actual Proceeds",
    # "back_end_product_cancellations": "Back End Cancellations",
    "insurance_claims": "Insurance Claims",
    "gross_co_amt": "Gross CO Amount",
    "unearned_discount": "Unearned Discount",
    "net_loss_or_gain": "Net Loss or Gain",
    "recovery": "Recovery",
    "rem_bal": "Remaining Balance",
    "cash_or_new_ac": "Cash or New AC",
    "acct_min_val": "Min Value",
    "acct_gain_loss": "Gain / Loss",
    "acct_diff": "Difference",
    "acct_repo_month": "Repo Month",

    # "repo_allow2_hist": "Allow2",
    # "pforma_nrv": "Proforma NRV",
    # "pforma_gain_loss": "Proforma Gain / Loss",
    # "pforma_diff": "Proforma Difference"
}


@main.route('/download-repo', methods=['GET'])
@login_required
def download_repo():
    """Download repo log bucket"""
    # the exact order and spelling of the original columns
    s = datetime.datetime.strftime(datetime.datetime.now(), '%m%d%Y')
    repo_ref = Repos.query.all()
    filename = f'/tmp/exportRepo-{s}.csv'
    if request.method == 'GET':
        try:
            d = [z.to_json() for z in repo_ref]
            df = pd.DataFrame(d)
            try:
                df["gaap_date"] = df["gaap_date"].dt.strftime("%m/%d/%Y")
            except:
                pass
            try:
                df["noi_sent"] = df["noi_sent"].dt.strftime("%m/%d/%Y")
            except:
                pass
            try:
                df["dafs"] = df["dafs"].dt.strftime("%m/%d/%Y")
            except:
                pass
            try:
                df["date_sold"] = df["date_sold"].dt.strftime("%m/%d/%Y")
            except:
                pass
            try:
                df["co_date"] = df["co_date"].dt.strftime("%m/%d/%Y")
            except:
                pass
            df.rename(columns=repoAccountingView, inplace=True)
            df = df[list(repoAccountingView.values())]
            if os.path.isfile(filename):
                os.remove(filename)
            df.to_csv(filename, index=False)
            # client = storage.Client()
            # bucket = client.get_bucket('pif_bucket')
            # blob = bucket.blob(f'database-output-{s}.csv')
            # blob.upload_from_filename(filename, content_type='text/csv')
            return send_file(filename, mimetype='text/csv', as_attachment=True)
        except Exception as e:
            logging.error(f"Error on download database {type(e)}: {e}")
            return f"Error on download database: {e}"


@main.route('/repo', methods=['POST'])
def post_repo():
    """Add new repo view"""
    req = set_data_types(request.get_json())
    loan_id = req['loan']
    req['last_editor'] = current_user.email
    req['last_update'] = datetime.datetime.now()
    repo_category = req['repo_category']
    logging.info(f'the repo category {repo_category}')
    logging.info(f'the repo req {req}')
    req.pop('repo_category')
    repos = Repos.query.filter_by(loan=loan_id).first()
    """ Repo part. Only for saving/changing in repo table"""
    if repos:
        db.session.query(Repos).filter_by(loan=loan_id).update(req)
        db.session.commit()
        msg = f"Loan {req['loan']} updated"
    else:
        """Save new repo first so that category can be added for it"""
        print("the new loan case")
        msg = f"Repo {req['loan']} created"
        repos = Repos(**req)
        db.session.add(repos)
        db.session.commit()
    """ remove old categories """
    repos.categories = []
    """ Update with new categories """
    for c in repo_category:
        repos = Repos.query.filter_by(loan=loan_id).first()
        category = Category.query.filter_by(category_name=c).first()
        repos.categories.append(category)
    db.session.commit()
    return json.dumps({'msg': msg}), 200, {'ContentType': 'application/json'}
    # r = db.collection('repos').document(f"{req['loan']}")
    # if r.get().exists:
    #     msg = f"Loan {req['loan']} updated"
    # else:
    #     msg = f"Repo {req['loan']} created"
    # req['last_editor'] = user['email']
    # req['last_update'] = datetime.datetime.now()
    # r.set(req, merge=True)
    # logging.debug(f'sending message: {msg}')
    # return json.dumps({'msg': msg}), 200, {'ContentType': 'application/json'}
    # else:
    #    return redirect('/')


@main.route('/users', methods=['GET'])
@login_required
def user_management():
    """User Management View"""
    # users = [doc.to_dict() for doc in db.collection('users').stream()]
    user_all = users()  # get users from pgsql here
    print("value from utils", user_all)
    users_all = User.query.all()
    print("value from main", users_all)
    if request.method == 'GET' and current_user.has_roles('Admin'):
        return render_template('users.html', users=users_all, user=current_user)
    else:
        return redirect('/repo-log')


@main.route('/assign-permission', methods=["POST"])
def permission():
    """ Assign access permission  to user """
    if request.method == 'POST':
        user_data = request.get_json()
        perm = user_data['permission']
        email = user_data['email']
        user = User.query.filter(User.email == email).first()
        """ remove old roles """
        for role in user.roles:
            user.roles.remove(role)

        for p in perm:
            ''' Process the options object form users permission'''
            if p['selected']:
                role = Role.query.filter(Role.name == p['value']).first()
                if not role:
                    user.roles.append(Role(name=p['value']))
                else:
                    user.roles.append(role)
        db.session.commit()
        return render_template('users.html', user=current_user)


@main.route('/remove-admin/<unique_id>', methods=['GET'])
@login_required
def remove_admin(unique_id):
    """Remove admin role from user management"""
    logging.info(f'removing role for user with uid {unique_id}')
    user = User.query.filter_by(uuid=unique_id).first()
    role_admin = Role.query.filter(Role.name == 'Admin').first()
    if user.has_roles('Admin'):
        user.roles.remove(role_admin)
    db.session.commit()
    return redirect('/users')


@main.route('/give-admin/<unique_id>', methods=['GET'])
@login_required
def give_admin(unique_id):
    """ Add admin role from user management """
    logging.info(f'removing role for user with uid {unique_id}')
    user = User.query.filter_by(uuid=unique_id).first()
    role_admin = Role.query.filter(Role.name == 'Admin').first()
    if not user.has_roles('Admin'):
        user.roles.append(role_admin)
    db.session.commit()
    return redirect('/users')


@main.route('/remove-user/<unique_id>', methods=['GET'])
def remove_user(unique_id):
    """Remove user from user management"""
    user = lookup_user('uuid', unique_id)
    if request.method == 'GET':
        if user == current_user:
            # db.session.commit()
            message = " active user can't be deleted"
        else:
            usr = User.query.filter_by(uuid=unique_id).first()
            db.session.delete(usr)
            db.session.commit()
            message = f"{user['email']} has been deleted"
        return render_template('users.html', msg=message), 200
    else:
        return redirect('/')


# @main.route('/test-email')
# def test_email():
#     from sendgrid import SendGridAPIClient
#     from sendgrid.helpers.mail import Mail
#     message = Mail(
#         from_email='info@samedayauto.net',
#         to_emails='dev@samedayauto.net',
#         subject='Sending with Twilio SendGrid is Fun',
#         html_content='<strong>and easy to do anywhere, even with Python</strong>')
#     try:
#         sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#         response = sg.send(message)
#         print(response.status_code)
#         print(response.body)
#         print(response.headers)
#     except Exception as e:
#         print(e.message)
#
#     return "success"
