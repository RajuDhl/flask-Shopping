from sqlalchemy import Column

from app import db
# from flask_login import UserMixin
from flask_user import UserMixin
from dataclasses import dataclass


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    activity = db.Column(db.DateTime)
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    ip = db.Column(db.String(15))
    verified = db.Column(db.Boolean)
    uuid = db.Column(db.String(36))

    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='user_roles')

    def to_json(self):
        return {
            "roles": [{"name": a.name} for a in self.roles] if self.roles else None
        }

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    display_name = db.Column(db.String(50), unique=True)

    def __str__(self):
        return self.name


# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


repo_categories = db.Table(
    "repo_categories",
    db.Column("repo_id", db.Integer, db.ForeignKey("repos.id")),
    db.Column("category_id", db.Integer, db.ForeignKey("category.id")),
)


@dataclass
class Repos(db.Model):
    __tablename__ = 'repos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # primary keys are required by SQLAlchemy
    awv = db.Column(db.Float)
    eom_gaap_proceeds_estimate = db.Column(db.Float)
    balance_repo_date = db.Column(db.Float)
    loan = db.Column(db.String(255))
    cash_or_new_ac = db.Column(db.String(255))
    location = db.Column(db.String(255))  # : "SOLD",
    back_end_product_cancellation = db.Column(db.Float)  # : 0,
    sold_to = db.Column(db.String(255))  # "TEXAS CAN",
    acct_sold_month = db.Column(db.String(255))  # "Oct-13",
    gaap_date = db.Column(db.DateTime)
    name = db.Column(db.String(255))
    dafs = db.Column(db.DateTime)
    make = db.Column(db.String(255))
    acct_diff = db.Column(db.Float)
    insurance_claims = db.Column(db.Float)
    noi_sent = db.Column(db.DateTime)
    co_date = db.Column(db.DateTime)
    reason = db.Column(db.String(255))
    unearned_discount = db.Column(db.Float)
    recovery = db.Column(db.Integer)
    mmr = db.Column(db.Float)
    gross_co_amt = db.Column(db.Float)
    current_mo_proceeds_estimate = db.Column(db.Float)
    date_sold = db.Column(db.DateTime)
    date_reinstate = db.Column(db.DateTime)
    chargeable_damages = db.Column(db.Float)
    net_loss_or_gain = db.Column(db.Float)
    acct_repo_month = db.Column(db.String(255))
    cash_price = db.Column(db.Float)
    rem_bal = db.Column(db.Float)
    true_up_amount = db.Column(db.Float)
    months_in_inventory = db.Column(db.Float)
    actual_proceeds = db.Column(db.Float)
    vin = db.Column(db.String(255))
    model = db.Column(db.String(255))
    account_number = db.Column(db.Integer)
    min_val = db.Column(db.Float)
    gain_loss = db.Column(db.Float)
    diff = db.Column(db.Float)
    repo_allow2_hist = db.Column(db.Float)
    proforma_gl = db.Column(db.Float)
    customer_name = db.Column(db.String(255))
    status = db.Column(db.String(255))
    exception_detail = db.Column(db.String(255))
    acct_gain_loss = db.Column(db.Integer)
    exception = db.Column(db.String(255))
    estimated_recovery = db.Column(db.Float)
    same_month_sale = db.Column(db.String(255))
    acct_min_val = db.Column(db.Integer)
    notes = db.Column(db.String(255))
    trim = db.Column(db.String(255))
    true_up_transaction = db.Column(db.String(255))
    mileage = db.Column(db.Integer)
    dealer = db.Column(db.String(255))
    # repo_category = db.Column(db.String(255))
    #  category = db.relationship('Category', backref='category', lazy='dynamic')
    # repo_category = (postgresql.ARRAY(db.String(55)))
    categories = db.relationship(
        "Category",
        secondary=repo_categories,
        backref="repos",
        lazy="select",
        cascade="all,delete"
    )
    cr_grade = db.Column(db.Float)
    year = db.Column(db.Integer)
    pforma_diff = db.Column(db.Float)
    pforma_nrv = db.Column(db.Float)
    last_editor = db.Column(db.String(255))
    last_update = db.Column(db.DateTime)

    def to_json(self):
        return {
            "loan": self.loan if self.loan else None,
            "status": self.status if self.status else None,
            "repo_category": [a.category_name for a in self.categories] if self.categories else None,
            "gaap_date": self.gaap_date if self.gaap_date else None,
            "noi_sent": self.noi_sent if self.noi_sent else None,
            "dafs": self.dafs if self.dafs else None,
            "date_sold": self.date_sold if self.date_sold else None,
            "co_date": self.co_date if self.co_date else None,
            "dealer": self.dealer if self.dealer else None,
            "months_in_inventory": self.months_in_inventory if self.months_in_inventory else None,
            "location": self.location if self.location else None,
            "balance_repo_date": self.balance_repo_date if self.balance_repo_date else None,
            "cr_grade": self.cr_grade if self.cr_grade else None,
            "chargeable_damages": self.chargeable_damages if self.chargeable_damages else None,
            "awv": self.awv if self.awv else None,
            "mmr": self.mmr if self.mmr else None,
            "cash_price": self.cash_price if self.cash_price else None,
            "estimated_recovery": self.estimated_recovery if self.estimated_recovery else None,
            "current_mo_proceeds_estimate": self.current_mo_proceeds_estimate if self.current_mo_proceeds_estimate else None,
            "eom_gaap_proceeds_estimate": self.eom_gaap_proceeds_estimate if self.eom_gaap_proceeds_estimate else None,
            "actual_proceeds": self.actual_proceeds if self.actual_proceeds else None,
            "insurance_claims": self.insurance_claims if self.insurance_claims else None,
            "gross_co_amt": self.gross_co_amt if self.gross_co_amt else None,
            "unearned_discount": self.unearned_discount if self.unearned_discount else None,
            "net_loss_or_gain": self.net_loss_or_gain if self.net_loss_or_gain else None,
            "recovery": self.recovery if self.recovery else None,
            "rem_bal": self.rem_bal if self.rem_bal else None,
            "cash_or_new_ac": self.cash_or_new_ac if self.cash_or_new_ac else None,
            "acct_min_val": self.acct_min_val if self.acct_min_val else None,
            "acct_gain_loss": self.acct_gain_loss if self.acct_gain_loss else None,
            "acct_diff": self.acct_diff if self.acct_diff else None,
            "acct_repo_month": self.acct_repo_month if self.acct_repo_month else None,
        }

    def get_category(self):
        return self.categories

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@dataclass
class Category(db.Model):
    __tablename__ = 'category'
    id = Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(80))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __str__(self):
        return self.category_name


