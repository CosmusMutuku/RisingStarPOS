import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

# Connect to the database
conn = sqlite3.connect('C:/Users/user/rising_star_pos.db')
cursor = conn.cursor()

# Function to search for products based on product name
def search_product():
    product_name = product_entry.get()
    matching_products = []
    query = "SELECT * FROM product WHERE name LIKE ?"
    cursor.execute(query, ('%' + product_name + '%',))
    rows = cursor.fetchall()
    for row in rows:
        matching_products.append(row)
    show_search_results(matching_products)

# Create the main dashboard window
dashboard = tk.Tk()
dashboard.title("Inventory Management")
dashboard.configure(background="Blue")  # Add this line to set the background color


# Configure the shop name label
shop_name = "Rising Star Electronics"
shop_name_label = tk.Label(dashboard, text=shop_name, font=("Arial", 30, "bold italic"), fg="Green", bg="Yellow")
shop_name_label.pack(pady=30)

# Rest of the code for the shopping cart section
shopping_cart = []
cart_frame = tk.Frame(dashboard)  # Create a frame for the shopping cart display
cart_frame.pack(anchor=tk.W)  # Align the frame to the left side of the page

def add_to_cart(product):
    selected_product = product
    quantity = simpledialog.askinteger("Product Quantity", "Enter the quantity of the product to add to cart:")
    if quantity is not None:
        if quantity > 0:
            total_quantity = sum(item['quantity'] for item in shopping_cart if item['product_id'] == selected_product[0])
            available_quantity = selected_product[6] - total_quantity
            if quantity <= available_quantity:
                messagebox.showinfo("Product Added", f"Added {quantity} {selected_product[1]} to the cart.")
                shopping_cart.append({
                    'product_id': selected_product[0],
                    'product_name': selected_product[1],
                    'quantity': quantity,
                    'unit_price': selected_product[4]
                })
                show_shopping_cart()  # Update the shopping cart display
            else:
                messagebox.showinfo("Insufficient Quantity", "Insufficient quantity. Please try again with a lower quantity.")
        else:
            messagebox.showinfo("Invalid Quantity", "Invalid quantity. Please enter a positive value.")


def show_search_results(matching_products):
    results_window = tk.Toplevel(dashboard)
    results_window.title("Matching Products")
    results_window.geometry("500x300")

    for product in matching_products:
        product_label = tk.Label(results_window, text=f"Product: {product[1]}", font=("Arial", 14))
        product_label.pack()

        price_label = tk.Label(results_window, text=f"Price: {product[4]}", font=("Arial", 12))
        price_label.pack()

        quantity_label = tk.Label(results_window, text=f"Quantity: {product[6]}", font=("Arial", 12))
        quantity_label.pack()

        product_button = tk.Button(results_window, text="Select", command=lambda p=product: add_to_cart(p))
        product_button.pack()

def show_shopping_cart():
    for widget in cart_frame.winfo_children():  # Clear previous cart display
        widget.destroy()

    # Provisional Shopping Cart Heading
    heading_label = tk.Label(cart_frame, text="Provisional Shopping Cart", font=("Arial", 16, "bold"))
    heading_label.grid(row=0, column=0, columnspan=6, pady=(0, 10))

    # Subheadings
    subheading_number = tk.Label(cart_frame, text="", font=("Arial", 12, "bold"))
    subheading_number.grid(row=1, column=0, sticky=tk.W, padx=(5, 10))

    subheading_product = tk.Label(cart_frame, text="Item Name", font=("Arial", 12, "bold"))
    subheading_product.grid(row=1, column=1, sticky=tk.W)

    subheading_quantity = tk.Label(cart_frame, text="Quantity", font=("Arial", 12, "bold"))
    subheading_quantity.grid(row=1, column=2, sticky=tk.W)

    subheading_unit_price = tk.Label(cart_frame, text="Unit Price", font=("Arial", 12, "bold"))
    subheading_unit_price.grid(row=1, column=3, sticky=tk.W)

    subheading_amount = tk.Label(cart_frame, text="Amount", font=("Arial", 12, "bold"))
    subheading_amount.grid(row=1, column=4, sticky=tk.W)

    delete_label = tk.Label(cart_frame, text="Delete", font=("Arial", 12, "bold"))
    delete_label.grid(row=1, column=5, sticky=tk.W)

    total_price = 0
    product_quantities = {}  # Track quantities of each product

    # Calculate product quantities
    for item in shopping_cart:
        product_id = item['product_id']
        quantity = item['quantity']
        if product_id in product_quantities:
            product_quantities[product_id] += quantity
        else:
            product_quantities[product_id] = quantity

    # Display the added products in the cart with numbering
    index = 1
    for item in shopping_cart:
        product_id = item['product_id']
        product_name = item['product_name']
        quantity = item['quantity']
        unit_price = item['unit_price']
        amount = quantity * unit_price

        if product_quantities[product_id] > 0:
            # Display the item number
            number_label = tk.Label(cart_frame, text=index, font=("Arial", 12))
            number_label.grid(row=index+1, column=0, padx=(5, 10), sticky=tk.W)

            # Display the product, quantity, unit price, and amount
            product_label = tk.Label(cart_frame, text=product_name, font=("Arial", 12))
            product_label.grid(row=index+1, column=1, sticky=tk.W)

            quantity_label = tk.Label(cart_frame, text=quantity, font=("Arial", 12))
            quantity_label.grid(row=index+1, column=2)

            unit_price_label = tk.Label(cart_frame, text=unit_price, font=("Arial", 12))
            unit_price_label.grid(row=index+1, column=3)

            amount_label = tk.Label(cart_frame, text=amount, font=("Arial", 12))
            amount_label.grid(row=index+1, column=4)

            delete_button = tk.Button(cart_frame, text="Delete", font=("Arial", 12), command=lambda i=index-1: delete_item(i))
            delete_button.grid(row=index+1, column=5)

            total_price += amount
            product_quantities[product_id] -= quantity
            index += 1

    # Display the total price
    total_price_label = tk.Label(cart_frame, text=f"Total Price: {total_price}", font=("Arial", 12, "bold"))
    total_price_label.grid(row=index+1, columnspan=6, pady=(10, 0))

