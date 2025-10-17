from flask import Blueprint
from flask import render_template,redirect,url_for
from app.forms.forms import User_RegisterForms,Provider_RegisterForm
from app.utils.extensions import bcyrpt
from app.__init__ import mysql


auths_bp = Blueprint('auths_bp',__name__)


@auths_bp.route('/')
def first():
   user_form = User_RegisterForms()
   return render_template('choose_registration.html',user_form=user_form)


@auths_bp.route('/user_register',methods=['POST','GET'])
def user_register():
   user_form = User_RegisterForms()
   print('I am here')

   if user_form.validate_on_submit():
      user_name =user_form.user_name.data
      user_email = user_form.user_email.data
      confirm_password = user_form.confirm_password.data

      # hash the pass before storing
      hash_password = bcyrpt.generate_password_hash(confirm_password).decode('utf-8')
      # open up db 
      cursor = mysql.connection.cursor()
      cursor.execute('INSERT INTO users (username,email,password) VALUES (%s,%s,%s)',(user_name,user_email,hash_password))
      mysql.connection.commit()
      cursor.close()
      return redirect(url_for('auths_bp.first'))
   
   return render_template('user_register.html',user_form=user_form)

@auths_bp.route('/provider_register',methods=['POST','GET'])
def provider_register():
   provider_form = Provider_RegisterForm()

   if provider_form.validate_on_submit():
      provider_name =provider_form.provider_name.data
      provider_email = provider_form.provider_email.data
      confirm_password = provider_form.confirm_password.data
      provider_profession = provider_form.profession.data
      profession_desc=provider_form.profession_desc.data
      phone = provider_form.phone.data

      # hash the password
      hash_password = bcyrpt.generate_password_hash(confirm_password).decode('utf-8')
      # db
      cursor = mysql.connection.cursor()
      cursor.execute('INSERT INTO service_providers (username,email,password,profession,profession_desc,phone) VALUES (%s,%s,%s,%s,%s,%s)',(provider_name,provider_email,confirm_password,provider_profession,profession_desc,phone))
      mysql.connection.commit()
      cursor.close()
      return redirect(url_for('auths_bp.first'))
   
   return render_template('provider_register.html',provider_form=provider_form)
   
      
      