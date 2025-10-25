from flask import redirect,render_template,url_for,session,flash,get_flashed_messages
from flask import Blueprint
from app.__init__ import mysql
from app.forms.forms import BookingForm
from app.utils.mail import sendBookingNotifications

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

@dashboards_bp.route('/book_service/<int:provider_id>', methods=['GET','POST'])
def book_service(provider_id):
    booking_form = BookingForm()
    
    # Get provider data
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT username, profession, email FROM service_providers WHERE id=%s', (provider_id,))
    provider_data = cursor.fetchone()
    cursor.close()
    
    provider_name = provider_data[0]
    provider_profession = provider_data[1]
    provider_email = provider_data[2]  # Get email here

    # Handle form submission
    if booking_form.validate_on_submit():
        # Set provider_id in form
        booking_form.provider_id.data = provider_id
        
        # Save to database
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO bookings (user_id, provider_id, status, address, service_description, service_date) 
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (
            session['user_id'], 
            provider_id, 
            'pending',
            booking_form.address.data,
            booking_form.description.data, 
            booking_form.date_time.data
        ))
        mysql.connection.commit()
        cursor.close()

        # Send notification
        sendBookingNotifications(
            # provider_mail=provider_email, # removing this parameter for now
            username=session['username'],
            service_type=booking_form.service_type.data,
            proivder_mail=provider_email,
            address=booking_form.address.data,
            booking_date=booking_form.date_time.data
        )

        flash('Booking request sent! You will get response soon.', 'success')
        return redirect(url_for('dashboards_bp.user_dashboard'))

    return render_template('dashboards/booking_form.html', 
                        booking_form=booking_form,
                        provider_id=provider_id,
                        provider_name=provider_name,
                        provider_profession=provider_profession)

@dashboards_bp.route('/provider')
def provider_dashboard():
   if 'provider_id' not in session:
      return redirect(url_for('auths_bp.provider_login'))
   
   # start working on tiny logics, 
   # total bookings
   cursor = mysql.connection.cursor()
   cursor.execute('SELECT COUNT(*) FROM bookings WHERE provider_id= %s ',(session['provider_id'],))
   total_bookings = cursor.fetchone()[0]
   cursor.close()

   ## completed jobs/bookings
   cursor = mysql.connection.cursor()
   cursor.execute('''SELECT COUNT(*) FROM bookings WHERE provider_id =%s AND status = %s'''
                  ,(session['provider_id'],'completed'))
   completed_jobs = cursor.fetchone()[0]
   cursor.close()

   # pending jobs/bookings
   cursor = mysql.connection.cursor()
   cursor.execute(''' SELECT COUNT(*) FROM bookings WHERE provider_id = %s AND status = %s''',
                  (session['provider_id'],'pending'))
   pending_jobs = cursor.fetchone()[0]
   cursor.close()

   # average rating
   cursor = mysql.connection.cursor()
   cursor.execute(''' SELECT AVG(rating) FROM reviews WHERE provider_id = %s''',(session['provider_id'],))
   raw_rating = cursor.fetchone()[0]   # will return like 4.4433
   cursor.close()
   print(raw_rating)
   # we need round off figures
   rounded_rating = round(raw_rating,1)  # round off 

   return render_template('dashboards/provider_dashboard.html',provider_name=session['provider_name'],total_bookings=total_bookings,completed_jobs=completed_jobs,pending_jobs=pending_jobs,rounded_rating=rounded_rating)



