import tkinter as tk
from tkinter import messagebox
import sqlite3

# Connect to the database
conn = sqlite3.connect(r'C:\Users\user\rising_star_pos.db')
cursor = conn.cursor()

# Create the main window
window = tk.Tk()
window.title("Inventory Management System")

# Function to check if a string can be converted to a numeric value
def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Function to check and display alert for low quantity
def check_alert(product_name, quantity):
    alert_threshold = 10  # Define your alert threshold here

    if int(quantity) <= alert_threshold:
        messagebox.showwarning("Alert", f"Low quantity for {product_name}. Current quantity: {quantity}")

# Create the add product functionality
def add_product():
    add_product_window = tk.Toplevel(window)
    add_product_window.title("Add New Product")

    def submit_form():
        name = name_entry.get()
        buying_price = buying_price_entry.get()
        selling_price = selling_price_entry.get()
        quantity = quantity_entry.get()

        # Validate numeric input for buying price, selling price, and quantity
        if not is_numeric(buying_price) or not is_numeric(selling_price) or not is_numeric(quantity):
            messagebox.showerror("Invalid Input", "Please enter numeric values for buying price, selling price, and quantity.")
            return

        # Insert the new product into the database
        cursor.execute("INSERT INTO Product (name, buying_price, selling_price, quantity) VALUES (?, ?, ?, ?)",
                       (name, buying_price, selling_price, quantity))
        conn.commit()

        # Check for alert
        check_alert(name, quantity)

        # Show a success message
        messagebox.showinfo("Success", "Product added successfully!")

        add_product_window.destroy()

    name_label = tk.Label(add_product_window, text="Name:")
    name_label.pack()
    name_entry = tk.Entry(add_product_window)
    name_entry.pack()

    buying_price_label = tk.Label(add_product_window, text="Buying Price:")
    buying_price_label.pack()
    buying_price_entry = tk.Entry(add_product_window)
    buying_price_entry.pack()

    selling_price_label = tk.Label(add_product_window, text="Selling Price:")
    selling_price_label.pack()
    selling_price_entry = tk.Entry(add_product_window)
    selling_price_entry.pack()

    quantity_label = tk.Label(add_product_window, text="Quantity:")
    quantity_label.pack()
    quantity_entry = tk.Entry(add_product_window)
    quantity_entry.pack()

    submit_button = tk.Button(add_product_window, text="Submit", command=submit_form)
    submit_button.pack(pady=10)

# Create the update prices functionality
def update_prices():
    search_product_window = tk.Toplevel(window)
    search_product_window.title("Search and Select Product")

    def search_and_select_product():
        search_term = name_entry.get()

        # Perform the database query to search and filter products by name
        cursor.execute("SELECT name FROM Product WHERE name LIKE ?", ('%' + search_term + '%',))
        search_result = cursor.fetchall()

        search_product_window.destroy()
        select_product_window = tk.Toplevel(window)
        select_product_window.title("Select Product")

        def select_product(product_name):
            select_product_window.destroy()
            update_prices_window = tk.Toplevel(window)
            update_prices_window.title("Update Buying/Selling Prices")

            def submit_form():
                buying_price = buying_price_entry.get()
                selling_price = selling_price_entry.get()

                # Validate numeric input for buying price and selling price
                if not is_numeric(buying_price) or not is_numeric(selling_price):
                    messagebox.showerror("Invalid Input", "Please enter numeric values for buying price and selling price.")
                    return

                # Update the buying price and selling price in the database
                cursor.execute("UPDATE Product SET buying_price = ?, selling_price = ? WHERE name = ?",
                               (buying_price, selling_price, product_name))
                conn.commit()

                # Check for alert
                cursor.execute("SELECT quantity FROM Product WHERE name = ?", (product_name,))
                quantity = cursor.fetchone()[0]
                check_alert(product_name, quantity)

                # Show a success message
                messagebox.showinfo("Success", "Prices updated successfully!")

                update_prices_window.destroy()

            buying_price_label = tk.Label(update_prices_window, text="Buying Price:")
            buying_price_label.pack()
            buying_price_entry = tk.Entry(update_prices_window)
            buying_price_entry.pack()

            selling_price_label = tk.Label(update_prices_window, text="Selling Price:")
            selling_price_label.pack()
            selling_price_entry = tk.Entry(update_prices_window)
            selling_price_entry.pack()

            submit_button = tk.Button(update_prices_window, text="Submit", command=submit_form)
            submit_button.pack(pady=10)

            # Check for alert
            cursor.execute("SELECT quantity FROM Product WHERE name = ?", (product_name,))
            quantity = cursor.fetchone()[0]
            check_alert(product_name, quantity)

            stock_button = tk.Button(update_prices_window, text="Stock", command=lambda: show_stock(product_name))
            stock_button.pack(side="left", padx=5)

            back_button = tk.Button(update_prices_window, text="Back", command=update_prices_window.destroy)
            back_button.pack(side="right", padx=5)

        for product in search_result:
            product_name = product[0]
            product_button = tk.Button(select_product_window, text=product_name, command=lambda name=product_name: select_product(name))
            product_button.pack(pady=5)

    name_label = tk.Label(search_product_window, text="Search Product:")
    name_label.pack()
    name_entry = tk.Entry(search_product_window)
    name_entry.pack()

    search_button = tk.Button(search_product_window, text="Search", command=search_and_select_product)
    search_button.pack(pady=10)

# Create the function to display the stock for a selected product
def show_stock(product_name):
    stock_window = tk.Toplevel(window)
    stock_window.title("Stock")

    cursor.execute("SELECT quantity FROM Product WHERE name = ?", (product_name,))
    quantity = cursor.fetchone()[0]

    stock_label = tk.Label(stock_window, text=f"Stock for {product_name}: {quantity}")
    stock_label.pack(pady=10)

    back_button = tk.Button(stock_window, text="Back", command=stock_window.destroy)
    back_button.pack(pady=5)

# Create the menu bar
menu_bar = tk.Menu(window)

# Create the File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Exit", command=window.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Create the Inventory menu
inventory_menu = tk.Menu(menu_bar, tearoff=0)
inventory_menu.add_command(label="Add Product", command=add_product)
inventory_menu.add_command(label="Update Prices", command=update_prices)
menu_bar.add_cascade(label="Inventory", menu=inventory_menu)

# Configure the window to use the menu bar
window.config(menu=menu_bar)

# Start the Tkinter event loop
window.mainloop()
