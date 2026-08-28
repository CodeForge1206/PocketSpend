import sqlite3  # Imports Python's SQLite library

#Database Connection 
connection = sqlite3.connect("pocketspend.db")  # Creates/connects to the database
cursor = connection.cursor()  # Creates a cursor for executing SQL commands

#Create expense table 

cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL
    )
""")  # Creates the expenses table if it doesn't already exist


connection.commit()  # Saves the database changes

connection.close()  # Closes the database connection