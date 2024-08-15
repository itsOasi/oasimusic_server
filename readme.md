A minimal and hopefully easy to configure server template
using sqlite and flask.



Project Structure
- helper.py - functions that I commonly use in my projects
- database.py - wrapper around sqlite3, designed to be used similarly
  to GlideRecord from ServiceNow in the following ways:
  - add_query function to programmatically compose queries
  - run_query to run the constructed query, or just get all records
    if add_query wasn't used
- app.py - interfaces with database.py and helper.py to build out
  server logic and model the database.
- main.py - entry point to the project - use flask to expose logic in
  app.py to front end