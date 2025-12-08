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
   cursor.close()
   
   return render_template('dashboards/user_dashboard.html',username=session['username'],service_providers_data=service_providers_data,all_bookings=all_bookings)

## start chat user
@dashboards_bp.route('/start_chat/<int:job_id>',methods=['GET'])
def start_chat(job_id):
    
    # if job_id:
    #     # get provider id from bookings 
    #     cursor = mysql.connection.cursor()
    #     cursor.execute('SELECT provider_id FROM bookings WHERE id = %s', (job_id,))
    #     booking = cursor.fetchone()
    # else:
    #     flash(f'{job_id} error!','warning')

    # if booking[0] is None:
    #     flash('Cannot start a chat, no provider is assigned to this job','info')
    #     return redirect(url_for('dashboards_bp.user_dashboard'))
    
    # receiver_id = booking[0] 

    # # get user id from session
    # sender_id = session.get('user_id')
    # # 
    # # insert into table
    # cursor = mysql.connection.cursor()
    # cursor.execute(' INSERT INTO messages (receiver_id,sender_id,job_id,message) VALUES(%s,%s,%s,%s)',
    #                (receiver_id,sender_id,job_id,'Hello, Lets discuss this job'))
    
    # flash('Message sent!','info')
    # get customer name
    # customer_name = session.get('username')
    # create notification for user
    # create_notifcations(receiver_id,f'New message from {customer_name}!')

    return redirect(url_for('dashboards_bp.user_chat_box', job_id=job_id)) # chat boxxxxx pending

@dashboards_bp.route('/user_chat_box/<int:job_id>',methods=['GET'])
def user_chat_box(job_id):
    # get sender_id
    user_id = session.get('user_id')

    # get job_id
    # job_id = session.get('last_job')
    print(job_id)

    cursor = mysql.connection.cursor()
    cursor.execute(' SELECT sender_id,message,created_at,is_read FROM messages WHERE job_id = %s ORDER BY created_at ASC',(job_id,)) 
    messages = cursor.fetchall()
    cursor.close()

    # mark as read the messages 
    cursor = mysql.connection.cursor()
    cursor.execute(' UPDATE messages SET is_read = TRUE WHERE job_id=%s AND receiver_id = %s',(job_id,user_id))
    mysql.connection.commit()
    cursor.close()

    return render_template('dashboards/user_chat_box.html',messages=messages,job_id=job_id,user_id=user_id)

# send message 
@dashboards_bp.route('/send_message',methods=["POST"])
def send_messages():
    user_id = session.get('user_id')
    # job_id = session.get('last_job')
    job_id = request.form.get('job_id')
    message_text = request.form['message']

    # get provider id for this chat 
    cursor = mysql.connection.cursor()
    cursor.execute(' SELECT provider_id FROM bookings WHERE id = %s',(job_id,))
    provider_id = cursor.fetchone()
    
    # case
    if not provider_id or provider_id[0] is None:
        flash('Cannot send message, No provider assigned to this job','info')
        return redirect(url_for('dashboards_bp.user_dashboard'))
    
    try:
        # insert into messages
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO messages (receiver_id,sender_id,job_id,message) VALUES(%s,%s,%s,%s) ',(provider_id[0],user_id,job_id,message_text,))
        mysql.connection.commit()
        cursor.close()
        # flash
        flash('Sent!','success')
        # create notification for provider
        create_notifcations(provider_id[0],job_id,'New message')

    except Exception as e:
        flash(f'Error {e} sending message, try again!','danger')
    
    # handle routes redirect to chat box
    return redirect(url_for('dashboards_bp.user_chat_box',job_id=job_id))

# my chats route
@dashboards_bp.route('/myChats',methods=['GET'])
def myChats():
    if 'user_id' not in session:
        return redirect(url_for('auths_bp.user_login'))
    
    user_id = session.get('user_id')

    # get chats 
    cursor = mysql.connection.cursor()
    cursor.execute(
        'SELECT DISTINCT job_id FROM messages WHERE receiver_id = %s OR sender_id = %s'
    ,(user_id,user_id))
    chats_job = cursor.fetchall()
    
    return render_template('dashboards/my_chats.html',chats_job=chats_job)

# mark as read single notification
@dashboards_bp.route('/mark_as_read_single/<int:notification_id>',methods=['POST'])
def mark_as_read_single(notification_id):
    if 'user_id' not in session:
        return redirect(url_for('auths_bp.user_login'))
    
    cursor = mysql.connection.cursor()
    cursor.execute(' UPDATE notifications SET is_read = TRUE WHERE id =%s AND recipient_id =%s',(notification_id,session['user_id']))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('dashboards_bp.user_dashboard'))

