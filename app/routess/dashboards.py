from flask import redirect,render_template,url_for,session,flash,get_flashed_messages
from flask import Blueprint
from app.__init__ import mysql
from app.forms.forms import BookingForm

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

@dashboards_bp.route('/book_service/<int:provider_id>',methods=['GET','POST'])
def book_service(provider_id):
   booking_form = BookingForm()

   # get proivder data
   cursor = mysql.connection.cursor()
   cursor.execute('SELECT username, profession FROM service_providers WHERE id=%s',(provider_id,))
   provider_data = cursor.fetchone()
   cursor.close()
   print(provider_data)
   # get the name and profession
   provider_name = provider_data[0]
   provider_profession = provider_data[1]

   # form data and 
   if booking_form.validate_on_submit():

      cursor= mysql.connection.cursor()
      cursor.execute('INSERT INTO bookings (user_id,provider_id,status,address,service_description,service_data) VALUES (%s,%s,%s,%s,%s,%s)',(session['user_id',provider_id,booking_form.address.data,booking_form.description.data,booking_form.date_time.data]))
      mysql.connection.commit()
      cursor.close()

      flash('Booking request sent!','success')
      return redirect(url_for('dashboards_bp.user_dashboard'))

   return render_template('dashboards/booking_form.html',booking_form=booking_form,provider_id=provider_id,provider_name=provider_name,provider_profession=provider_profession)

#
@dashboards_bp.route('/create_booking',methods=['GET','POST'])
def create_booking():
   return 'in making....'


@dashboards_bp.route('/provider')
def provider_dashboard():
   if 'provider_id' not in session:
      return redirect(url_for('auths_bp.provider_login'))

   return render_template('dashboards/provider_dashboard.html',provider_name=session['provider_name'])


