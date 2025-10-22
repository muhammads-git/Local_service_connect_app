from flask import redirect,render_template,url_for,session,flash,get_flashed_messages
from flask import Blueprint
from app.__init__ import mysql

# initialize Blueprints instance
dashboards_bp = Blueprint('dashboards_bp', __name__, url_prefix='/dashboard')


@dashboards_bp.route('/user')
def user_dashboard():
   if 'user_id' not in session:
      return redirect(url_for('auths_bp.user_login'))
   
   # dashboard
   cursor = mysql.connection.cursor()

   cursor.execute("""
    SELECT 
        sp.id,
        sp.username, 
        sp.profession,
        sp.profession_desc,
        ROUND(AVG(r.rating),1) as avg_rating  -- Use AVG to get single rating per provider
    FROM service_providers sp
    JOIN reviews r ON sp.id = r.provider_id
    GROUP BY sp.id, sp.username, sp.profession, sp.profession_desc
    ORDER BY avg_rating DESC
   """)
   service_providers_data = cursor.fetchall()
   cursor.close()
      
   return render_template('dashboards/user_dashboard.html',username=session['username'],service_providers_data=service_providers_data)

@dashboards_bp.route('/book_service',methods=['GET','POST'])
def book_service():
   return 'booked service'
######

@dashboards_bp.route('/provider')
def provider_dashboard():
   if 'provider_id' not in session:
      return redirect(url_for('auths_bp.provider_login'))

   return render_template('dashboards/provider_dashboard.html',provider_name=session['provider_name'])


