from flask import Flask
from flask_mysqldb import MySQL
from .config import Development
from dotenv import load_dotenv
from app.routess.routes import auths_bp
mysql = MySQL()

def create_app():
    # load env
   load_dotenv()
    # initialize Flask obj
   app = Flask(__name__)
   app.config.from_object(Development)

   # register auths blueprint
   app.register_blueprint(auths_bp)   

   mysql.init_app(app)

   return app
