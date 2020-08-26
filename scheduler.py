import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

# Turns on a scheduler that is used to iterate over the course request list on a given interval
# Scheduler will shut down upon exit
def turnOnScheduler():
	scheduler = BackgroundScheduler()
	#Interation frequency can be changed here
	scheduler.add_job(func=checkCoursesForUsers, trigger="interval", minutes=0.05)
	scheduler.start()
	atexit.register(lambda: scheduler.shutdown())


# Runs on a given interval to iterate through the user list and notify users
# if a spot has opened up in their courses
def checkCoursesForUsers():
    print("Current Time: " + time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

