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
```

Some environmental variables will be needed, please set these to run this project locally:
```
EMAILPASS : This is the password of the email account set in emailer.py
ACCOUNT_URI : This is the URI of your Azure Cosmos DB Account
ACCOUNT_KEY : This is the primary key of your Azure Cosmos DB Account
```

Make sure project dependencies match requirements.txt after installation

## TODO List
- A premium service using paypal for users to have faster polling, more maximum requests, sms capability
- Make UX/UI better, change the background maybe

