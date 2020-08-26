from flask import Flask, render_template   
from scheduler import turnOnScheduler

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
	turnOnScheduler()
	app.run(debug=True)
	
