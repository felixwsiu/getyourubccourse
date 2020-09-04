# GetYourUBCCourse

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
A bot that will iterate through given student course requests and notify them via email if a seat has opened up
in their desired course.

Seats will be parsed from :  
https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-all-departments
	
## Technologies
Project is created with:
* Python version: 3.7.8
* Dependencies can be found in requirements.txt

Hosted on Heroku with a production and staging:  
Production @ https://getyourubccourse-pro.herokuapp.com/  

Heroku free dynos are set to sleep with 30 minutes of inactivity, but our scheduler runs seperately on the Heroku Scheduler Addon so it will not be affected.
However, I didn't want a 10 second cold boot on the loading of the app every time so I used : http://kaffeine.herokuapp.com/ 
It will ping the heroku app every 30 minutes so it will never go to sleep

	
## Setup
Virtual environment for dependencies can be created by : python3 -m venv env

```
$ pip install flask
$ pip install Flask-WTF
$ pip install gunicorn
$ pip install beautifulsoup4
$ pip install APScheduler
$ pip install wtforms[email]
$ pip install Flask_Bootstrap4
```

Make sure project dependencies match requirements.txt after installation

## TODO List
- Metrics for emails, active users etc (Footer or header toolbar to display)
- A way to remove your request from the list (eg. User may get in the course), maybe a page that can login with a unique code and email to check on
 all requests that are related to the user. Emails should also have a link to removing the request so they can stop the spam
- A premium service using paypal for users to have faster polling, more maximum requests, sms capability
- Make UX/UI better, change the background maybe

