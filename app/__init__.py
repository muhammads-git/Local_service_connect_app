from flask import Flask,g,render_template,redirect,session,url_for
from flask_mysqldb import MySQL
from flask_wtf import CSRFProtect
from dotenv import load_dotenv
import os
from datetime import timedelta

# Load .env once at the top
load_dotenv()

mysql = MySQL()
csrf = CSRFProtect() 

app = Flask(__name__)

@app.before_request
def notifications():
   # look for notificatons
      # notifications logic, when provider accepts notification it comes to db 
   # we need to fetch notification table data , messages to see if there is any
   # so we can show to user in dashboards
   if 'user_id' in session:
      cursor = mysql.connection.cursor()
      
      cursor.execute(' SELECT id, message, created_at, is_read FROM notifications WHERE user_id =%s ORDER by created_at DESC',(session['user_id'],))
      notifications = cursor.fetchall()
      cursor.close()

      # count unread
      # count_notifications = sum(1 for notification in notifications)
      count = 0
      for notification in notifications:
      #    notification[0] == message
      # 1 == created at 
      # 2 == is_read which will be 0 default
         if notification[3] == 0:
               count += 1

      unread_count = count

      # make available for all the routes
      g.unread_count = unread_count
      g.notifications = notifications
   
   else:
       g.unread_count = 0
       g.notifications = []


# creating app
def create_app():
    
    # Simple direct config - no separate config file
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    # Session 
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'serviconnect')
    
    # Mail config
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'Ibuild@serviconnect.com')

    # Initialize extensions
    mysql.init_app(app)
    csrf.init_app(app)
    
    # Initialize mail
    from app.utils.mail import init_mail
    init_mail(app)
    
    # Register blueprints
    from app.routess.auths import auths_bp
    from app.routess.dashboards import dashboards_bp
    from app.routess.admins_panel import admins_bp

    app.register_blueprint(auths_bp)   
    app.register_blueprint(dashboards_bp)
    app.register_blueprint(admins_bp)

    return app