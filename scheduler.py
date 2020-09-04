from datetime import date, datetime
import databaseutil 
import coursescraper
import emailer
import sys
import metrics
#Scheduler.py will be run on Heroku Scheduler with 10 minute intervals


# Runs on a given interval to iterate through the list of course requests and notify users
# if a spot has opened up in their courses
def checkCoursesForUsers():
	requests = databaseutil.getAllRequests()
	# over due requests will be deleted to clean up DB
	delete = []
	for r in requests:
		if coursescraper.isCourseSeatOpen(r.dept, r.course, r.section):
			sys.stdout.write("Sending Course Seat Email: " + r.dept + r.course + " " + r.section + ". Email: " + r.email + "\n")
			emailer.sendCourseSeatEmail(r.email, r.dept, r.course, r.section)
			metrics.addTotalNotificationsSent()
		requestExpiryCheck(r.id, r.email, r.dept, r.course, r.section, r.dateAdded)
		

# The dateAdded string will be converted to the date type to be compared to todays date
# If it is greater than 30 (1 month), the request will expire and be deleted
# @params {string} id: unique id name for the representing request
# @params {string} email: user's email that is also used as the partition key for this container
def requestExpiryCheck(id, email, dept, course, section, dateAdded):
	if (date.today() - datetime.strptime(dateAdded, "%Y-%m-%d").date()).days > 30:
		sys.stdout.write("Deleting Course Request : " + dept + course + " " + section + ". Email: " + email + "\n")
		databaseutil.deleteRequest(id,email)
		emailer.sendDeletedCourseRequestEmail(email, dept, course, section)

checkCoursesForUsers()