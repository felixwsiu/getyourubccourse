from flask import Flask, flash, render_template , request, redirect
from threading import Thread
import coursescraper
import emailer
import databaseutil
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

# Will check if the course is valid, and duplicate request before adding the new request to the DB
# @params {form} form: the course request form 
def courseSubmitSucess(form):
	dept = form.department.data
	course = form.course.data
	section = form.section.data
	email = form.email.data

	if coursescraper.isCourseValid(dept, course, section):
		if databaseutil.doesNotDuplicate(dept, course, section, email):
			app.logger.info("New Course Request : " + dept + course + " " + section + ". Email: " + email)
			databaseutil.addRequest(dept, course, section, email)
			flash(dept + " " + course + " " + section +" was successfully added for you! 😊", "success")
		else:
			flash("Course request is duplicated, you're covered! 😎", "warning")
	else:
		flash("Course was not valid, double check for typos! 😔", "danger")


@app.route('/', methods=["GET","POST"])
def home():
	form = courseRequestForm()
	if request.method == "POST" and form.validate_on_submit():
		courseSubmitSucess(form)
	else:
		errorFlashing(form)

	return render_template("home.html", form=form)




if __name__ == '__main__':
	app.run(debug=True)
