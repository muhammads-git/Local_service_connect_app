from flask import redirect,render_template,url_for,session,flash,get_flashed_messages,request
from flask import Blueprint
from app.__init__ import mysql
from app.forms.forms import BookingForm,BookServiceForm
from app.utils.mail import sendBookingNotifications
from app.utils.mail import create_notifcations
# initialize Blueprints instance
dashboards_bp = Blueprint('dashboards_bp', __name__, url_prefix='/dashboard')

@dashboards_bp.route('/user')
def user_dashboard():
   if 'user_id' not in session:
      return redirect(url_for('auths_bp.user_login'))
   
   # Fetching provider data for user dashboard
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
    
    # fectching users total bookings
   cursor = mysql.connection.cursor()
   cursor.execute('SELECT COUNT(*) FROM bookings WHERE user_id = %s',(session['user_id'],))
   
    # total bookings this user booked
   all_bookings = cursor.fetchone()[0]
   print(all_bookings)
   cursor.close()

   
   return render_template('dashboards/user_dashboard.html',username=session['username'],service_providers_data=service_providers_data,all_bookings=all_bookings)

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


#### Request a service 
@dashboards_bp.route('/request_a_service',methods=['POST','GET'])
def request_a_service():
    request_service_form = BookServiceForm()

    if request_service_form.validate_on_submit():
        type  = request_service_form.service_type.data
        description = request_service_form.service_description.data
        
        # fetch user data if profile is complete
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT address FROM users where id = %s',(session['user_id'],))
        user_adress = cursor.fetchone()[0]
        cursor.close()

        # check if user address is not null
        if user_adress is not None:
            # db 
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO bookings (user_id,status,service_type,service_description) VALUES (%s,%s,%s,%s)', (session['user_id'],'pending',type,description))
            mysql.connection.commit()
            cursor.close()

            # flash message
            flash('Service request has been sent, You will get provider soon!','success')
            return redirect(url_for('dashboards_bp.request_a_service'))
        else:
            flash('Complete your profile before submitting service form','warning')
            # url
            return redirect(url_for('auths_bp.complete_profile'))
        
    # GET
    return render_template('dashboards/bookservice_form.html',request_service_form=request_service_form)
        
    
@dashboards_bp.route('/provider')
def provider_dashboard():
   # if provider not in session...
   if 'provider_id' not in session:
      return redirect(url_for('auths_bp.provider_login'))
   
   # dashboard data....
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

    # edge cases
   if raw_rating is None:
       rounded_rating = str(0.0)
   else:       # we need round off figures
        rounded_rating = round(raw_rating,1)  # round off 


   # handle RECENT BOOKINGS...
   cursor = mysql.connection.cursor()

   cursor.execute("""
             SELECT u.username AS customer_name,b.service_description, b.created_at ,b.status,b.id FROM users u JOIN bookings b ON u.id = b.user_id WHERE b.provider_id = %s
             ORDER BY b.id DESC   """,
                  (session['provider_id'],))
   
   recent_bookings = cursor.fetchall()
   cursor.close()

   #completion rate 
   # total booking provider got
   cursor = mysql.connection.cursor()
   cursor.execute('SELECT COUNT(*) FROM bookings WHERE provider_id = %s',(session['provider_id'],))
   total_bookings_data = cursor.fetchone()[0]
   cursor.close()

   # completed bookingss out of total
   cursor = mysql.connection.cursor()
   cursor.execute('SELECT COUNT(*) FROM bookings WHERE provider_id =%s AND status = %s',(session['provider_id'],('completed')))
   completed_bookings = cursor.fetchone()[0]

   

   # complettion rate logic
   if completed_bookings:
        # percentage formula
        completion_rate = (completed_bookings / total_bookings_data * 100) 
        # if true  
        round_off_completions = round(completion_rate,2)
   else:
       completion_rate = str(0.0)
       round_off_completions = completion_rate


   return render_template('dashboards/provider_dashboard.html',provider_name=session['provider_name'],total_bookings=total_bookings,completed_jobs=completed_jobs,pending_jobs=pending_jobs,rounded_rating=rounded_rating,recent_bookings=recent_bookings,round_off_completions=round_off_completions)


