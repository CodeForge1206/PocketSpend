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
    # Get Expenses
    # -----------------------------

    def get_expenses(self):
        self.cursor.execute("""
            SELECT id, description, amount, category
            FROM expenses
        """)  # Gets all expenses from the database

        return self.cursor.fetchall()  # Returns the database records

    # -----------------------------
    # Get Total Spending
    # -----------------------------

    def get_total(self):
        self.cursor.execute("""
            SELECT SUM(amount)
            FROM expenses
        """)

        total = self.cursor.fetchone()[0]

        return total if total is not None else 0

    # -----------------------------
    # Close Database
    # -----------------------------

    def close(self):
        self.connection.close()  # Closes the database connection
