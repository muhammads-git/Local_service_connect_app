from flask import Blueprint,session,redirect,render_template,request,url_for,flash
from app.utils.mail import create_notifcations
from app.__init__ import mysql
from app.routess.payments.mockGateway import MockGateway


payment_bp = Blueprint('payment_bp',__name__,'/payment')



@payment_bp.route('/initiate-payment<int:job_id>',methods=['GET','POST'])
def initiate_payment(job_id):
   """
   Docstring for initiate_payment
   
   :param job_id: Description
   lets initiate payment with fetching the data from bookings table , to inserting it into, 
   transaction

   """
   if 'user_id' not in session:
      return redirect(url_for('auths_bp.user_login'))
   
   result = None
   transaction_id = None
   
   try:

      cursor = mysql.connection.cursor()
      cursor.execute(""" SELECT b.user_id,b.status,s.service_name,s.price FROM bookings b LEFT JOIN
                     services s ON b.provider_id = s.provider_id
                     WHERE b.user_id=%s AND b.id=%s """,
                     (session['user_id'],job_id))

      bookings_data = cursor.fetchone()

   except Exception as e:
      print(f'error: {e}')




   # INSERT INTO TRANZCTIONS
   try:

      cursor = mysql.connection.cursor()
      cursor.execute(""" INSERT INTO transactions (booking_id,user_id,amount,transaction_status ) VALUES(%s,%s,%s,%s)"""
                     ,(job_id,session['user_id'],bookings_data[3],'pending'))
      
      transaction_id = cursor.lastrowid

      # call gateway
      gateway = MockGateway()
      result = gateway.createPayment(bookings_data[3],job_id)

      # update transaction gateway reference
      cursor.execute(' UPDATE transactions SET gateway_reference=%s WHERE id=%s',(result['reference'],transaction_id))


   except Exception as e:
      print(f'error: {e}')
   
   finally:
      mysql.connection.commit()
      cursor.close()

   if result and result.get('checkout_url'):
        return redirect(result['checkout_url'])
   else:
        return redirect(url_for('dashboards_bp.user_dashboard'))

@payment_bp.route('/mock-checkout')
def mock_checkout():
   reference= request.args.get('reference')
   amount = request.args.get('amount')

   return f'''
    <html>
        <body>
            <h1>Mock Payment Gateway</h1>
            <p>Amount: {amount} PKR</p>
            <p>Reference: {reference}</p>
            
            <a href="/payment-callback/mock?reference={reference}&status=success">
                Pay Now (Success)
            </a>
            <br>
            <a href="/payment-callback/mock?reference={reference}&status=failed">
                Pay Now (Failure)
            </a>
        </body>
    </html>
    '''

@payment_bp.route('/payment-callback/mock')
def mock_callback():
    reference = request.args.get('reference')
    status = request.args.get('status')
    
    # 1. Gateway verify karo
    gateway = MockGateway()
    result = gateway.verifyPayment(reference)
    
    if status == 'success' and result['success']== True:
        cursor = mysql.connection.cursor() 
        # 2. Transaction update karo
        cursor.execute('''
            UPDATE transactions 
            SET transaction_status = 'completed' 
            WHERE gateway_reference = %s
        ''', (reference,))
        
        # 3. Booking update karo
        cursor.execute('''
            UPDATE bookings b
            JOIN transactions t ON b.id = t.booking_id
            SET b.payment_status = 'paid'
            WHERE t.gateway_reference = %s
        ''', (reference,))
        
        mysql.connection.commit()
        flash('Payment successful!', 'success')
    else:
        flash('Payment failed!', 'danger')
    
    return redirect(url_for('dashboards_bp.user_dashboard'))




























# @payment_bp.route('/pay/<int:job_id>',methods=["GET","POST"])
# def pay_now(job_id):
#    if 'user_id' not in session: 
#       return redirect(url_for('auths_bp.user_login'))
   
#    try: 
#       # initialize as None
#       bookingDetails = None
#       # fetch bookings detail
#       cursor = mysql.connection.cursor()
#       cursor.execute(' SELECT user_id,provider_id,service_type,payment_status,service_price,plateform_percentage,total_price FROM bookings WHERE id=%s AND user_id=%s',(job_id,session['user_id']))
#       bookingDetails = cursor.fetchone()
#    except mysql.connection.DatabaseError as e:
#       flash('something went wrong','warning')
#       print('DATABASE error while fetching booking details: {e}')
   
#    finally:
#       cursor.close()

#    # NOW UPDATE BACKEND 
#    try:
#       cursor = mysql.connection.cursor()
#       cursor.execute(' START TRANSACTION ')
#       cursor.execute(' UPDATE bookings SET payment_status = %s WHERE id =%s AND user_id = %s',(,job_id,session['user_id']))
#       customerName = session['username']
#       flash(f'Payment successfull!','success')
#       # notify provider
#       providerID = bookingDetails[1]
#       create_notifcations(providerID,job_id,f'Customer {customerName} has successfully transfered your money','chat')
      
#    except mysql.connection.DatabaseError as e:
#       mysql.connection.rollback()
#       print(f'db error while payment: {e}')
#       flash('Something went wrong','warning')

#    finally:
#       mysql.connection.commit()
#       cursor.close()

#    return redirect(url_for('dashboards_bp.user_dashboard', bookingDetails=bookingDetails))
