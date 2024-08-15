from flask import Flask, request, json
from flask_cors import CORS
import app, helper, database
import datetime
app = Flask(__name__)

ASSET_DIR = "" # where repo data will be stored
ADMIN_PASSWD = "1234" # get from environment variable
# config = helper.json_to_dict("config.json") # settings to be
# if config["cors"]:
#	CORS(app)

'''
	test_commands = {
		"fill db": fill_db,
		"search": test_search,
		"sign up":test_signup, 
		"log in":test_login, 
		"join": test_join,
		"start bus":test_start_bus,
		"add srv": test_add_service,
		"quick add srv": test_quick_add_service
	}
'''

@app.route("/search") # performs search on business table
def search():
	print(request.form)
	app.search(request.form["query"], request.form["location"])

@app.route("/signup") # creates user 
def signup():
	print(request.form)
	user = app.User({})
	user.signup(request.form["name"], request.form["email"], request.form["password"])

@app.route("/login") # loads homepage
def login():
	print(request.form)
	user = app.User({})
	user.login(request.form["email"], request.form["password"])


@app.route("/join") # loads homepage
def join():
	print(request.form)
	user = app.User({})
	user.join()

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8001, debug=True)