def delete_item(index):
    del shopping_cart[index]
    show_shopping_cart()  # Update the shopping cart display

# Product Entry
product_label = tk.Label(dashboard, text="Search Product by Name", font=("Arial", 12))
product_label.pack(pady=10)

product_entry = tk.Entry(dashboard, font=("Arial", 15))
product_entry.pack(pady=20)

product_entry.bind("<Return>", lambda event: search_product())  # Bind the Enter key to the search function

# Add to Cart Button
add_to_cart_button = tk.Button(dashboard, text="Add to Cart", font=("Arial", 12, "bold"), command=search_product, fg="Green", bg="Black")
add_to_cart_button.pack(pady=10)


# Complete Shopping Function
def complete_shopping():
    if len(shopping_cart) == 0:
        messagebox.showinfo("Empty Cart", "The shopping cart is empty. Please add products before completing the purchase.")
    else:
        payment_modes_frame = tk.Toplevel(dashboard)
        payment_modes_frame.title("Mode of Payment")
        payment_modes_frame.geometry("300x150")

        def select_payment_mode(mode):
            payment_modes_frame.destroy()
            if mode == "Other":
                other_payment_frame = tk.Toplevel(dashboard)
                other_payment_frame.title("Other Payment Mode")
                other_payment_frame.geometry("300x100")

                def continue_with_other():
                    other_payment_frame.destroy()
                    amount_received = simpledialog.askfloat("Amount Received", "Enter the amount received from the client:")
                    if amount_received is not None:
                        attendant_name = simpledialog.askstring("Attendant Name", "Enter the name of the attendant:")
                        if attendant_name is not None:
                            generate_receipt(other_mode_entry.get(), amount_received, attendant_name)
                        else:
                            messagebox.showinfo("Invalid Attendant Name", "Attendant name cannot be empty.")
                    else:
                        messagebox.showinfo("Invalid Amount Received", "Amount received cannot be empty.")

                other_label = tk.Label(other_payment_frame, text="Enter Other Payment Mode:", font=("Arial", 12))
                other_label.pack()

                other_mode_entry = tk.Entry(other_payment_frame, font=("Arial", 12))
                other_mode_entry.pack()

                continue_button = tk.Button(other_payment_frame, text="Continue", font=("Arial", 12), command=continue_with_other)
                continue_button.pack(pady=10)

            else:
                amount_received = simpledialog.askfloat("Amount Received", "Enter the amount received from the client:")
                if amount_received is not None:
                    attendant_name = simpledialog.askstring("Attendant Name", "Enter the name of the attendant:")
                    if attendant_name is not None:
                        generate_receipt(mode, amount_received, attendant_name)
                    else:
                        messagebox.showinfo("Invalid Attendant Name", "Attendant name cannot be empty.")
                else:
                    messagebox.showinfo("Invalid Amount Received", "Amount received cannot be empty.")

        cash_button = tk.Button(payment_modes_frame, text="Cash", font=("Arial", 12), command=lambda: select_payment_mode("Cash"))
        cash_button.pack(pady=10)

        mpesa_button = tk.Button(payment_modes_frame, text="M-Pesa", font=("Arial", 12), command=lambda: select_payment_mode("M-Pesa"))
        mpesa_button.pack(pady=10)

        # Remove the "Other" button option from here

