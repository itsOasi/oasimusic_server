from flask import Flask, request, send_file
from flask_cors import CORS
import app, helper, database, yt_stats, os, json
import datetime
flask_app = Flask(__name__)

yt = yt_stats.YTstats(app.Data({}).get("yt_api_key"), app.Data({}).get("yt_channel_id"))

# config = helper.json_to_dict("config.json") # settings to be
CORS(flask_app, resources={r"/*": {"origins": "*"}})
user = app.User({})
@flask_app.route("/", methods=["GET"]) # loads homepage
def index():
	return helper.read_file("auth.html")

@flask_app.route("/home", methods=["GET"]) # loads homepage
def home():
	return helper.read_file("index.html")

@flask_app.route("/signup", methods=["POST"]) # creates user 
def signup():
	print(request.form)
	user.signup(request.form["name"], request.form["email"], request.form["password"])
	return {"success": user.logged_in}

@flask_app.route("/login", methods=["POST"]) # loads homepage
def login():
	print(request.form)
	user.login(request.form["email"], request.form["password"])
	return {"success": user.logged_in, "id": user.id, "session": user.session}

@flask_app.route("/logout", methods=["GET"])
def logout():
	user.logout()
	return {"success": not user.logged_in}

@flask_app.route("/view_data", methods=["GET", "POST"]) # loads homepage
def view_data():
	if request.method == "POST":
		if not user.check_session(request.form["id"], request.form["session"]):
			return {"error": "invalid session"}
		return {"success": True}
	return helper.read_file("view_data.html")

@flask_app.route("/test_data", methods=["GET", "POST"]) # loads homepage
def test_data():
	if not user.check_session(request.form["id"], request.form["session"]):
		return {"error": "invalid session"}
	return helper.read_file("test_data.html")

@flask_app.route("/add_data", methods=["GET","POST"]) # updates config file
def add_config():
	if request.method == "GET":
		return helper.read_file("add_data.html")
	print(request.form)
	config = app.Data({})
	config.add(request.form["key"], request.form["value"])
	print(config.get_all())

	return {"success": True}

@flask_app.route("/get_all_data", methods=["POST"]) # loads homepage
def get_all_data():
	data = []
	if not user.check_session(request.form["id"], request.form["session"]):
		return {"error": "invalid session"}
	for row in app.data_table.results:
		data.append({"key": row[1], "value": row[2]})
	print(data)
	return data

@flask_app.route("/get_data", methods=["POST"]) # loads homepage
def get_data():
	if not user.check_session(request.form["id"], request.form["session"]):
		return {"error": "invalid session"}
	app.data_table.add_query("key", "=", request.form["key"])
	app.data_table.run_query()
	return app.data_table.results

@flask_app.route('/backup', methods=['GET'])
def download_db():
    try:
        return send_file(
            app.database_file,
            as_attachment=True
        )
    except Exception as e:
        return str(e), 500

@flask_app.route('/upload', methods=['GET', 'POST'])
def upload_db(): 
	if request.method == 'GET': 
		return helper.read_file("upload.html")
	if not user.check_session(request.form["id"], request.form["session"]):
		return {"error": "invalid session"}
	if 'file' not in request.files: 
		return {'error': 'No file part'}, 400
	file = request.files['file'] 
	if file.filename == '': 
		return {'error': 'No selected file'}, 400 
	if file and file.filename.endswith('.db'): 
		file_path = app.database_file
		file.save(file_path) 
		return {'message': 'Database uploaded successfully!'}, 200 
	return {'error': 'Invalid file format'}, 400

@flask_app.route("/refresh_yt_data", methods=["GET"]) # loads homepage
def refresh_yt_data():
	yt.api_key = app.Data({}).get("yt_api_key")
	yt.channel_id = app.Data({}).get("yt_channel_id")
	return yt.get_channel_video_data()

@flask_app.route("/get_yt_data", methods=["GET"]) # loads homepage
def get_yt_data():
	return helper.dict_to_json(yt.video_data)

if __name__ == "__main__":
	flask_app.run(host="0.0.0.0", port=8000)
