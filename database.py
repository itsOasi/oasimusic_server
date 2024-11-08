import sqlite3
'''
	The Database class represents the entire database. It grants convenient access to 
	the tables within the database.
'''
class Database:
	def __init__(self, database_name):
		self.name = database_name or ":memory:"
		self.connection = sqlite3.connect(database_name)
		self.cursor = self.connection.cursor()

	def create_table(self, table_name, fields):
		# fields = {"field_name":"TYPE"}
		return Table(self.name, table_name, fields, True)
        
	def get_table(self, table_name):
		return Table(self.name, table_name)

	#TODO: def delete_table

'''
	The table class provides CRUD control over a single table. It is most conveniently 
	accessed through the Database class, but do as you will.
'''
class Table:
	def __init__(self, database_name, table_name, fields={}, create=False):
		self.connection = sqlite3.connect(database_name, check_same_thread=False)
		self.cursor = self.connection.cursor()
		self.table_name = table_name
		self.results = []
		self.columns = {}
		self.filter = ""
		self.field_str = ""
		if create:
			self.columns = fields
			self._create_table(self.columns)
	
	def _create_table(self, fields):
		#fields {variable_name:variable_type}
		field_str = ""
		# print(f"columns {self.columns}")
		for name, datatype in fields.items():
			field_str += f"{name} {datatype}, "
		self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({field_str[:-2]})")
		self.connection.commit()
		
	def insert(self, data):
		#data = {column: value}
		field_str = ", ".join(data.keys())
		placeholder_str = ", ".join("?" for _ in data.values())
		query_str = f"INSERT INTO {self.table_name}({', '.join(i for i in list(self.columns.keys()))}) VALUES ({placeholder_str})"
		print(query_str)
		self.cursor.execute(query_str, tuple(data.values()))
		self.connection.commit()
	
	def add_query(self, column, operator, value):
		# TODO: make sure value is correct type
		if type(value) is str:
			self.filter += f"{column} {operator} '{value}' AND "
		if type(value) is int or type(value) is float:
			self.filter += f"{column} {operator} {value} AND "
		else:
			return
	
	def run_query(self, columns="*"):
		query = f"SELECT {columns} FROM {self.table_name}"
		if self.filter:
			query += f" WHERE {self.filter[:-5]}"
		print("LOG "+query)
		self.cursor.execute(query)
		self.results = self.cursor.fetchall()
		self.filter = ""
	
	def delete(self, condition):
		self.cursor.execute(f"DELETE FROM {self.table_name} WHERE {condition}")
		self.connection.commit()

	def update(self, column, value, condition_column=None, condition_value=None):
		# Construct the base query
		query = f"UPDATE {self.table_name} SET {column} = ?"
		params = [value]

		# Add the condition if provided
		if condition_column and condition_value:
			query += f" WHERE {condition_column} = ?"
			params.append(condition_value)

		# Execute the query
		self.cursor.execute(query, params)
		self.connection.commit()

	#TODO: def add_columns
	
	#TODO: def rem_columns
	
	def close(self):
		self.cursor.close()
		self.connection.close()

if __name__ == "__main__":
	running = True
	db = Database(":memory:")
	curr_table = db.create_table("User", {"id":"INT", "email":"TEXT"})
	while running:
		cmnd = input("what would you like to do?")
		if cmnd in ["create table", "ct"]:
			table_name = input("enter table_name: ")
			fields = {}
			while True:
				prop = input("enter prop name or done: ")
				if prop in ["done"]:
					break
				type = input("enter value: ")
				fields[prop] = type
			curr_table = db.create_table(table_name, fields)
			print(curr_table.columns)
		
		if cmnd in ["get table", "gt"]:
			# db.list_tables
			table_name = input("enter table_name: ")
			curr_table = db.get_table(table_name)
		
		if cmnd in ["add query", "aq"]:
			if not curr_table:
				continue
			column = input("column name: ")
			operator = input("operator: ")
			value = input("value: ")
			curr_table.add_query(column, operator, value)
		
		if cmnd in ["run query", "run"]:
			if not curr_table:
				continue
			curr_table.run_query()
			print(curr_table.results)
			
		if cmnd in ["ins", "insert"]:
			if not curr_table:
				continue
			print(curr_table.columns)
			insert_vals = {}
			while True:
				prop = input("enter prop name or done")
				if prop in ["done"]:
					break
				value = input("enter value")
				insert_vals[prop] = value
			curr_table.insert(insert_vals)