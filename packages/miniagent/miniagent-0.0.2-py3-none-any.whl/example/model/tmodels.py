from miniagent import db
from miniagent.models import YesNoEnum
from sqlalchemy import Enum

class TPurchase(db.Model):
   id = db.Column(db.Integer, primary_key = True, nullable=False)
   product_code   = db.Column(db.String(100), nullable=False)
   payment_amount = db.Column(db.Integer, nullable=False)
   card_no = db.Column(db.String(100))
   approved_no = db.Column(db.String(100), nullable=False)
   approved_date = db.Column(db.DateTime(), nullable=False)
   refund_no = db.Column(db.String(100))
   refund_date = db.Column(db.DateTime())

class THealth(db.Model):
   id = db.Column(db.Integer, primary_key = True, nullable=False)
   adapter_name = db.Column(db.String(300), nullable=False)
   adaptee_name = db.Column(db.String(300))
   is_healthy = db.Column(Enum(YesNoEnum), nullable=False)
   checked_date = db.Column(db.DateTime(), nullable=False)
