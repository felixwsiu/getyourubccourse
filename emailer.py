import smtplib, ssl, os

# A SMPTP Connection will be secured from the beginning using SMTP_SSL()
# For this code to work, your google account must have "Allow Less Secure Apps to ON"
# or your login will be deemed dangerous. (WARNING : This will make your account more vulnerable)
# TLS-encrypted connection will be initiated, and the default context of SSL will load the system’s trusted CA certificates,
# enable host name checking and certificate validation, and try to choose reasonably secure protocol and cipher settings.

port = 465 
smtp_server = "smtp.gmail.com"

# Email Settings
sender_email = "getyourubccourse@gmail.com" 
receiver_email = "felixs1999@gmail.com"  

message = """\
Subject: Hi there

This message is sent from Python.
"""


# EMAILPASS is an ENV on heroku's servers. If you want to run this locally, you can simply replace it with
# an input("")
password = os.environ["EMAILPASS"]; #input("Type your password and press enter: ")

def sendEmailTest():
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
	    server.login(sender_email, password)
	    server.sendmail(sender_email, receiver_email, message)