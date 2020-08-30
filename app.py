from flask import Flask, render_template   
from threading import Thread
import emailer


app = Flask(__name__)


@app.route('/')
def home():
	return render_template("home.html")


@app.route('/<name>')
def hello_name(name):
	return "Hello {}!".format(name)

if __name__ == '__main__':
	app.run(debug=True)
