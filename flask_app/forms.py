from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length, InputRequired, ValidationError

class CatReviewForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=50)])
    text = TextAreaField('Review', validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Submit')
    
class RegistrationForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(min=1, max=50)])
    text = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Submit')
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Log In')

class SubmitReview(FlaskForm):
    stars = SelectField("Rating", choices=["1","2", "3", "4", "5"],)
    submit = SubmitField('Submit')