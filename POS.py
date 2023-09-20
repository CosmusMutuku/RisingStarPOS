# -*- coding: utf-8 -*-
"""POS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1G39JquGh1YsF2ZhwgwvOOenWDUsE18Tk

## Main Dashboard
"""

import tkinter as tk

# Create the main dashboard window
dashboard_window = tk.Tk()
dashboard_window.title("Main Dashboard")
dashboard_window.geometry("800x600")

# Add shop name label
shop_name_label = tk.Label(dashboard_window, text="Rising Star Electronics", font=("Arial", 35, "bold"))
shop_name_label.pack(pady=20)

# Add recent total margin label
recent_margin_label = tk.Label(dashboard_window, text="Recent Total Margin: $XXX")
recent_margin_label.pack()

# Add recent total transactions label
recent_transactions_label = tk.Label(dashboard_window, text="Recent Total Transactions: XX")
recent_transactions_label.pack()

# Add total margin generated label
total_margin_label = tk.Label(dashboard_window, text="Total Margin Generated: $XXX")
total_margin_label.pack()

# Add inventory status section
inventory_frame = tk.Frame(dashboard_window)
inventory_frame.pack(pady=20)

inventory_label = tk.Label(inventory_frame, text="Inventory Status", font=("Arial", 16, "bold"))
inventory_label.pack()

# Add inventory categories
categories = ["Products to Restock", "Low Stock", "Adequate Stock", "Plenty Stock"]
for category in categories:
    category_label = tk.Label(inventory_frame, text=category)
    category_label.pack()

dashboard_window.mainloop()


"""## Shopping Cart"""

import sqlite3

# Connect to the database
conn = sqlite3.connect('C:/Users/user/rising_star_pos.db')
cursor = conn.cursor()

# Function to search for products based on product name
def search_product(product_name):
    matching_products = []
    query = "SELECT * FROM product WHERE name LIKE ?"
    cursor.execute(query, ('%' + product_name + '%',))
    rows = cursor.fetchall()
    for row in rows:
        matching_products.append(row)
    return matching_products

# Create an empty shopping cart
shopping_cart = []

# Loop for selecting and adding products
while True:
    # Prompt for the product name
    product_name = input("Enter the product name: ")

    # Search for the product in the inventory
    matching_products = search_product(product_name)

    # Check if any matching products found
    if len(matching_products) == 0:
        print("No matching products found. Please recheck the spelling.")
        continue  # Restart the loop to search again

    # Display the matching products
    print("Matching Products:")
    for i, product in enumerate(matching_products):
        print("Product ID:", product[0])
        print("Name:", product[1])
        print("Selling Price:", product[4])
        print("Quantity:", product[6])
        print("------------------------")

    # Prompt for selecting a product
    selected_product_id = input("Enter the product ID to select: ")

    # Retrieve the selected product from the inventory
    selected_product = None
    for product in matching_products:
        if str(product[0]) == selected_product_id:
            selected_product = product
            break

    # Check if the selected product exists
    if selected_product:
        print("Selected Product:")
        print("Product ID:", selected_product[0])
        print("Name:", selected_product[1])
        print("Selling Price:", selected_product[4])
        print("Quantity:", selected_product[6])
        print("------------------------")

        # Prompt for the quantity of the product
        quantity = input("Enter the quantity of the product to add to cart: ")

        # Check if the quantity input is valid
        if quantity.isdigit():
            quantity = int(quantity)
            if quantity > 0:
                # Check if the requested quantity is available
                if quantity <= selected_product[6]:
                    print(f"Added {quantity} {selected_product[1]} to the cart.")
                    # Add the selected product with the requested quantity to the shopping cart
                    shopping_cart.append({
                        'product_id': selected_product[0],
                        'product_name': selected_product[1],
                        'quantity': quantity,
                        'unit_price': selected_product[4]
                    })
                else:
                    print("Insufficient quantity. Please try again with a lower quantity.")
                    continue  # Restart the loop to select another product

                # Prompt to add another product or complete the cart
                choice = input("Do you want to add another product? (Y/N): ")
                if choice.lower() != "y":
                    break
            else:
                print("Invalid quantity. Please enter a positive value.")
        else:
            print("Invalid input. Please enter a valid quantity.")
    else:
        print("Invalid product ID. Please try again.")

# Display the shopping cart
print("Shopping Cart:")
total_price = 0
for item in shopping_cart:
    product_name = item['product_name']
    quantity = item['quantity']
    unit_price = item['unit_price']
    amount = quantity * unit_price
    total_price += amount

    print("Product:", product_name)
    print("Amount:", amount)
    print("Quantity:", quantity)
    print("Unit Price:", unit_price)
    print("------------------------")

print("Total Price:", total_price)

# Calculate change
payment_mode = input("Enter the payment mode (cash, card, or mpesa): ")
amount_received = float(input("Enter the amount received from the customer: "))

if payment_mode.lower() == "cash":
    change = amount_received - total_price
    print("Change:", change)
else:
    print("Payment mode not supported for change calculation.")

# Close the database connection
conn.close()

"""## Payment Processing"""

import sqlite3

