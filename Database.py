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
            "Shopping",
            "Other"
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

    def add_expense(self, description, amount, category, date, category_id):
        self.cursor.execute("""
            INSERT INTO expenses (description, amount, category, date, category_id)
            VALUES (?, ?, ?, ?, ?)
        """, (description, amount, category, date, category_id))  # Adds the expense to the database

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

    #Get category ID
    def get_category_id(self, category_name):
        self.cursor.execute(""" SELECT category_id FROM categories WHERE category_name = ? """, (category_name,)) #Finds the ID for the selected category 
        result = self.cursor.fetchone() #Gets the matching category

        if result:
            return result[0] # Returns the category ID

        return None # Returns nothing if the category does not exist

    def add_other_category(self):
        self.cursor.execute(
        "INSERT INTO categories (category_name) VALUES (?)",
        ("Other",)
    )  # Adds Other to the categories table

        self.connection.commit()  # Saves the change

        # -----------------------------
    # Reset Category IDs
    # -----------------------------

    def reset_categories(self):
        # Temporarily turn off foreign key checking
        self.cursor.execute("PRAGMA foreign_keys = OFF")

        # Remove the unwanted category
        self.cursor.execute("""
            DELETE FROM categories
            WHERE category_name = 'ShoppingOther'
        """)

        # Change Other to a temporary name
        self.cursor.execute("""
            UPDATE categories
            SET category_name = 'OtherTemp'
            WHERE category_name = 'Other'
        """)

        # Change the category IDs to their correct values
        self.cursor.execute("""
            UPDATE categories
            SET category_id = CASE category_name
                WHEN 'Food' THEN 1
                WHEN 'Transport' THEN 2
                WHEN 'Entertainment' THEN 3
                WHEN 'Bills' THEN 4
                WHEN 'Shopping' THEN 5
                WHEN 'OtherTemp' THEN 6
            END
        """)

        # Change Other back to its normal name
        self.cursor.execute("""
            UPDATE categories
            SET category_name = 'Other'
            WHERE category_name = 'OtherTemp'
        """)

        # Update existing expenses to match the new IDs
        self.cursor.execute("""
            UPDATE expenses
            SET category_id = (
                SELECT category_id
                FROM categories
                WHERE categories.category_name = expenses.category
            )
        """)

        self.connection.commit()  # Saves all changes

        # Turn foreign key checking back on
        self.cursor.execute("PRAGMA foreign_keys = ON") 

    def remove_shopping_other(self):
        self.cursor.execute("""
        DELETE FROM categories
        WHERE category_name = 'ShoppingOther'
    """)  # Removes the accidental category

        self.connection.commit()  # Saves the change

        

    # -----------------------------
    # Close Database
    # -----------------------------

    def close(self):
        self.connection.close()  # Closes the database connection
