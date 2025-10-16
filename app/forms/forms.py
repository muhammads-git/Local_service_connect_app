from flask_wtf import FlaskForm
from wtforms.validators import Length,Email,DataRequired,InputRequired,EqualTo
from wtforms import SearchField,StringField,PasswordField,SubmitField,EmailField,SelectField

# user
class User_RegisterForms(FlaskForm):
   user_name = StringField('Full Name',validators=[InputRequired(),Length(min=6,max=20)])
   user_email = EmailField('Email',validators=[InputRequired(),Email()])
   user_password = PasswordField('Password',validators=[InputRequired(),Length(min=6,max=20)])
   confirm_password = PasswordField('Confirm Password',validators=[InputRequired(),EqualTo(user_password)])
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
   location = SelectField('Location', choices=[
        ('karachi', 'Karachi'),
        ('lahore', 'Lahore'),
        ('islamabad', 'Islamabad'),
        ('peshawar', 'Peshawar'),
        ('quetta', 'Quetta'),
        ('faisalabad', 'Faisalabad'),
        ('multan', 'Multan'),
    ], validators=[InputRequired()])
   
   submit = SubmitField('Register As Provider')