# -*- coding: utf-8 -*-
"""Inventory Management.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iC2XlESjjxHJ3AgT8EMPZJsi_hwzWLUW

## Inventory Managemement
"""

import sqlite3

# Connect to the database
conn = sqlite3.connect('C:\Users\user\rising_star_pos.db')
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