# Connect to the database
conn = sqlite3.connect('C:/Users/user/rising_star_pos.db')
cursor = conn.cursor()

# Function to search for products based on product name
def search_product(product_name):
    matching_products = []
    query = "SELECT * FROM product WHERE name LIKE ?"
    cursor.execute(query, ('%' + product_name + '%',))
    rows = cursor.fetchall()
    for row in rows:
        matching_products.append(row)
    return matching_products

# Create an empty shopping cart
shopping_cart = []

# Loop for selecting and adding products
while True:
    # Prompt for the product name
    product_name = input("Enter the product name: ")

    # Search for the product in the inventory
    matching_products = search_product(product_name)

    # Check if any matching products found
    if len(matching_products) == 0:
        print("No matching products found. Please recheck the spelling.")
        continue  # Restart the loop to search again

    # Display the matching products
    print("Matching Products:")
    for i, product in enumerate(matching_products):
        print("Product ID:", product[0])
        print("Name:", product[1])
        print("Selling Price:", product[4])
        print("Quantity:", product[6])
        print("------------------------")

    # Prompt for selecting a product
    selected_product_id = input("Enter the product ID to select: ")

    # Retrieve the selected product from the inventory
    selected_product = None
    for product in matching_products:
        if str(product[0]) == selected_product_id:
            selected_product = product
            break

    # Check if the selected product exists
    if selected_product:
        print("Selected Product:")
        print("Product ID:", selected_product[0])
        print("Name:", selected_product[1])
        print("Selling Price:", selected_product[4])
        print("Quantity:", selected_product[6])
        print("------------------------")

        # Prompt for the quantity of the product
        quantity = input("Enter the quantity of the product to add to cart: ")

        # Check if the quantity input is valid
        if quantity.isdigit():
            quantity = int(quantity)
            if quantity > 0:
                # Check if the requested quantity is available
                if quantity <= selected_product[6]:
                    print(f"Added {quantity} {selected_product[1]} to the cart.")
                    # Add the selected product with the requested quantity to the shopping cart
                    shopping_cart.append({
                        'product_id': selected_product[0],
                        'product_name': selected_product[1],
                        'quantity': quantity,
                        'unit_price': selected_product[4]
                    })
                else:
                    print("Insufficient quantity. Please try again with a lower quantity.")
                    continue  # Restart the loop to select another product

                # Prompt to add another product or complete the cart
                choice = input("Do you want to add another product? (Y/N): ")
                if choice.lower() != "y":
                    break
            else:
                print("Invalid quantity. Please enter a positive value.")
        else:
            print("Invalid input. Please enter a valid quantity.")
    else:
        print("Invalid product ID. Please try again.")

# Display the shopping cart
print("Shopping Cart:")
total_price = 0
for item in shopping_cart:
    product_name = item['product_name']
    quantity = item['quantity']
    unit_price = item['unit_price']
    amount = quantity * unit_price
    total_price += amount
    print("Product:", product_name)
    print("Quantity:", quantity)
    print("Unit Price:", unit_price)
    print("Amount:", amount)
    print("------------------------")

# Prompt to display the total amount the customer needs to pay
display_total = input("Do you want to display the total amount the customer needs to pay? (Y/N): ")
if display_total.lower() == "y":
    print("Total Price:", total_price)

# Calculate change
payment_mode = input("Enter the payment mode (cash, card, or mpesa): ")
amount_received = float(input("Enter the amount received from the customer: "))

if payment_mode.lower() == "cash":
    change = amount_received - total_price
    print("Change:", change)
else:
    print("Payment mode not supported for change calculation.")

# Prompt for the attendant's name
attendant_name = input("Enter the name of the service provider (attendant): ")

# Prompt to print the receipt
print_receipt = input("Do you want to print the receipt? (Y/N): ")

if print_receipt.lower() == "y":
    print("\n")
    print("Rising Star Electronics")
    print("------------------------------")
    print("Attendant:", attendant_name)
    print("------------------------------")
    print("Product\t\tQuantity\tUnit Price\tAmount")
    print("------------------------------")
    for item in shopping_cart:
        product_name = item['product_name']
        quantity = item['quantity']
        unit_price = item['unit_price']
        amount = quantity * unit_price
        print(f"{product_name}\t\t{quantity}\t\t{unit_price}\t\t{amount}")
    print("------------------------------")
    print("Total Price:", total_price)
    print("Amount Paid:", amount_received)
    print("Change Received:", change)
    print("Payment Mode:", payment_mode)
    print("------------------------------")
    print("Thank you for shopping with us!")
    print("Visit us again for quality assured products at well-considered prices.")
    print("------------------------------")

# Close the database connection
conn.close()

"""## Inventory Management"""

import sqlite3

# Connect to the database
conn = sqlite3.connect('C:/Users/user/rising_star_pos.db')
cursor = conn.cursor()

# Function to get the category ID based on the description
def get_category_id(description):
    # Check if the description already exists in the database
    query = "SELECT category_id FROM product WHERE description = ?"
    cursor.execute(query, (description,))
    category_id = cursor.fetchone()

    # If the description exists, return the category ID
    if category_id:
        return category_id[0]

    # If the description is new, insert it into the database and return the newly generated category ID
    query = "INSERT INTO category (description) VALUES (?)"
    cursor.execute(query, (description,))
    conn.commit()

    return cursor.lastrowid

