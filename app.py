from flask import Flask, render_template   
from scheduler import turnOnScheduler
from threading import Thread
import emailer
import os

app = Flask(__name__)


@app.route('/')
def home():
	return render_template("home.html")


@app.route('/<name>')
def hello_name(name):
	return "Hello {}!".format(name)

if __name__ == '__main__':
	Thread(turnOnScheduler()).start()
	Thread(emailer.sendEmailTest()).start()
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, threaded=True, debug=True)
