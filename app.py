from flask import Flask, flash, render_template , request, redirect
from threading import Thread
import coursescraper
import emailer
from forms import courseRequestForm


app = Flask(__name__)
app.config['SECRET_KEY'] = "<\x8e\xd5`\x87c\xc0\xee<s?\xe0\xe1x\x8a\x88X\x81\x99_\x83\x999w"


# Will check validation errors in the form and flash messages for the user
# @params {form} form: the course request form 
def errorFlashing(form):
	for fieldName, errorMessages in form.errors.items():
		for err in errorMessages:
			if err == "This field is required.":
				flash("A " + fieldName + " is required", "danger")
			if err == "Email is invalid.":
				flash("Your email is invalid", "danger")


@app.route('/', methods=["GET","POST"])
def home():
	form = courseRequestForm()
	if request.method == "POST" and form.validate_on_submit():
		if coursescraper.isCourseValid(form.dept.data, form.course.data, form.section.data):
			flash("Course was successfully added to our system! 😊", "success")
		else:
			flash("Course was not valid, double check the fields. 😔", "danger")
	else:
		errorFlashing(form)

	return render_template("home.html", form=form)




if __name__ == '__main__':
	app.run(debug=True)
