import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os

# A SMPTP Connection will be secured from the beginning using SMTP_SSL()
# For this code to work, your google account must have "Allow Less Secure Apps to ON"
# or your login will be deemed dangerous. (WARNING : This will make your account more vulnerable)
# TLS-encrypted connection will be initiated, and the default context of SSL will load the system’s trusted CA certificates,
# enable host name checking and certificate validation, and try to choose reasonably secure protocol and cipher settings.

port = 465 
smtp_server = "smtp.gmail.com"
sender_email = "getyourubccourse@gmail.com" 




# EMAILPASS is an ENV on heroku's servers. If you want to run this locally, you can simply replace it with
# an input("")
password = os.environ["EMAILPASS"]; #input("Type your password and press enter: ")

# Sends an email to a user that a seat has opened in their requested course
# @params {string} receiver_email : email of the receipient user
# @params {string} dept : department of the course (eg. CPSC)
# @params {string} course : course number (eg. 201)
# @params {string} section : section number (eg. 001)
def sendCourseSeatEmail(receiver_email, dept, course, section, id):
	html = """
		 <html>
			 <body>
				 <h2>Nice!</h2>
				 <h3>One or more seats has opened up in your desired course, register as soon as possible to snatch it away :) </h3>
				 <h3>Link to your course: https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept={dept}&course={course}&section={section}
				 <h3>Request Reference ID: {id}
				 <h3>Goodluck on your studies!</h3>
				 <h4>	- GetYourUBCCourse </h4>
				 <p>
				 	<img src="cid:image1">
				 </p>
			 </body>
		 </html>
	""".format(dept=dept,course=course,section=section,id=id)

	msgRoot = MIMEMultipart('related')
	msgRoot["Subject"] = f"GetYourUBCCourse - A Seat Has Opened Up In : {dept} {course} {section}"


	msgHtml = MIMEText(html,"html")

	img = open("emailpic/hahayes.png", "rb").read()
	msgImg = MIMEImage(img, "png")
	msgImg.add_header("Content-ID", "<image1>")
	msgImg.add_header("Content-Disposition", "inline", filename="emailpic/hahayes.png")

	msgRoot.attach(msgHtml)
	msgRoot.attach(msgImg)

	loginAndSend(receiver_email,msgRoot)


# Sends an email to a user that has their course request removed
# @params {string} receiver_email : email of the receipient user
# @params {string} dept : department of the course (eg. CPSC)
# @params {string} course : course number (eg. 201)
# @params {string} section : section number (eg. 001)
def sendDeletedCourseRequestEmail(receiver_email, dept, course, section):

	html = """
		 <html>
			 <body>
				 <h2>Wow!</h2>
				 <h3>Your course request has expired! Still haven't got into your course? You're going to have to request again :( </h3>
				 <h3>Link to the site: https://getyourubccourse-pro.herokuapp.com</h3>
				 <h3>Goodluck on getting in your course!</h3>
				 <h4>	- GetYourUBCCourse </h4>
				 <p>
				 	<img src="cid:image1">
				 </p>
			 </body>
		 </html>
	"""

	msgRoot = MIMEMultipart('related')
	msgRoot["Subject"] = f"GetYourUBCCourse - Your course request for: {dept} {course} {section} has expired"


	msgHtml = MIMEText(html,"html")

	img = open("emailpic/deleted.jpg", "rb").read()
	msgImg = MIMEImage(img, "jpg")
	msgImg.add_header("Content-ID", "<image1>")
	msgImg.add_header("Content-Disposition", "inline", filename="emailpic/deleted.jpg")

	msgRoot.attach(msgHtml)
	msgRoot.attach(msgImg)

	loginAndSend(receiver_email,msgRoot)


# Establishes a connection and logins in to the email server, then sends the msgRoot as a string
# @params {string} receiver_email : email of the receipient user
# @params {MIMEMultiPart} msgRoot : a MIMEobject for the whole email
def loginAndSend(receiver_email,msgRoot):
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
	    server.login(sender_email, password)
	    server.sendmail(sender_email, receiver_email, msgRoot.as_string())

