from flask import Flask,g,render_template,redirect,session,url_for,flash,request,jsonify
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
def fetch_notifications():    
   if 'user_id' in session or 'provider_id' in session:
      cursor = mysql.connection.cursor()
      # User or Provider
      recipient_id = session.get('user_id') or session.get('provider_id')
      
      try:
         cursor.execute(""" SELECT
            job_id,  
            COUNT(*) as message_count, 
            MAX(created_at) as latest_time, 
            GROUP_CONCAT(message SEPARATOR ' | ') as messages_combined,
            MIN(is_read) as unread
            FROM notifications 
            WHERE recipient_id = %s 
            GROUP BY job_id
            ORDER BY latest_time DESC """ ,(recipient_id,))
         notifications = cursor.fetchall()

      except Exception as e:
         flash(f"error {e} occured, try again!",'warning')

      if not notifications:
         notifications = 0   #default   
      unread_count = sum(1 for note in notifications if note[4] == 0)

      # make available for all the routes
      g.unread_count = unread_count
      g.notifications = notifications                  

# creating app
def create_app():
    
    # Simple direct config - no separate config file
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    # Session 
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
    # disabling CSRF protection for apis
   #  app.config['WTF_CSRF_CHECK_DEFAULT'] = False

   #  app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
   #  app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
   #  app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
   #  app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'serviconnect')
      # NEW WAY (Using Railway's injected variables)
   # ✅ NEW CODE (Connects to Railway cloud)

    app.config['MYSQL_HOST'] = os.getenv('DB_HOST', 'switchyard.proxy.rlwy.net')
    app.config['MYSQL_PORT'] = int(os.getenv('DB_PORT', 49423))  # CRITICAL: Add this line
    app.config['MYSQL_USER'] = os.getenv('DB_USER', 'root')
    app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD', 'JkBFoZOTIMdAUzpoXhsbrftfHyHmasvX')
    app.config['MYSQL_DB'] = os.getenv('DB_NAME', 'railway')
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
    # api rout testing.......
    from app.routess.api.api_routes import api_bp

    app.register_blueprint(auths_bp)   
    app.register_blueprint(dashboards_bp)
    app.register_blueprint(admins_bp)
    app.register_blueprint(api_bp) # for testing.....
   
   # apply csrf protections to all blueprints except apisss
    csrf.exempt(api_bp)

    return app