def generate_receipt(payment_mode, amount_received, attendant_name):
    receipt_window = tk.Toplevel(dashboard)
    receipt_window.title("Receipt")
    receipt_window.geometry("600x400")

    # Rest of the generate_receipt() function code


    # Receipt Heading
    heading_label = tk.Label(receipt_window, text="Rising Star Electronics", font=("Arial", 20, "bold"))
    heading_label.pack(pady=20)

    # Receipt Subheadings
    subheading_label = tk.Label(receipt_window, text="Official Receipt", font=("Arial", 16))
    subheading_label.pack()

    contact_label = tk.Label(receipt_window, text="Contacts: +254708184901", font=("Arial", 12))
    contact_label.pack()

    # Receipt Shopping Cart
    cart_frame_clone = tk.Frame(receipt_window)
    cart_frame_clone.pack(anchor=tk.W)

    subheading_number_clone = tk.Label(cart_frame_clone, text="", font=("Arial", 12, "bold"))
    subheading_number_clone.grid(row=0, column=0, sticky=tk.W, padx=(5, 10))

    subheading_product_clone = tk.Label(cart_frame_clone, text="Item Name", font=("Arial", 12, "bold"))
    subheading_product_clone.grid(row=0, column=1, sticky=tk.W)

    subheading_quantity_clone = tk.Label(cart_frame_clone, text="Quantity", font=("Arial", 12, "bold"))
    subheading_quantity_clone.grid(row=0, column=2, sticky=tk.W)

    subheading_unit_price_clone = tk.Label(cart_frame_clone, text="Unit Price", font=("Arial", 12, "bold"))
    subheading_unit_price_clone.grid(row=0, column=3, sticky=tk.W)

    subheading_amount_clone = tk.Label(cart_frame_clone, text="Amount", font=("Arial", 12, "bold"))
    subheading_amount_clone.grid(row=0, column=4, sticky=tk.W)

    total_price = 0

    for index, item in enumerate(shopping_cart, start=1):
        product_name = item['product_name']
        quantity = item['quantity']
        unit_price = item['unit_price']
        amount = quantity * unit_price

        number_label_clone = tk.Label(cart_frame_clone, text=index, font=("Arial", 12))
        number_label_clone.grid(row=index, column=0, padx=(5, 10), sticky=tk.W)

        product_label_clone = tk.Label(cart_frame_clone, text=product_name, font=("Arial", 12))
        product_label_clone.grid(row=index, column=1, sticky=tk.W)

        quantity_label_clone = tk.Label(cart_frame_clone, text=quantity, font=("Arial", 12))
        quantity_label_clone.grid(row=index, column=2)

        unit_price_label_clone = tk.Label(cart_frame_clone, text=unit_price, font=("Arial", 12))
        unit_price_label_clone.grid(row=index, column=3)

        amount_label_clone = tk.Label(cart_frame_clone, text=amount, font=("Arial", 12))
        amount_label_clone.grid(row=index, column=4)

        total_price += amount

    total_label_clone = tk.Label(cart_frame_clone, text=f"Total Price: {total_price}", font=("Arial", 14, "bold"), fg="blue")
    total_label_clone.grid(row=len(shopping_cart)+1, column=4, sticky=tk.E, padx=10, pady=10)

    # Payment Details
    payment_mode_label = tk.Label(receipt_window, text=f"Payment Mode: {payment_mode}", font=("Arial", 12))
    payment_mode_label.pack(pady=10)

    amount_received_label = tk.Label(receipt_window, text=f"Amount Received: {amount_received}", font=("Arial", 12))
    amount_received_label.pack()

    change_label = tk.Label(receipt_window, text=f"Change: {amount_received - total_price}", font=("Arial", 12))
    change_label.pack()

    # Attendant Details
    attendant_label = tk.Label(receipt_window, text=f"Attendant: {attendant_name}", font=("Arial", 12))
    attendant_label.pack(pady=20)

# Complete Button
complete_button = tk.Button(dashboard, text="Complete", font=("Arial", 14, "bold"), command=complete_shopping, fg="Red", bg="Black")
complete_button.pack(pady=20)


# Run the dashboard
dashboard.mainloop()
