# -----------------------------
# Expense Class
# -----------------------------

class Expense:
    # Creates a new Expense object
    def __init__(self, description, amount, category):
        self.description = description  # Stores the expense description
        self.amount = amount  # Stores the expense amount
        self.category = category  # Stores the expense category