# @dataclass
# class PifLog(db.Model):
#     __tablename__ = 'pif_log'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # primary keys are required by SQLAlchemy
#     customer_number = db.Column(db.String(255))
#     account_number = db.Column(db.Integer)
#     name = db.Column(db.String(255))
#     date_pif = db.Column(db.DateTime)
#     status = db.Column(db.String(255))
#     op = db.Column(db.String(255))
#     method = db.Column(db.String(255))
#     op_sent = db.Column(db.DateTime)
#     gap_or_warr_cancelation_required = db.Column(db.String(255))
#     date_canceled = db.Column(db.DateTime)
#     ttl_cntrct_recd = db.Column(db.DateTime)
#     ttl_cntrct_sent = db.Column(db.DateTime)
#     comments = db.Column(db.String(255))
#     unnamed = db.Column(db.String(255))
#     last_editor = db.Column(db.String(255))
#     last_update = db.Column(db.DateTime)
#
#     def to_dict(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}
#
#
# @dataclass
# class ExtensionLog(db.Model):
#     __tablename__ = 'extension'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # primary keys are required by SQLAlchemy
#     customer_number = db.Column(db.Integer)
#     account_number = db.Column(db.Integer)
#     requested_date = db.Column(db.DateTime)
#     final_status = db.Column(db.String(255))
#     approved_date = db.Column(db.DateTime)
#     approved_by = db.Column(db.String(255))
#     extension_type = db.Column(db.String(255))
#     collector = db.Column(db.String(255))
#     prior_due_date = db.Column(db.DateTime)
#     new_due_date = db.Column(db.DateTime)
#     prior_maturity_date = db.Column(db.DateTime)
#     new_maturity_date = db.Column(db.DateTime)
#     last_editor = db.Column(db.String(255))
#     last_update = db.Column(db.DateTime)
#
#     def to_dict(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}
#
#
# @dataclass
# class TitleFollowUp(db.Model):
#     __tablename__ = 'title_follow_up'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # primary keys are required by SQLAlchemy
#     customer_number = db.Column(db.Integer)
#     account = db.Column(db.Integer)
#     dealer = db.Column(db.String(255))
#     name = db.Column(db.String(255))
#     app_received = db.Column(db.DateTime)
#     contract_date = db.Column(db.DateTime)
#     title_due = db.Column(db.DateTime)
#     white_slip_received = db.Column(db.DateTime)
#     title_received = db.Column(db.DateTime)
#     dealer = db.Column(db.String(255))
#     follow_up_comments = db.Column(db.String(255))
#     unnamed = db.Column(db.String(255))
#     last_editor = db.Column(db.String(255))
#     last_update = db.Column(db.DateTime)
#
#     def to_dict(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}
#
#
# @dataclass
# class RealDiscToNrv(db.Model):
#     __tablename__ = 'real_disc_to_nrv'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # primary keys are required by SQLAlchemy
#     avg = db.Column(db.Float)
#     code = db.Column(db.String(255))
#     count = db.Column(db.Integer)
#     end = db.Column(db.DateTime)
#     months = db.Column(db.String(255))
#     start = db.Column(db.DateTime)
#     weighted_avg = db.Column(db.Float)
#
#     def to_dict(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}
#
#
# @dataclass
# class ValAllow(db.Model):
#     __tablename__ = 'val_allow'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # primary keys are required by SQLAlchemy
#     avg = db.Column(db.Float)
#     code = db.Column(db.String(255))
#     count = db.Column(db.Integer)
#     end = db.Column(db.DateTime)
#     months = db.Column(db.String(255))
#     start = db.Column(db.DateTime)
#     weighted_avg = db.Column(db.Float)
#
#     def to_dict(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}
