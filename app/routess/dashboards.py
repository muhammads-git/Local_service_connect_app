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
        AVG(r.rating) as avg_rating  -- Use AVG to get single rating per provider
    FROM service_providers sp
    JOIN reviews r ON sp.id = r.provider_id
    GROUP BY sp.id, sp.username, sp.profession, sp.profession_desc
    ORDER BY avg_rating DESC
   """)
   service_providers_data = cursor.fetchall()
   cursor.close()

   # get the top rated
   cursor =mysql.connection.cursor()
   cursor.execute("""
   SELECT 
                  sp.username,
                  sp.profession,
                  CAST(AVG(r.rating) AS DECIMAL(3,1)) as avg_rating
         FROM service_providers sp
         JOIN reviews r ON sp.id = r.provider_id
         GROUP BY sp.username, sp.profession
         ORDER BY avg_rating DESC
         LIMIT 1
   """)
   top_rated = cursor.fetchall()



   return render_template('dashboards/user_dashboard.html',username=session['username'],service_providers_data=service_providers_data,top_rated=top_rated)

@dashboards_bp.route('/book_service',methods=['GET','POST'])
def book_service():
   return 'booked service'
######

@dashboards_bp.route('/provider')
def provider_dashboard():
   if 'provider_id' not in session:
      return redirect(url_for('auths_bp.provider_login'))

   return render_template('dashboards/provider_dashboard.html',provider_name=session['provider_name'])


