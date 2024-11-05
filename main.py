from flask import Flask, request, json
from flask_cors import CORS
import app, helper, database
import datetime
flask_app = Flask(__name__)

ASSET_DIR = "" # where repo data will be stored
ADMIN_PASSWD = "1234" # get from environment variable
# config = helper.json_to_dict("config.json") # settings to be
# if config["cors"]:
#	CORS(app)

@flask_app.route("/signup") # creates user 
def signup():
	print(request.form)
	user = app.User({})
	user.signup(request.form["name"], request.form["email"], request.form["password"])

@flask_app.route("/login") # loads homepage
def login():
	print(request.form)
	user = app.User({})
	user.login(request.form["email"], request.form["password"])


if __name__ == "__main__":
	flask_app.run(host="0.0.0.0", port=8001, debug=True)
