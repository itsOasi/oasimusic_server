import database, helper

#####################################
#	Create Database and Tables Here
database_file = "database.db"
db = database.Database(database_file)
user_table = db.create_table("User", {"id":"TEXT", 
									  "email":"TEXT", 
									  "name":"TEXT", 
									  "password":"TEXT",
									  "role":"TEXT", 
									  "session":"TEXT"})
data_table = db.create_table("Data", {"id":"TEXT",
									  "key":"TEXT",
									  "value":"TEXT"})
									  
########################################################################################
#	Create classes to represent the tables and control the flow of the program

class User:
	def __init__(self, kwargs={}):
		self.id = ''
		self.name = kwargs["name"] if "name" in kwargs.keys() else ""
		self.email = kwargs["email"] if "email" in kwargs.keys() else ""
		self.password = kwargs["password"]  if 'password' in kwargs.keys() else ""
		self.role = 'user'
		self.logged_in = False
		self.session = kwargs["session"] if 'session' in kwargs.keys() else ""
	
	def signup(self, name, email, password):
		self.name = name
		user_table.insert({"id":helper.generate_id("USR"),  "email":email, "name":name, "password":password, "role":"user", "session":helper.generate_id("SESH")})
		print("welcome "+self.name)
		print("please log in")
	
	def login(self, email, password):
		user_table.add_query("email", "=", email)
		user_table.add_query("password", "=", password)
		user_table.run_query()
		if len(user_table.results):
			res = user_table.results[0]
			print(res)
			self.id = res[0]
			self.email = res[1]
			self.name = res[2]
			self.password = res[3]
			self.role = res[4]
			self.logged_in = True
			self.generate_session_id()
			print("welcome back "+self.name)
			return self.session
		else:	
			print("no user found")
			return False
		
	def logout(self):
		user_table.update("session", "", "id", self.id)
		self.logged_in = False

	def check_session(self, id, session):
		user_table.add_query("id", "=", id)
		user_table.add_query("session", "=", session)
		user_table.run_query()
		if len(user_table.results):
			return True
		else:
			return False

	def generate_session_id(self):
		self.session = helper.generate_id("SESH")
		user_table.update("session", self.session, "id", self.id)

		


class Data:
	def __init__(self, kwargs={}):
		self.id = kwargs["id"] if "id" in kwargs.keys() else ""
		self.key = kwargs["key"] if "key" in kwargs.keys() else ""
		self.value = kwargs["value"] if "value" in kwargs.keys() else ""
	
	def add(self, key, value):
		data_table.insert({"id":helper.generate_id("DAT"), "key":key, "value":value})
		print("data added")
	
	def get(self, key):
		data_table.add_query("key", "=", key)
		data_table.run_query()
		if len(data_table.results):
			res = data_table.results[0]
			print(res)
			self.id = res[0]
			self.key = res[1]
			self.value = res[2]
			print("data retrieved")
		else:	
			print("no data found")
	
	def get_all(self):
		data_table.run_query()
		return data_table.results

	def update(self, key, value):
		data_table.add_query("key", "=", key)
		data_table.add_query("value", "=", value)
		data_table.run_query()
		if len(data_table.results):
			res = data_table.results[0]
			print(res)
			self.id = res[0]
			self.key = res[1]
			self.value = res[2]
			print("data updated")
		else:	
			print("no data found")

	def delete(self, key):
		data_table.add_query("key", "=", key)
		data_table.run_query()
		print("data deleted")



##################################################################################################
#tests
if __name__ == "__main__":
	import os
	user = User({})
	
	def test_signup():
		email = input("enter an email ")
		name = input("enter your full name ")
		password = input("enter a password ")
		user.signup(name, email, password)
	
	def test_login():
		email = input("enter an email ")
		password = input("enter a password ")
		user.login(email,  password)
	
	test_commands = {
	"sign up":test_signup, 
	"log in":test_login
	}

	while True:
		user_input = input("what are we testing?\n"+str(list(test_commands.keys()))+"\n")
		if user_input in test_commands:
			test_commands[user_input]()

	
	