# mark as read all
@dashboards_bp.route('/mark_all_asread',methods=['POST'])
def mark_all_asread():
    if 'user_id' not in session:
        return redirect(url_for('auths_bp.user_login'))
    
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE notifications SET is_read = TRUE WHERE recipient_id = %s',(session['user_id'],))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('dashboards_bp.user_dashboard'))

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
            cursor.execute('INSERT INTO bookings (user_id,status,service_type,service_description) VALUES (%s,%s,%s,%s)', (session['user_id'],'available',type,description))
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
    cursor.execute(' SELECT b.id, u.username, b.service_description, b.status FROM users u JOIN bookings b ON u.id = b.user_id WHERE b.status ="available" ORDER BY b.id DESC')
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
    cursor.execute(' SELECT b.id, u.username, b.service_description, b.status, b.service_date, b.address FROM users u JOIN bookings b ON u.id =b.user_id WHERE b.id = %s AND b.status =%s',(job_id,'available'))
    selected_job_data = cursor.fetchone()
    cursor.close()

    return selected_job_data

# accept job ruoute
@dashboards_bp.route('/accept_job/<int:job_id>',methods=['POST'])
def accept_job(job_id):
    # // save the job_id in sessions
    session['last_job'] = job_id
    # // modify
    session.modified = True

    if 'provider_id' not in session:
        return redirect(url_for('auths_bp.provider_login'))
        
    # get provider id from session
    provider_id = session.get('provider_id')
    # handle update booking
    cursor = mysql.connection.cursor()
    cursor.execute(' UPDATE bookings SET status ="accepted", provider_id = %s WHERE id = %s AND status = %s ',(provider_id,job_id,'available'))
    mysql.connection.commit()
    cursor.close()
    flash('Booking has been accepted!','success')


    # get userid to send him a notifications
    cursor = mysql.connection.cursor()
    cursor.execute(' SELECT user_id FROM bookings WHERE id = %s',(job_id,))
    customer_id = cursor.fetchone()[0]
    # provider name 
    provider_name = session.get('provider_name')

    # send notification to user
    create_notifcations(customer_id,job_id,f'A Provider {provider_name} accepted your request.')

    return redirect(url_for('dashboards_bp.provider_chat_box',job_id=job_id))

## PROVIDER CHAT SYSTEM 
@dashboards_bp.route('/provider_chat_box/<int:job_id>',methods=['GET'])
def provider_chat_box(job_id):
    if 'provider_id' not in session:
        return redirect(url_for('auths_bp.provider_login'))
    
    # get provider id
    receiver_id = session.get('provider_id')
    # get job_id
    # job_id = session.get('last_job')
# 
    # fetch messages from table messages to show in chat box
    cursor = mysql.connection.cursor()
    cursor.execute(' SELECT sender_id,message,created_at,is_read FROM messages WHERE job_id=%s',(job_id,))
    messages = cursor.fetchall()
    cursor.close()

    # update messages to TRUE
    cursor = mysql.connection.cursor()
    cursor.execute(' UPDATE messages SET is_read = TRUE WHERE job_id=%s AND receiver_id = %s',(job_id,receiver_id))
    mysql.connection.commit()
    cursor.close()
    
    return render_template('dashboards/provider_chat_box.html', messages=messages,job_id=job_id,receiver_id=receiver_id)  # receiver is provider soo ==

# send message route
@dashboards_bp.route('/provider_send_messages',methods=['POST'])
def provider_send_messages():
    # provider id , job_id, message 
    provider_id = session.get('provider_id')
    # // get job id from session
    # job_id = session.get('last_job')
    job_id = request.form.get('job_id')
    # // get message from url <form></form>
    message_text = request.form['message']

    # get user id from bookings table 
    cursor = mysql.connection.cursor()
    cursor.execute(' SELECT user_id FROM bookings WHERE id=%s',(job_id,))
    user_id = cursor.fetchone()[0]

    try:
        # insert into messages
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO messages (receiver_id,sender_id,job_id,message) VALUES(%s,%s,%s,%s)',(user_id,provider_id,job_id,message_text))
        mysql.connection.commit()
        cursor.close()
        flash('Sent!','success')
        # create notification
        create_notifcations(user_id,job_id,'New Message!')
        
    except Exception as e:
        flash(f'Error {e} while sending this message','danger')
        print('Error insertingggg.....')

    # handle route 
    return redirect(url_for('dashboards_bp.provider_chat_box'))

## mark all as read 
@dashboards_bp.route('/provider_mark_all_read',methods=['POST'])
def provider_mark_all_read():
    # the notification provider got
    if 'provider_id' not in session:
        flash('login required!','warning')
        return redirect(url_for('auths_bp.provider_login'))
    cursor = mysql.connection.cursor()
    cursor.execute(' UPDATE notifications SET is_read = TRUE WHERE recipient_id =%s',(session['provider_id'],))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('dashboards_bp.provider_dashboard'))

@dashboards_bp.route('/provider_mark_one_read<int:notification_id>',methods=['POST'])
def provider_mark_one_read(notification_id):
    if 'provider_id' not in session:
        flash('Login required!','warning')
    
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE notifications SET is_read = TRUE WHERE id = %s AND recipient_id = %s',(notification_id,session['provider_id']))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('dashboards_bp.provider_dashboard'))

@dashboards_bp.route('/provider_start_chat/<int:job_id>', methods=["GET"])
def provider_start_chat(job_id):
    if 'provider_id' not in session:
        return redirect(url_for('auths_bp.provider_login'))

    return redirect(url_for('dashboards_bp.provider_chat_box',job_id=job_id))

