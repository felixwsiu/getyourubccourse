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

Hosted on Heroku:  
Production @ https://getyourubccourse-pro.herokuapp.com/  
Staging @ https://getyourubccourse-stage.herokuapp.com/
	
## Setup
Virtual environment for dependencies can be created by : python3 -m venv env

```
$ pip install flask
$ pip install gunicorn
$ pip install beautifulsoup4
$ pip install APScheduler
```

Make sure project dependencies match requirements.txt after installation
