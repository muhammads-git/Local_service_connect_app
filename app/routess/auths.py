from flask import Blueprint
from flask import render_template,redirect,url_for,session,flash,get_flashed_messages, request
from app.forms.forms import User_RegisterForms,Provider_RegisterForm,User_LoginForm,Provider_LoginForm,CompleteProfileForm
from app.utils.extensions import bcyrpt
from app.__init__ import mysql

auths_bp = Blueprint('auths_bp', __name__)

### checking web work

@auths_bp.route('/debug')
def debug():
    print("Headers:", dict(request.headers))
    print("Args:", dict(request.args))
    print("Form:", dict(request.form))
    return "Check your console!"


@auths_bp.route('/')
def first():
   user_form = User_RegisterForms()
   return render_template('choose_registration.html',user_form=user_form)


@auths_bp.route('/user_register',methods=['GET','POST'])
def user_register():
   user_form = User_RegisterForms()

   if user_form.validate_on_submit():
      user_name =user_form.user_name.data
      user_email = user_form.user_email.data
      user_phone = user_form.user_phone.data
      confirm_password = user_form.confirm_password.data

      # hash the pass before storing
      hash_password = bcyrpt.generate_password_hash(confirm_password).decode('utf-8')
      # open up db 
      cursor = mysql.connection.cursor()
      cursor.execute('INSERT INTO users (username,email,phone,password) VALUES (%s,%s,%s,%s)',(user_name,user_email,user_phone,hash_password))
      mysql.connection.commit()
      cursor.close()

      flash("Successfully registered as a user.","success")
      return redirect(url_for('auths_bp.user_login'))
   
   return render_template('auths/user_register.html',user_form=user_form)

@auths_bp.route('/provider_register',methods=['GET','POST'])
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
      cursor.execute('INSERT INTO service_providers (username,email,password,profession,profession_desc,phone) VALUES (%s,%s,%s,%s,%s,%s)',(provider_name,provider_email,hash_password,provider_profession,profession_desc,phone))
      mysql.connection.commit()
      cursor.close()
      flash("Successfully registered as a provider.","success")
      return redirect(url_for('auths_bp.provider_login'))
   
   return render_template('auths/provider_register.html',provider_form=provider_form)


# login routes
@auths_bp.route('/user_login',methods=['POST','GET'])
def user_login():
   
   if 'user_id' in session:
      return redirect(url_for('dashboards_bp.user_dashboard'))
   
   user_form = User_LoginForm()
   
   if user_form.validate_on_submit():
      user_name = user_form.user_name.data
      user_password = user_form.user_password.data
   
      # fetch the name from db then compare password if ==
      cursor = mysql.connection.cursor()
      cursor.execute('SELECT * FROM users WHERE username =%s',(user_name,))
      user = cursor.fetchone()
      cursor.close()

      # if 
      if user:
         hash_password = user[3] # index 3 means col 3 is passwords col
         if bcyrpt.check_password_hash(hash_password,user_password):
            session['user_id'] = user[0]  # create session 
            session['username'] = user[1]
            session['role'] = 'user' # save the role for later differences
            # flash
            flash('Successfully logged In!','success')
            return redirect(url_for('dashboards_bp.user_dashboard'))  # pending....
         
    # if the req is GET show the page
   return render_template('auths/user_login.html',user_form=user_form)


# user loguot
@auths_bp.route('/logout')
def logout():
   
   if session.get('role') == 'user':
      session.clear()
      return redirect(url_for('auths_bp.user_login'))
   elif session.get('role') == 'provider':
      session.clear()
      return redirect(url_for('auths_bp.provider_login'))
   else:
      session.clear()
      return redirect(url_for('admins_bp.admin_login'))


@auths_bp.route('/provider_login',methods=['POST','GET'])
def provider_login():
   provider_form = Provider_LoginForm()

   if provider_form.validate_on_submit():
      provider_name = provider_form.provider_name.data
      provider_password = provider_form.provider_password.data

      # open db
      cursor = mysql.connection.cursor()
      cursor.execute('SELECT * FROM service_providers WHERE username = %s',(provider_name,))
      provider = cursor.fetchone()
      cursor.close()

      # check if data available
      if provider:
         hash_password=provider[3] # col 3 is passwords col
         if bcyrpt.check_password_hash(hash_password,provider_password):
            session['provider_id'] = provider[0]
            session['provider_name'] = provider[1]
            session['role'] = 'provider' 

            flash('Successfully logged In!','success')
            return redirect(url_for('dashboards_bp.provider_dashboard'))
   # if req is GET show the page
   return render_template('auths/provider_login.html',provider_form=provider_form)



# complete profile
@auths_bp.route('/complete_profile',methods=['POST','GET'])
def complete_profile():
   profile_form = CompleteProfileForm()      
   if profile_form.validate_on_submit():
      address= profile_form.address.data

      try:
      # db
         cursor = mysql.connection.cursor()
         cursor.execute('UPDATE users SET address = %s WHERE id = %s',(address,session['user_id']))
         mysql.connection.commit()
         cursor.close()

         # flash
         flash('Your profile is completed!','success')
         # redirect to user dashboard
         return redirect(url_for('dashboards_bp.user_dashboard'))
      
      except Exception as e:
         mysql.connection.rollback()
         flash('Error Updating profile','warning')
         return redirect(url_for('auths_bp.complete_profile'))

   # get
   return render_template('auths/complete_profile_form.html',profile_form=profile_form)
