from flask import render_template,redirect,session,url_for,request,flash,get_flashed_messages
from flask import Blueprint
from dotenv import load_dotenv
import os
from app.forms.forms import Admin_LoginForm
from app.utils.extensions import bcyrpt
from app.__init__ import mysql
# load environmnet variables
load_dotenv()

admins_bp = Blueprint('admins_bp',__name__,url_prefix='/admins')


@admins_bp.route('/admin_login',methods=['POST','GET'])
def admin_login():
   # initialize 
   admin_form = Admin_LoginForm()
   if admin_form.validate_on_submit():
      username = admin_form.username.data
      email = admin_form.email.data
      password = admin_form.password.data
      secret_key = admin_form.secret_key.data

      # check secret key
      if secret_key != os.getenv('ADMIN_SECRET_KEY'):
         flash("Unauthorized secret key!", "danger")
         return redirect(url_for('admins_bp.admin_login'))
      
      # db store
      cursor = mysql.connection.cursor()
      cursor.execute('SELECT * FROM admins WHERE username=%s',(username,))
      admin = cursor.fetchone()
      cursor.close()

      # check
      if admin and bcyrpt.check_password_hash(admin[3],password):
         session['admin_id'] = admin[0]
         session['role'] = 'admin'
         session['admin_name'] = admin[1]
         # success message
         flash('Welcome Admin!','success')
         return redirect(url_for('admins_bp.admin_dashboard'))
      
      flash('Invalid Credentials','warning')
   
   return render_template('admins/admin_login.html', admin_form=admin_form)



@admins_bp.route('/admin_dashboard',methods=['GET','POST'])
def admin_dashboard():
   # check if the user is admin or 
   secret_key = os.getenv('ADMIN_SECRET_KEY')
   if session.get('role') != 'admin' or not session.get('admin_id'):
      flash('Access denied','danger')
      return redirect(url_for('admins_bp.admins_login'))
   

   # fetch the users
   cursor = mysql.connection.cursor()
   cursor.execute('SELECT COUNT(*) FROM users')
   total_users= cursor.fetchone()[0]
   cursor.close()

   # fetch the service providers
   cursor = mysql.connection.cursor()
   cursor.execute('SELECT COUNT(*) FROM service_providers')
   total_providers= cursor.fetchone()[0]
   cursor.close()

   return render_template('admins/admin_dashboard.html',total_users=total_users,total_providers=total_providers)
      

