from flask import Flask
from flask_mysqldb import MySQL
from .config import Development
from dotenv import load_dotenv
from app.utils.extensions import bcyrpt

mysql = MySQL()

def create_app():
    # load env
   load_dotenv()
    # initialize Flask obj
   app = Flask(__name__)
   app.config.from_object(Development)


   # register auths blueprint
   from app.routess.auths import auths_bp
   from app.routess.dashboards import dashboards_bp
   from app.routess.admins_panel import admins_bp

   app.register_blueprint(auths_bp)   
   app.register_blueprint(dashboards_bp)
   app.register_blueprint(admins_bp)


   # connect instance with app
   mysql.init_app(app) # msyql
   bcyrpt.init_app(app) # bcrypt

   return app
