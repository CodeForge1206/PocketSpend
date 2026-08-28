import tkinter as tk #Import python GUI library 
from tkinter import ttk
from expense import Expense  # Imports our Expense class
from tkinter import messagebox  # Imports popup messages
expenses = []  # Stores Expense objects
window = tk.Tk() # creates application main window 
window.title("PocketSpend") #window title name 
window.geometry("500x400")




subtitle_label = tk.Label(
    window, # Places the label inside the main window
    text="Personal Expense Tracker",  # Sets the subtitle
    font=("Arial", 12)  # Sets the font size
)
subtitle_label.pack(pady=(0, 20)) # Positions the subtitle

#Imput Frame
input_frame = tk.Frame(window)  # Creates a container for our inputs

input_frame.pack() # Places the input container in the window

#Description - LEFT
description_frame = tk.Frame(input_frame) # Creates a container for description
description_frame.grid(
    row=0, # Places it in the first row
    column=0, # Places it in the first column
    padx=15,  # Adds horizontal spacing
    pady=10  # Adds vertical spacing
) 

description_label = tk.Label(
    description_frame, # Places the label inside its frame
    text="Description" # Sets the label text
)
description_label.pack(anchor="w") # Aligns the label to the left

description_entry = tk.Entry(
    description_frame, # Places the input box inside its frame
    width=20  # Sets the input box width
)

description_entry.pack(pady=5)  # Positions the input box

#Amount - RIGHT 
amount_frame = tk.Frame(input_frame)  # Creates a container for amount

amount_frame.grid(
    row=0,  # Places it in the first row
    column=1,  # Places it in the second column
    padx=15, # Adds horizontal spacing
    pady=10 # Adds vertical spacing
)

amount_label = tk.Label(
    amount_frame,  # Places the label inside its frame
    text="Amount (R)"  # Sets the label text
)

amount_label.pack(anchor="w")  # Aligns the label to the left

amount_entry = tk.Entry(
    amount_frame, # Places the input box inside its frame
    width=20 # Sets the input box width
)

amount_entry.pack(pady=5)  # Positions the input box

#Category - LEFT 
category_frame = tk.Frame(input_frame)  # Creates a container for category

category_frame.grid(
    row=1, # Places it in the second row
    column=0,  # Places it in the first column
    columnspan=2,  # Uses both columns
    
    pady=10 # Adds vertical spacing
)

category_label = tk.Label(
    category_frame,  # Places the label inside its frame
    text="Category"  # Sets the label text
)

category_label.pack(anchor="w")  # Aligns the label to the left

category_combobox = ttk.Combobox(
    category_frame,  # Places the dropdown inside its frame
    values=[  # Provides the available categories
        "Food",
        "Transport",
        "Shopping",
        "Entertainment",
        "Bills",
        "Other"
    ],
    state="readonly",  # Prevents users from typing their own category
    width=22  # Sets the dropdown width
)

category_combobox.pack(pady=5) # Positions the dropdown

category_combobox.current(0) # Selects Food by default


#Expense Button 

def add_expense():
    description = description_entry.get()  # Gets the description
    amount = amount_entry.get()  # Gets the amount
    category = category_combobox.get()  # Gets the selected category

    # Check if the description is empty
    if description == "":
        messagebox.showerror(
            "Missing Description",
            "Please enter an expense description."
        )
        return

    # Check if the amount is a valid number
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror(
            "Invalid Amount",
            "Please enter a valid amount."
        )
        return

     # Check that the amount is greater than zero
    if amount <= 0:
        messagebox.showerror(
            "Invalid Amount",
            "Amount must be greater than zero."
        )
        return

    expense = Expense(
        description,
        amount,
        category
    )  # Creates an Expense object

    expenses.append(expense)  # Stores the Expense object
    expense_table.insert(
        "",
        tk.END,
        values=(
            expense.description,
            f"R{expense.amount:.2f}",
            expense.category
        )
    )  # Adds the expense to the table

    total = sum(expense.amount for expense in expenses)  # Calculates total spending - Take the amount from every Expense object and add them together.

    total_label.config(
    text=f"Total Spent: R{total:.2f}"
)  # Updates the total displayed on screen


  # Adds the expense as a new table row
add_button = tk.Button(
    window,  # Places the button in the main window
    text="Add Expense",  # Sets the button text
    width=20,  # Sets the button width
    command=add_expense  # Runs add_expense when clicked
)

add_button.pack(pady=10)  # Centers and positions the button

# Expense Table 
expense_table = ttk.Treeview(
    window,  # Places the table in the window
    columns=("description", "amount", "category"),  # Creates three columns
    show="headings",  # Hides the default Treeview column
    height=8  # Sets the number of visible rows
)

expense_table.heading(
    "description",
    text="Description"
    
)  # Sets the first column heading

expense_table.heading(
    "amount",
    text="Amount"
    
)  # Sets the second column heading

expense_table.heading(
    "category",
    text="Category", 
    
)  # Sets the third column heading

expense_table.column(
    "description",
    width=180,
    anchor="center"
)  # Sets description column width

expense_table.column(
    "amount",
    width=100, 
    anchor="center"
)  # Sets amount column width

expense_table.column(
    "category",
    width=150, 
    anchor="center"
)  # Sets category column width

expense_table.pack(pady=5)  # Displays the table

#Table Spent
total_label = tk.Label(
    window,  # Places the label in the main window
    text="Total Spent: R0.00",  # Sets the starting total
    font=("Arial", 12, "bold")  # Makes the total bold
)

total_label.pack(pady=10)  # Positions the total

# Keep the window running
window.mainloop()