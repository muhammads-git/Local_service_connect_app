from flask import Blueprint,session,redirect,render_template,request,url_for
from app.__init__ import mysql

payment_bp = Blueprint('payment_bp',__name__,'/payment')


@payment_bp.route('/pay/<int:job_id>')
def pay_now(job_id):
   if 'user_id' not in session: 
      return redirect(url_for('auths_bp.user_login'))
   
   # 
   # fetch bookings detail
   cursor = mysql.connection.cursor()
   cursor.execute(' SELECT user_id,provider_id,service_type,payment_status,service_price,plateform_percentage,total_price FROM bookings WHERE id=%s AND user_id=%s',(job_id,session['user_id']))


   