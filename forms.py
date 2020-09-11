from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

class courseRequestForm(FlaskForm):
	email = StringField("Your Email", validators=[DataRequired(),Email("Email is invalid.")])
	department = StringField("Course Department", validators=[DataRequired()])
	course = StringField("Course Number", validators=[DataRequired()])
	section = StringField("Section Number", validators=[DataRequired()])
	register = SubmitField("Register")


class removeRequestForm(FlaskForm):
	id = StringField("Request Reference ID", validators=[DataRequired("A Request Reference ID is required.")])
	remove = SubmitField("Remove Request")

class premiumForm(FlaskForm):
	email = StringField("Your Email", validators=[DataRequired("An Email is required"),Email("Email is invalid.")])
	register = SubmitField("Register")