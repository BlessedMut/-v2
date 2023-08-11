from flask_login import UserMixin
from sqlalchemy.sql import func

from . import db


class AirtimeSold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    denomination = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    voucher_key = db.Column(db.String(30))
    serial_number = db.Column(db.String(60))
    batch_number = db.Column(db.String(60))
    expiry_date = db.Column(db.DateTime(timezone=True))
    vic = db.Column(db.String(30))
    receiver = db.Column(db.String(21))
    buyer = db.Column(db.String(21))
    user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=True)


class AirtimeAvailable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    denomination = db.Column(db.Float)
    voucher_key = db.Column(db.String(30))
    serial_number = db.Column(db.String(60))
    batch_number = db.Column(db.String(60))
    expiry_date = db.Column(db.String(21))
    vic = db.Column(db.Integer)
    user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)



class User(db.Model, UserMixin):
    # user model
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(50))
    mobile = db.Column(db.String(21))
    password = db.Column(db.String(150))
    role = db.Column(db.String(30))
    status = db.Column(db.Boolean)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    profile_pic = db.Column(db.String(250))
    airtime_sold = db.relationship('AirtimeSold', backref='sold_airtime', lazy=True)
    airtime_available = db.relationship('AirtimeAvailable', backref='available_airtime', lazy=True)
    netone_pinless = db.relationship('PinlessRecharges', backref='pinless_netone', lazy=True)
    netone_bundles = db.relationship('DataBundles', backref='bundles_netone', lazy=True)
    upload_logs = db.relationship('UploadLogs', backref='logs', lazy=True)
    company = db.relationship('Company', backref='company', lazy=True)


class PinlessRecharges(db.Model):
    __table__name = 'pinless_recharges'
    id = db.Column(db.Integer, primary_key=True)
    reply_code = db.Column(db.Integer)
    reply_message = db.Column(db.String(350))
    wallet_balance = db.Column(db.Float)
    amount = db.Column(db.Float)
    discount = db.Column(db.Float)
    initial_balance = db.Column(db.Float)
    final_balance = db.Column(db.Float)
    validity_window = db.Column(db.DateTime(timezone=True))
    data = db.Column(db.Float)
    sms = db.Column(db.Integer)
    agent_reference = db.Column(db.String(100))
    recharge_id = db.Column(db.String(100))
    user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)


class DataBundles(db.Model):
    __table__name = 'data_bundles'
    id = db.Column(db.Integer, primary_key=True)
    reply_code = db.Column(db.Integer)
    reply_message = db.Column(db.String(350))
    wallet_balance = db.Column(db.Float)
    amount = db.Column(db.Float)
    discount = db.Column(db.Float)
    initial_balance = db.Column(db.Float)
    final_balance = db.Column(db.Float)
    validity_window = db.Column(db.DateTime(timezone=True))
    data = db.Column(db.Float)
    sms = db.Column(db.Integer)
    agent_reference = db.Column(db.String(100))
    recharge_id = db.Column(db.String(100))
    user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)


# Contact Management
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(250))
    phone_number = db.Column(db.String(15))
    departments = db.relationship('Department', backref='company', lazy=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)



class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    employees = db.relationship('Employee', backref='department', lazy=True)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)


class UploadLogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