@dashboards_bp.route('/accept_booking/<int:booking_id>',methods=['POST','GET'])
def accept_booking(booking_id):
   # change the status
   try:
        cursor  = mysql.connection.cursor()
        cursor.execute("""
                        UPDATE bookings SET status = 'accepted' WHERE id =%s AND provider_id =%s                
                        """,(booking_id,session['provider_id']))
        
        mysql.connection.commit()
        cursor.close()
        
        # flash message/ pop up
        flash('Booking accepted','success')
        return redirect(url_for('dashboards_bp.provider_dashboard'))
        
   except Exception as e:
        flash('Error Occured','warning')
        return redirect(url_for('dashboards_bp.provider_dashboard'))
   

@dashboards_bp.route('/reject_booking/<int:booking_id>',methods=['POST','GET'])
def reject_booking(booking_id):
    # 
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE bookings SET status ="rejected" WHERE id =%s AND provider_id = %s',(booking_id,session['provider_id']) )
        mysql.connection.commit()
        cursor.close()

        # pop up
        flash('Booking rejected','danger')
        return redirect(url_for('dashboards_bp.provider_dashboard'))

    except Exception as e:
       flash('Error Occured','warning')
       return redirect(url_for('dashboards_bp.provider_dashboard'))
    
### available jobs/bookings
@dashboards_bp.route('/available_jobs',methods=['GET'])
def available_jobs():
    # think .............
    cursor = mysql.connection.cursor()
    cursor.execute(' SELECT b.id, u.username, b.service_description, b.status FROM users u JOIN bookings b ON u.id = b.user_id WHERE b.status ="pending" ')
    available_jobs_data = cursor.fetchall()
    cursor.close()

    # if users clicks view job
    selected_job_id = request.args.get('view_jobs')
    selected_job = None

    if selected_job_id:
        selected_job = get_view_jobs_id(selected_job_id)



    return render_template('dashboards/available_jobs.html',available_jobs_data=available_jobs_data,selected_job_id=selected_job_id,selected_job=selected_job)

# get view_jobs id
def get_view_jobs_id(job_id):
    # get selected job data from db
    cursor = mysql.connection.cursor()
    cursor.execute(' SELECT b.id, u.username, b.service_description, b.status, b.service_date, b.address FROM users u JOIN bookings b ON u.id =b.user_id WHERE b.id = %s AND b.status =%s',(job_id,'pending'))
    selected_job_data = cursor.fetchone()
    cursor.close()

    return selected_job_data

# accept job ruoute
@dashboards_bp.route('/accept_job/<int:job_id>',methods=['GET'])
def accept_job(job_id):
    # check if job is available
    cursor = mysql.connection.cursor()
    cursor.execute(' SELECT status FROM bookings WHERE id = %s',(job_id,))
    _available = cursor.fetchone()
    cursor.close()

    # edge case
    if _available == 'accepted':
        flash('Job has already been accepted by another PROVIDER','warning')
        return redirect(url_for('dashboards_bp.available_jobs'))
    

    # get provider id from session
    provider_id = session.get('provider_id')
    # handle update booking
    cursor = mysql.connection.cursor()
    cursor.execute(' UPDATE bookings SET status ="accepted", provider_id = %s WHERE id = %s ',(provider_id,job_id,))
    mysql.connection.commit()
    cursor.close()

    flash('Booking has been accepted, Cutomer has been notified!','success')

    # connect flash
    flash('You can now connect to Customer','success')

    # get user this booking belongs
    cursor = mysql.connection.cursor()
    cursor.execute(' SELECT user_id FROM bookings WHERE id = %s',(job_id,))
    customer_id = cursor.fetchone()[0]

    # send notification to user
    create_notifcations(customer_id,'Great News! A provider accepted your request.')

    return redirect(url_for('dashboards_bp.available_jobs'))




# @dashboards_bp.route('/reject_job/int:job_id')
# def reject_job(job_id):

#     cursor = mysql.connection.cursor()
#     cursor.execute(' UPDATE bookings SET status ="accepted" WHERE id = %s ',(job_id))
#     mysql.connection.commit()
#     cursor.close()

#     # Flash for your side
#     flash('Booking Rejected','warning')

#     # now notfiy users that booking is rejected

#     return 'Rejected'