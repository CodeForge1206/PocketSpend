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
        self.add_date_column()  # Adds date column if it doesn't exist
        self.create_categories_table()  # Creates the categories table
        self.add_default_categories()  # Adds default categories
        self.add_category_id_column()  # Adds category ID if needed
        self.update_existing_category_ids()  # Links old expenses to categories
    # Create Categories Table
    # -----------------------------

    def create_categories_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT NOT NULL UNIQUE
            )
        """)  # Creates the categories table

        self.connection.commit()  # Saves the changes

        # -----------------------------
    # Add Default Categories
    # -----------------------------

    def add_default_categories(self):
        categories = [
            "Food",
            "Transport",
            "Entertainment",
            "Bills",
            "Shopping"
        ]  # Creates our default categories

        for category in categories:
            self.cursor.execute("""
                INSERT OR IGNORE INTO categories (category_name)
                VALUES (?)
            """, (category,))  # Adds the category if it doesn't exist

        self.connection.commit()  # Saves the categories

        # Add Category ID Column
    # -----------------------------

    def add_category_id_column(self):
        self.cursor.execute("""
            PRAGMA table_info(expenses)
        """)  # Gets information about the expenses table

        columns = self.cursor.fetchall()  # Gets all columns

        column_names = [column[1] for column in columns]  # Gets column names

        if "category_id" not in column_names:
            self.cursor.execute("""
                ALTER TABLE expenses
                ADD COLUMN category_id INTEGER
            """)  # Adds the category ID column
        # -----------------------------
    # Link Existing Categories
    # -----------------------------

    def update_existing_category_ids(self):
        self.cursor.execute("""
            UPDATE expenses
            SET category_id = (
                SELECT category_id
                FROM categories
                WHERE categories.category_name = expenses.category
            )
            WHERE category_id IS NULL
        """)  # Matches old category names to category IDs

        self.connection.commit()  # Saves the changes

        # -----------------------------
    # Get Categories
    # -----------------------------

    def get_categories(self):
        self.cursor.execute("""
            SELECT category_id, category_name
            FROM categories
            ORDER BY category_name
        """)  # Gets all categories

        return self.cursor.fetchall()  # Returns the categories




    # -----------------------------
    # Create Expenses Table
    # -----------------------------

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)  # Creates the expenses table

        self.connection.commit()  # Saves the changes
        # -----------------------------
    # Add Date Column
    # -----------------------------
    def add_date_column(self):
        self.cursor.execute("""
            PRAGMA table_info(expenses)
        """)  # Gets information about the table

        columns = self.cursor.fetchall()  # Gets the table columns

        column_names = [column[1] for column in columns]  # Gets column names

        if "date" not in column_names:
            self.cursor.execute("""
        ALTER TABLE expenses
        ADD COLUMN date TEXT
    """)  # Adds the date column

            self.cursor.execute("""
        UPDATE expenses
        SET date = date('now')
        WHERE date IS NULL
    """)  # Gives old expenses today's date

            self.connection.commit()  # Saves the changes
    

        # -----------------------------
    # Add Expense
    # -----------------------------

    def add_expense(self, description, amount, category, date):
        self.cursor.execute("""
            INSERT INTO expenses (description, amount, category, date)
            VALUES (?, ?, ?, ?)
        """, (description, amount, category, date))  # Adds the expense to the database

        self.connection.commit()  # Saves the expense

        # -----------------------------
    # Get Expenses
    # -----------------------------

    def get_expenses(self):
        self.cursor.execute("""
            SELECT id, description, amount, category, date
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
    # Get Categories
    # -----------------------------

    def get_categories(self):
        self.cursor.execute("""
            SELECT category_id, category_name
            FROM categories
            ORDER BY category_name
        """)  # Gets categories from the database

        return self.cursor.fetchall()  # Returns the categories

    # -----------------------------
    # Close Database
    # -----------------------------

    def close(self):
        self.connection.close()  # Closes the database connection