# Function to add a new product
def add_product():
    product_name = input("Enter the product name: ")
    buying_price = float(input("Enter the buying price: "))
    selling_price = float(input("Enter the selling price: "))
    quantity = int(input("Enter the quantity: "))
    alert_quantity = int(input("Enter the low stock alert quantity: "))
    description = input("Enter the description: ")

    category_id = get_category_id(description)

    query = "INSERT INTO product (name, buying_price, selling_price, quantity, alert_quantity, description, category_id) VALUES (?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(query, (product_name, buying_price, selling_price, quantity, alert_quantity, description, category_id))
    conn.commit()
    print("New product added successfully.")

# Function to update the buying price of a product
def update_buying_price():
    product_name = input("Enter the product name: ")
    query = "SELECT product_id, name, buying_price FROM product WHERE name LIKE ?"
    cursor.execute(query, ('%' + product_name + '%',))
    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No matching products found.")
        return

    print("Matching Products:")
    print("------------------")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Buying Price: {row[2]}")

    product_id = None
    while product_id is None:
        try:
            product_id = int(input("Enter the product ID: "))
            if product_id not in [row[0] for row in rows]:
                print("Invalid product ID. Please recheck and enter a valid product ID.")
                product_id = None
        except ValueError:
            print("Invalid input. Please enter a valid product ID.")

    new_buying_price = float(input("Enter the new buying price: "))

    query = "UPDATE product SET buying_price = ? WHERE product_id = ?"
    cursor.execute(query, (new_buying_price, product_id))
    conn.commit()
    print("Buying price updated successfully.")

# Function to update the selling price of a product
def update_selling_price():
    product_name = input("Enter the product name: ")
    query = "SELECT product_id, name, selling_price FROM product WHERE name LIKE ?"
    cursor.execute(query, ('%' + product_name + '%',))
    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No matching products found.")
        return

    print("Matching Products:")
    print("------------------")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Selling Price: {row[2]}")

    product_id = None
    while product_id is None:
        try:
            product_id = int(input("Enter the product ID: "))
            if product_id not in [row[0] for row in rows]:
                print("Invalid product ID. Please recheck and enter a valid product ID.")
                product_id = None
        except ValueError:
            print("Invalid input. Please enter a valid product ID.")

    new_selling_price = float(input("Enter the new selling price: "))

    query = "UPDATE product SET selling_price = ? WHERE product_id = ?"
    cursor.execute(query, (new_selling_price, product_id))
    conn.commit()
    print("Selling price updated successfully.")

# Function to receive new stock for a product
def receive_new_stock():
    product_name = input("Enter the product name: ")
    query = "SELECT product_id, name, quantity FROM product WHERE name LIKE ?"
    cursor.execute(query, ('%' + product_name + '%',))
    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No matching products found.")
        return

    print("Matching Products:")
    print("------------------")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Quantity: {row[2]}")

    product_id = None
    while product_id is None:
        try:
            product_id = int(input("Enter the product ID: "))
            if product_id not in [row[0] for row in rows]:
                print("Invalid product ID. Please recheck and enter a valid product ID.")
                product_id = None
        except ValueError:
            print("Invalid input. Please enter a valid product ID.")

    quantity = int(input("Enter the new stock quantity: "))

    query = "UPDATE product SET quantity = quantity + ? WHERE product_id = ?"
    cursor.execute(query, (quantity, product_id))
    conn.commit()
    print("New stock received successfully.")

# Function to set the low stock alert for a product
def set_low_stock_alert():
    product_name = input("Enter the product name: ")
    query = "SELECT product_id, name, alert_quantity FROM product WHERE name LIKE ?"
    cursor.execute(query, ('%' + product_name + '%',))
    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No matching products found.")
        return

    print("Matching Products:")
    print("------------------")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Low Stock Alert: {row[2]}")

    product_id = None
    while product_id is None:
        try:
            product_id = int(input("Enter the product ID: "))
            if product_id not in [row[0] for row in rows]:
                print("Invalid product ID. Please recheck and enter a valid product ID.")
                product_id = None
        except ValueError:
            print("Invalid input. Please enter a valid product ID.")

    alert_quantity = int(input("Enter the low stock alert quantity: "))

    query = "UPDATE product SET alert_quantity = ? WHERE product_id = ?"
    cursor.execute(query, (alert_quantity, product_id))
    conn.commit()
    print("Low stock alert set successfully.")

# Inventory Management Menu
def inventory_management_menu():
    while True:
        print("\nInventory Management Menu:")
        print("1. Add New Product")
        print("2. Update Buying Price")
        print("3. Update Selling Price")
        print("4. Receive New Stock")
        print("5. Set Low Stock Alert")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            update_buying_price()
        elif choice == "3":
            update_selling_price()
        elif choice == "4":
            receive_new_stock()
        elif choice == "5":
            set_low_stock_alert()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

# Run the inventory management menu
inventory_management_menu()

# Close the database connection
conn.close()