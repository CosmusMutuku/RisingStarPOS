# -*- coding: utf-8 -*-
"""Main Dashboard.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KuIOaZCjPlLWh3_xMdN0JfmAmtTGc75Q

## Main Dashboard
"""

import tkinter as tk

# Create the main dashboard window
dashboard_window = tk.Tk()
dashboard_window.title("Main Dashboard")
dashboard_window.geometry("800x600")

# Add shop name label
shop_name_label = tk.Label(dashboard_window, text="Your Shop Name", font=("Arial", 20, "bold"))
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
