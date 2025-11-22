from flask_mail import Mail,Message
from flask import current_app
from flask import url_for
from app.__init__ import mysql
mail=Mail()


def init_mail(app):
    mail.init_app(app)

def sendBookingNotifications(username,service_type,proivder_mail,address,booking_date):
   # create a dashboard url for email.... 
   dashboard_url = url_for('dashboards_bp.provider_dashboard', _external=True)

   msg = Message(subject='🎯 New Booking Request - ServiConnec',
                 sender=current_app.config['MAIL_DEFAULT_SENDER'],
                 recipients=[proivder_mail]
      )

   msg.body =f'''
            You have a new booking request!
            
            Customer: {username}
            Service: {service_type}
            Address: {address}
            Date: {booking_date}
            
            Login to your dashboard to accept or decline.
            Link: {dashboard_url}
            
            - ServiConnect Team
'''
   # HTML version for clickable link
   msg.html = f'''
        <h3>🎯 New Booking Request - ServiConnect</h3>
        <p><strong>Customer:</strong> {username}</p>
        <p><strong>Service:</strong> {service_type}</p>
        <p><strong>Date:</strong> {booking_date}</p>
        <p><strong>Address:</strong> {address}</p>
        
        <p>Login to your dashboard to accept or decline:</p>
        <a href="{dashboard_url}" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
            View Dashboard
        </a>
        
        <p>- ServiConnect Team</p>
    '''   
   mail.send(msg)   



   # create notifications funtion

def create_notifcations(recipient_id,message):
    #
    cursor = mysql.connection.cursor()
    cursor.execute(' INSERT INTO notifications (recipient_id,message) VALUES(%s,%s)',(recipient_id,message))
    mysql.connection.commit()
    cursor.close()

