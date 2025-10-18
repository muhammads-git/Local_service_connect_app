from flask import render_template, redirect, session, url_for, request, flash
from flask import Blueprint
from dotenv import load_dotenv
import os
from app.forms.forms import Admin_LoginForm
from app.utils.extensions import bcyrpt
from app.__init__ import mysql
from app.utils.decorator import admin_required  # import the guard

# load environment variables
load_dotenv()

admins_bp = Blueprint('admins_bp', __name__, url_prefix='/admins')

@admins_bp.route('/admin_login', methods=['POST', 'GET'])
def admin_login():
    admin_form = Admin_LoginForm()

    if admin_form.validate_on_submit():
        username = admin_form.username.data
        email = admin_form.email.data
        password = admin_form.password.data
        secret_key = admin_form.secret_key.data

        # verify secret key
        if secret_key != os.getenv('ADMIN_SECRET_KEY'):
            flash("Unauthorized secret key!", "danger")
            return redirect(url_for('admins_bp.admin_login'))

        # database check
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM admins WHERE username=%s', (username,))
        admin = cursor.fetchone()
        cursor.close()

        if admin and bcyrpt.check_password_hash(admin[3], password):
            session['admin_id'] = admin[0]
            session['role'] = 'admin'
            session['admin_name'] = admin[1]
            flash('Welcome Admin!', 'success')
            return redirect(url_for('admins_bp.admin_dashboard'))

        flash('Invalid credentials', 'warning')

    return render_template('admins/admin_login.html', admin_form=admin_form)


@admins_bp.route('/admin_dashboard')
@admin_required  # 👈 one line = full protection
def admin_dashboard():
    # fetch user and provider counts
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM service_providers')
    total_providers = cursor.fetchone()[0]
    cursor.close()

    return render_template(
        'admins/admin_dashboard.html',
        total_users=total_users,
        total_providers=total_providers,
        admin_name=session.get('admin_name')
    )
