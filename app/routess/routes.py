from flask import Blueprint
from flask import render_template,redirect,url_for

auths_bp = Blueprint('auths_bp',__name__)


@auths_bp.route('/')
def first():
   return redirect(url_for('auths_bp.register'))


@auths_bp.route('/register',methods=['GET'])
def register():
   return 'Register as User or Service Provider!'