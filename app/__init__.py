from flask import Flask
from flask_mysqldb import MySQL
from .config import Development
from dotenv import load_dotenv
from app.utils.extensions import bcyrpt
from flask_wtf import CSRFProtect
import os

# load env
load_dotenv()

mysql = MySQL()

csrf = CSRFProtect() 

def create_app():

    # initialize Flask obj
   app = Flask(__name__)
   app.config.from_object(Development)

       # make sure SECRET_KEY exists
   if not app.config.get('SECRET_KEY'):
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

   # connect instance with app
   mysql.init_app(app) # msyql
   bcyrpt.init_app(app) # bcrypt
   csrf.init_app(app) # csrf link

   # register auths blueprint
   from app.routess.auths import auths_bp
   from app.routess.dashboards import dashboards_bp
   from app.routess.admins_panel import admins_bp

   app.register_blueprint(auths_bp)   
   app.register_blueprint(dashboards_bp)
   app.register_blueprint(admins_bp)

   return app
