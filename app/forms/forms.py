from flask_wtf import FlaskForm
from wtforms.validators import Length,Email,DataRequired,InputRequired,EqualTo
from wtforms import SearchField,StringField,PasswordField,SubmitField,EmailField,SelectField,TextAreaField,IntegerField,DateTimeField,HiddenField
from datetime import datetime # for DateField
# user
class User_RegisterForms(FlaskForm):
   user_name = StringField('Full Name',validators=[InputRequired(),Length(min=6,max=20)])
   user_email = EmailField('Email',validators=[InputRequired(),Email()])
   user_phone = StringField('Contact',validators=[InputRequired(),Length(max=10)])
   user_password = PasswordField('Password',validators=[InputRequired(),Length(min=6,max=20)])
   confirm_password = PasswordField('Confirm Password',validators=[InputRequired(),EqualTo('user_password',message='Password must match.')])
   submit = SubmitField('Register As User')

# provider
class Provider_RegisterForm(FlaskForm):
   provider_name = StringField('Username',validators=[InputRequired(),Length(min=6,max=20)])
   provider_email = EmailField('Email',validators=[InputRequired(),Email()])
   provider_password = PasswordField('Password',validators=[InputRequired(),Length(min=6,max=20)])
   confirm_password = PasswordField('Confirm Password',validators=[InputRequired(),EqualTo('provider_password',message='Password must match.')])
   profession = SelectField('Your Profession', choices=[
        ('plumber', 'Plumber'),
        ('electrician', 'Electrician'),
        ('cleaner', 'Cleaner'),
        ('handyman', 'Handyman'),
        ('carpenter', 'Carpenter'),
        ('general_worker', 'General Worker')
    ], validators=[DataRequired()])

   profession_desc = TextAreaField('Description',validators=[InputRequired(),Length(max=500,message='Description must be under 500')])
   
   # location = SelectField('Location', choices=[
   #      ('karachi', 'Karachi'),
   #      ('lahore', 'Lahore'),
   #      ('islamabad', 'Islamabad'),
   #      ('peshawar', 'Peshawar'),
   #      ('quetta', 'Quetta'),
   #      ('faisalabad', 'Faisalabad'),
   #      ('multan', 'Multan'),
   #  ], validators=[InputRequired()])
   
   phone = StringField('Phone Number', validators=[InputRequired(), Length(min=10, max=15)])  # starts form 0 
   submit = SubmitField('Register As Provider')



   ###### login forms
   # User
class User_LoginForm(FlaskForm):
   user_name = StringField('Full Name',validators=[InputRequired(),Length(min=6,max=20)])
   user_password = PasswordField('Password',validators=[InputRequired(),Length(min=6,max=20)])
   submit= SubmitField('Login As a User')

   # Provider
class Provider_LoginForm(FlaskForm):
   provider_name = StringField('Full Name',validators=[InputRequired(),Length(min=6,max=20)])
   provider_password = PasswordField('Password',validators=[InputRequired(),Length(min=6,max=20)])
   submit= SubmitField('Login As a Provider')


# admin form

class Admin_RegisterForm(FlaskForm):
   username = StringField('Username',validators=[InputRequired(),Length(min=6,max=20)])
   email = EmailField('Email',validators=[InputRequired(),Email()])
   password = PasswordField('Password',validators=[InputRequired(),Length(min=6,max=20)])
   submit = SubmitField('Register as Admin')



class Admin_LoginForm(FlaskForm):
   username = StringField('Username',validators=[InputRequired(),Length(min=6,max=20)])
   email = EmailField('Email',validators=[InputRequired(),Email()])
   password = PasswordField('Password',validators=[InputRequired(),Length(min=6,max=20)])
   secret_key =IntegerField('Secret Key',validators=[InputRequired()])
   submit = SubmitField('I am Admin')


####
class BookingForm(FlaskForm):
   provider_id = HiddenField('Provider_id')
   date_time = DateTimeField('Date & Time', validators=[InputRequired()],format='%Y-%m-%d %H:%M', default=datetime.now())
   address = TextAreaField('Address', validators=[InputRequired(),Length(max=50)])

   service_type = SelectField('Select',choices=[     
         ('plumbing', 'Plumbing'),
        ('electric', 'Electric'),
        ('cleaning', 'Cleaning'),
        ('mechanical', 'Mechanical'),
        ('technical', 'Technical'),])
   
   description=TextAreaField('Description', validators=[InputRequired(),Length(max=500)])
   contact = StringField('Contact', validators=[InputRequired(), Length(min=10,max=15)])

   submit = SubmitField('Book Service')


### Book a service form 

class BookServiceForm(FlaskForm):
   service_type = SelectField('Choose a service',choices=[        
        ('plumbing', 'Plumbing Work'),
        ('electrical', 'Electrical Work'), 
        ('cleaning', 'Cleaning'),
        ('handyman', 'Handyman Services'),
        ('carpentry', 'Carpentry Work'),
        ('other', 'Something Else')], validators=[InputRequired()])

   # service_address = TextAreaField('Write Your Address',validators=[InputRequired()])
   
   service_description = TextAreaField('Describe Your Specific Needs', validators=[DataRequired()])
   # contact = StringField('Contact', validators=[InputRequired(), Length(min=10,max=15)])
   # date = DateTimeField('DateTime',validators=[InputRequired()],format='%Y-%m-%d %H:%M', default=datetime.now())
   submit = SubmitField('Request')


   # complete profile
class CompleteProfileForm(FlaskForm):
   address = TextAreaField('Provide address',validators=[InputRequired(), Length(max=100)])
   submit = SubmitField('Submit')