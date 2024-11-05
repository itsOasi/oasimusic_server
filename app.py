import database, helper

#####################################
#	Create Database and Tables Here

db = database.Database(":memory:")
user_table = db.create_table("User", {"id":"TEXT", 
									  "email":"TEXT", 
									  "name":"TEXT", 
									  "password":"TEXT", 
									  "member":"BOOL"})

########################################################################################
#	Create classes to represent the tables and control the flow of the program

class User:
	def __init__(self, kwargs={}):
		self.id = ''
		self.name = kwargs["name"] if "name" in kwargs.keys() else ""
		self.email = kwargs["email"] if "email" in kwargs.keys() else ""
		self.password = kwargs["password"]  if 'password' in kwargs.keys() else ""
		self.businesses = []
		self.reviews = []
		self.logged_in = False
		self.member = False
	
	def signup(self, name, email, password):
		self.name = name
		user_table.insert({"id":helper.generate_id("USR"),  "email":email, "name":name, "password":password, "member": False})
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
			self.logged_in = True
			print("welcome back "+self.name)
		
	def join(self):
		if not self.logged_in:
			print("must be logged in to join")
			return False
		self.member = True

	
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
		if not user.member:
			return
		for bus in user.businesses:
			print(f"{bus.id} - {bus.name}")
			for srv in bus.services:
				print(f"{srv.name} - {srv.price}")
	
	
	
	test_commands = {
	"sign up":test_signup, 
	"log in":test_login
	}
	while True:
		user_input = input("what are we testing?\n"+str(list(test_commands.keys()))+"\n")
		if user_input in test_commands:
			test_commands[user_input]()

	
	