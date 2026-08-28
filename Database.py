import sqlite3  # Imports SQLite


# -----------------------------
# Database Class
# -----------------------------

class Database:
    # Creates a connection to the database
    def __init__(self):
        self.connection = sqlite3.connect("pocketspend.db")
        self.cursor = self.connection.cursor()

        self.create_table()  # Creates the expenses table


    # -----------------------------
    # Create Expenses Table
    # -----------------------------

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL
            )
        """)

        self.connection.commit()  # Saves the changes

        # -----------------------------
    # Add Expense
    # -----------------------------

    def add_expense(self, description, amount, category):
        self.cursor.execute("""
            INSERT INTO expenses (description, amount, category)
            VALUES (?, ?, ?)
        """, (description, amount, category))  # Adds the expense to the database

        self.connection.commit()  # Saves the expense


    # -----------------------------
    # Close Database
    # -----------------------------

    def close(self):
        self.connection.close()  # Closes the database connection
