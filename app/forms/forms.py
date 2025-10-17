from flask_wtf import FlaskForm
from wtforms.validators import Length,Email,DataRequired,InputRequired,EqualTo
from wtforms import SearchField,StringField,PasswordField,SubmitField,EmailField,SelectField,TextAreaField

# user
class User_RegisterForms(FlaskForm):
   user_name = StringField('Full Name',validators=[InputRequired(),Length(min=6,max=20)])
   user_email = EmailField('Email',validators=[InputRequired(),Email()])
   user_password = PasswordField('Password',validators=[InputRequired(),Length(min=6,max=20)])
   confirm_password = PasswordField('Confirm Password',validators=[InputRequired(),EqualTo('user_password',message='Password must match.')])
   submit = SubmitField('Register As User')

# provider
class Provider_RegisterForm(FlaskForm):
   provider_name = StringField('Username',validators=[InputRequired(),Length(min=6,max=20)])
   provider_email = EmailField('Email',validators=[InputRequired(),Email()])
   provider_password = PasswordField('Password',validators=[InputRequired(),Length(min=6,max=20)])
   confirm_password = PasswordField('Confirm Password',validators=[InputRequired(),EqualTo(provider_password)])
   profession = SelectField('Profession', choices=[
        ('plumber', 'Plumber'),
        ('electrician', 'Electrician'),
        ('cleaner', 'Cleaner'),
        ('carpenter', 'Carpenter'),
        ('painter', 'Painter'),
    ], validators=[InputRequired()])
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
   user_password = PasswordField('Password',validators=[DataRequired(),Length(min=6,max=20)])
   submit=SubmitField('Login As a User')

   # Provider
class Provider_LoginForm(FlaskForm):
   provider_name = StringField('Full Name',validators=[InputRequired(),Length(min=6,max=20)])
   provider_password = PasswordField('Password',validators=[DataRequired(),Length(min=6,max=20)])
   submit=SubmitField('Login As a User')




