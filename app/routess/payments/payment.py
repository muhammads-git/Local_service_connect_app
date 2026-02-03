from flask import Blueprint
from app.__init__ import mysql

payment_bp = Blueprint('payment_bp',__name__,'/payment')


@payment_bp.route('/pay')
def pay_now():
   return 'coming soon ..'