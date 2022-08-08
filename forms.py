from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length


class RegisterForm(FlaskForm):


    username = StringField("Username (Max 20 characters)", validators=[InputRequired(), Length(max=20) ])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(),])
    first_name = StringField("first name (Max 30 characters)", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("last name (Max 30 characters)", validators=[InputRequired(), Length(max=30)])

    


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

    
class FeedbackForm(FlaskForm):
    title = StringField("title", validators=[InputRequired()])
    content = TextAreaField("content", validators=[InputRequired()])

