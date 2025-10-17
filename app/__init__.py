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
   from app.routess.routes import auths_bp
   app.register_blueprint(auths_bp)   

   # connect instance with app
   mysql.init_app(app) # msyql
   bcyrpt.init_app(app) # bcrypt

   return app
