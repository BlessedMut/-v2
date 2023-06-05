from flask_login import UserMixin
from sqlalchemy.sql import func

from . import db


class AirtimeSold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    denomination = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    voucher_key = db.Column(db.Integer)
    serial_number = db.Column(db.Integer)
    batch_number = db.Column(db.Integer)
    expiry_date = db.Column(db.DateTime(timezone=True))
    vic = db.Column(db.Integer)
    receiver = db.Column(db.String(21))
    buyer = db.Column(db.String(21))
    user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)


class AirtimeAvailable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    denomination = db.Column(db.Float)
    voucher_key = db.Column(db.Integer)
    serial_number = db.Column(db.Integer)
    batch_number = db.Column(db.Integer)
    expiry_date = db.Column(db.String(21))
    vic = db.Column(db.Integer)


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
    airtime = db.relationship('AirtimeSold')


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

