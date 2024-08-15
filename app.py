import database, helper

#####################################
#	Create Database and Tables Here

db = database.Database(":memory:")
user_table = db.create_table("User", {"id":"TEXT", 
									  "email":"TEXT", 
									  "name":"TEXT", 
									  "password":"TEXT", 
									  "member":"BOOL"})
business_table = db.create_table("Business", {"id":"TEXT", 
											  "name":"TEXT", 
											  "owner_id":"TEXT", 
											  "about":"TEXT", 
											  "location":"TEXT", 
											  "location_public":"BOOL"})
service_table = db.create_table("Service", {"id":"TEXT", 
											"user_id":"TEXT", 
											"name":"TEXT", 
											"price":"REAL", 
											"about":"TEXT"})
review_table = db.create_table("Review", {"id":"TEXT", 
										  "email":"TEXT", 
										  "name":"TEXT", 
										  "password":"TEXT"})
# store anonymized user searches with location if user consents
# searches are used to help local businesses match their services to local needs
search_table = db.create_table("Search", {"id":"TEXT",  
										  "phrase":"TEXT",  
										  "date_time":"", 
										  "location":"string"})

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

	def start_business(self, name, about):
		if not self.member:
			print("must be a member to start a business")
			return False
		b = Business(self.id, name, about)
		b.create()
		self.businesses.append(b)
		return {""}
	
	def get_businesses(self):
		# businesses created by the user
		business_table.add_query("owner", "=", self.id)
		business_table.run_query()
		
	def add_business_service(self, business_id, name, price, about):
		if not self.member:
			return False
		for b in self.businesses:
			print(f"{b.id} {business_id}")
			if b.id == business_id:
				print("hello")
				b.add_service(self.id, name, price, about)
		
	def get_nearby_service_providers(self, location):
		pass
	
	def leave_review(self, service_id):
		r = Review(self.name, self.email, service_id,)
	
class Business:
	def __init__(self, owner_id, name, about, kwargs={}):
		self.id = ""
		self.owner = owner_id
		self.name = name
		self.about = about
		self.location = kwargs["location"] if "location" in kwargs else ""
		self.location_public = kwargs["location_public"] if "location_public" in kwargs else False
		self.contact = ""
		self.services = []
	
	def create(self):
		self.id = helper.generate_id("BUS")
		business_table.insert({"id": self.id, "name":self.name, "user_id":self.owner, "about":self.about, "location":self.location, "location_public":False})
	
	
	def add_service(self, user_id, name, price, about):
		print(f"{user_id} {self.owner}")
		if not user_id == self.owner:
			return False
		s = Service(name, price, about, self.id)
		s.create()
		self.services.append(s)
	
class Service:
	def __init__(self, name, price, about, business_id):
		self.id = ""
		self.name = name
		self.price = price
		self.business_id = business_id
		self.about = about
	
	def create(self):
		self.id = helper.generate_id("SRV")
		service_table.insert({"id":self.id, "business_id": self.business_id, "name":self.name, "price":self.price, "about":self.about})
		print("service created")

class Review:
	def __init__(self, user_name, user_email, service_id, rating=3, comment=""):
		self.id = ""
		self.user_name = user_name
		self.user_email = user_email
		self.service_id = service_id
		self.rating = rating
		self.comment = comment
	
	def create(self):
		print("review created")

def search(query, location=""):
	# add search to search table
	# query businesses
	print('searching...')
	_query_businesses(query, location)

def _query_businesses(self, query, location=""):
	# query services
	business_table.add_query("about", "LIKE", query)
	business_table.run_query()
	print(business_table.results)

def query_services(self, query, location=""):
	# query services
	pass
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
	
	def test_join():
		user.join()
	
	def test_start_bus():
		name = input("enter business name ")
		about = input("whats your business about? ")
		user.start_business(name, about)
		
	
	def test_add_service():
		id = input("enter business id ")
		name = input("enter service name ")
		about = input("what is the service about? ")
		price = input("how much does the service cost? ")
		user.add_business_service(name, id, price, about)
		for bus in user.businesses:
			print(f"{bus.id} - {bus.name}")
			print(bus.services)
		
	def test_quick_add_service():
		quser = User({"name":"name", "email":"email", "password":"1234"})
		quser.signup(quser.name, quser.email, quser.password)
		quser.login(quser.email, quser.password)
		quser.join()
		quser.start_business("name llc", "business")
		id = quser.businesses[0].id
		name = "service"
		about = "serving"
		price = 100
		quser.add_business_service(id, name, price, about)
		for bus in quser.businesses:
			print(f"{bus.id} - {bus.name}")
			print(bus.services)
	
	def test_leave_review():
		pass
	
	def fill_db():
		for i in range(20):
			test_quick_add_service()
			
	def test_search():
		query = input("enter search query ")
		search(query)
		# location = input("enter coordinates")
	
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
	while True:
		user_input = input("what are we testing?\n"+str(list(test_commands.keys()))+"\n")
		if user_input in test_commands:
			test_commands[user_input]()

	
	