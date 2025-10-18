from flask import redirect,render_template,url_for,session,flash,get_flashed_messages
from flask import Blueprint

# initialize Blueprints instance
dashboards_bp = Blueprint('dashboards_bp', __name__, url_prefix='/dashboard')


@dashboards_bp.route('/user')
def user_dashboard():
   if 'user_id' not in session:
      return redirect(url_for('auths_bp.user_login'))
   
   return render_template('dashboards/user_dashboard.html',username=session['username'])


@dashboards_bp.route('/provider')
def provider_dashboard():
   if 'provider_id' not in session:
      return redirect(url_for('auths_bp.provider_login'))

   return render_template('dashboards/provider_dashboard.html',provider_name=session['provider_name'])


