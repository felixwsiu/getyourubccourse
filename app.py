from flask import Flask, flash, render_template , request, redirect
from threading import Thread
import coursescraper
import emailer
import databaseutil
import metrics
import premiumutil
from forms import courseRequestForm, removeRequestForm, premiumForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "<\x8e\xd5`\x87c\xc0\xee<s?\xe0\xe1x\x8a\x88X\x81\x99_\x83\x999w"


# Will check validation errors in the form and flash messages for the user
# @params {form} form: the course request form 
def errorFlashing(form):
	for fieldName, errorMessages in form.errors.items():
		for err in errorMessages:
			if err == "A Request Reference ID is required.":
				flash("A Request Reference ID is required.",["danger","deregister"])
			if err == "This field is required.":
				flash("A " + fieldName + " is required", ["danger","register"])
			if err == "Email is invalid.":
				flash("Your email is invalid", ["danger","register"])

# Will check if the course is valid, and duplicate request before adding the new request to the DB
# @params {form} form: the course request form 
def courseSubmitSuccess(form):
	dept = form.department.data
	course = form.course.data
	section = form.section.data
	email = form.email.data

	if premiumutil.isPremiumUser(email):
		premium = True
	else:
		premium = False;

	if coursescraper.isCourseValid(dept, course, section):
		if (not databaseutil.isMaxRequests(email)) or premium:
			if databaseutil.doesNotDuplicate(dept, course, section, email):
				app.logger.info("New Course Request : " + dept + course + " " + section + ". Email: " + email + "\n")
				databaseutil.addRequest(dept, course, section, email, premium)
				flash(dept + " " + course + " " + section +" was successfully added for you! 😊", ["success","register"])
				if premium:
					flash("This course request will poll at light-speed with your 👑 PREMIUM Status 👑" , ["success","register"])
			else:
				flash("Course request is duplicated, you're covered! 😎", ["warning","register"])
		else:
			flash("You have hit the free limit for course requests! 😔 Deregister an existing request or upgrade to Premium!" , ["warning","register"])
	else:
		flash("Course was not valid, double check for typos! 😔", ["danger","register"])

# Will remove the course request from the DB using the ID of the item
# @params {form} form: the course request form 
def courseRemoveSuccess(form):
	courserequest = databaseutil.getCourseRequest(form.id.data)
	if courserequest != False:
		databaseutil.deleteRequest(courserequest["id"],courserequest["email"])
		flash("Your request was successfully removed! 😊", ["success","deregister"])
	else:
		flash("Couldn't find a course request under that ID! 😔" ,["danger","deregister"])


@app.route('/', methods=["GET","POST"])
def home():
	crform = courseRequestForm()
	rrform = removeRequestForm()

	seats = metrics.getTotalNotificationsSent()
	courses = len(databaseutil.getAllRequests())
	premiumusers = len(premiumutil.getAllUsers())
	if request.method == "POST" and request.form["submit"] == "register" and crform.validate_on_submit():
		courseSubmitSuccess(crform)
	else:
		errorFlashing(crform)


	if request.method == "POST" and request.form["submit"] == "deregister" and rrform.validate_on_submit():
		courseRemoveSuccess(rrform)
	else:
		errorFlashing(rrform)

	return render_template("home.html", crform=crform, seats=seats, courses=courses, premiumusers=premiumusers, rrform=rrform)


@app.route('/premium', methods=["GET","POST"])
def premium():
	pform = premiumForm()
	seats = metrics.getTotalNotificationsSent()
	courses = len(databaseutil.getAllRequests())
	premiumusers = len(premiumutil.getAllUsers())
	return render_template("premium.html", seats=seats, courses=courses, premiumusers=premiumusers, pform=pform)

if __name__ == '__main__':
	app.run(debug=True)
