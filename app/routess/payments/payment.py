from flask import Blueprint,session,redirect,render_template,request,url_for,flash
from app.utils.mail import create_notifcations
from app.__init__ import mysql

payment_bp = Blueprint('payment_bp',__name__,'/payment')


@payment_bp.route('/pay/<int:job_id>',methods=["GET","POST"])
def pay_now(job_id):
   if 'user_id' not in session: 
      return redirect(url_for('auths_bp.user_login'))
   
   try: 
      # initialize as None
      bookingDetails = None
      # fetch bookings detail
      cursor = mysql.connection.cursor()
      cursor.execute(' SELECT user_id,provider_id,service_type,payment_status,service_price,plateform_percentage,total_price FROM bookings WHERE id=%s AND user_id=%s',(job_id,session['user_id']))
      bookingDetails = cursor.fetchone()
   except mysql.connection.DatabaseError as e:
      flash('something went wrong','warning')
      print('DATABASE error while fetching booking details: {e}')
   
   finally:
      cursor.close()

   # NOW UPDATE BACKEND 
   try:
      cursor = mysql.connection.cursor()
      cursor.execute(' START TRANSACTION ')
      cursor.execute(' UPDATE bookings SET payment_status = %s WHERE id =%s AND user_id = %s',('paid',job_id,session['user_id']))
      customerName = session['username']
      flash(f'Payment successfull!','success')
      # notify provider
      providerID = bookingDetails[1]
      create_notifcations(providerID,job_id,f'Customer {customerName} has successfully transfered your money','chat')
      
   except mysql.connection.DatabaseError as e:
      mysql.connection.rollback()
      print(f'db error while payment: {e}')
      flash('Something went wrong','warning')

   finally:
      mysql.connection.commit()
      cursor.close()

   return redirect(url_for('dashboards_bp.user_dashboard', bookingDetails=bookingDetails))
