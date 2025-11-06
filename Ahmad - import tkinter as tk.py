import tkinter as tk
from tkinter import messagebox

# Menu data (Dictionary)
menu = {
    1: {"name": "Espresso", "price": 4.00},
    2: {"name": "Americano", "price": 4.20},
    3: {"name": "Flat White", "price": 4.80},
    4: {"name": "Cappuccino", "price": 4.50},
    5: {"name": "Latte", "price": 5.00},
    6: {"name": "Mocha", "price": 5.50},
    7: {"name": "Iced Coffee", "price": 5.30},
    8: {"name": "Croissant", "price": 3.50},
    9: {"name": "Muffin", "price": 3.00},
    10: {"name": "Donut", "price": 3.20}
}

order = []  # List to store selected items

# Add item to order
def add_item(item_id):
    try:
        order.append(menu[item_id])
        update_order_list()
    except KeyError:
        messagebox.showerror("Error", "Invalid item!")

# Update order list display
def update_order_list():
    order_list.delete(0, tk.END)
    total = 0
    for item in order:
        order_list.insert(tk.END, f"{item['name']} - ${item['price']:.2f}")
        total += item["price"]
    total_label.config(text=f"Total: ${total:.2f}")

# Checkout and apply discount
def checkout():
    try:
        total = sum(item["price"] for item in order)
        discount = 0

        # Discount by code
        code = discount_code.get().strip().lower()
        if code == "10off":
            discount = total * 0.10

        final_total = total - discount
        payment_method = payment_var.get()

        if not order:
            messagebox.showwarning("Warning", "No items in the order!")
            return

        summary = (
            f"Payment: {payment_method}\n"
            f"Subtotal: ${total:.2f}\n"
            f"Discount: ${discount:.2f}\n"
            f"Final Total: ${final_total:.2f}\n\nThank you!"
        )
        messagebox.showinfo("Order Summary", summary)

        # Clear order for next customer
        order.clear()
        discount_code.delete(0, tk.END)
        update_order_list()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("Coffee Shop System")
root.geometry("420x600")
root.config(bg="#f2f2f2")

# Title
tk.Label(root, text="☕ Coffee Shop Menu", font=("Arial", 16, "bold"), bg="#f2f2f2").pack(pady=10)

menu_frame = tk.Frame(root, bg="#f2f2f2")
menu_frame.pack()

# Section: Coffee
tk.Label(menu_frame, text="☕ Coffee", font=("Arial", 13, "bold"), bg="#f2f2f2").pack(pady=(5, 2))
for i in range(1, 8):
    item = menu[i]
    tk.Button(menu_frame, text=f"{i}. {item['name']} - ${item['price']:.2f}",
              command=lambda i=i: add_item(i), width=30, bg="#d9ead3").pack(pady=2)

# Section: Pastries
tk.Label(menu_frame, text="🥐 Pastries", font=("Arial", 13, "bold"), bg="#f2f2f2").pack(pady=(10, 2))
for i in range(8, 11):
    item = menu[i]
    tk.Button(menu_frame, text=f"{i}. {item['name']} - ${item['price']:.2f}",
              command=lambda i=i: add_item(i), width=30, bg="#fce5cd").pack(pady=2)

# Order display
tk.Label(root, text="🧾 Your Order:", font=("Arial", 12, "bold"), bg="#f2f2f2").pack(pady=10)
order_list = tk.Listbox(root, width=45, height=7)
order_list.pack()

total_label = tk.Label(root, text="Total: $0.00", font=("Arial", 12, "bold"), bg="#f2f2f2")
total_label.pack(pady=5)

# Discount code entry
tk.Label(root, text="Enter Discount Code:", font=("Arial", 11), bg="#f2f2f2").pack()
discount_code = tk.Entry(root, width=20)
discount_code.pack(pady=5)

# Payment method (default = Cash)
tk.Label(root, text="Select Payment Method:", font=("Arial", 11), bg="#f2f2f2").pack()
payment_var = tk.StringVar(value="Cash")  # default = Cash
tk.Radiobutton(root, text="Cash", variable=payment_var, value="Cash", bg="#f2f2f2").pack()
tk.Radiobutton(root, text="Card", variable=payment_var, value="Card", bg="#f2f2f2").pack()

# Checkout button
tk.Button(root, text="Checkout", command=checkout, bg="#a4c2f4",
          font=("Arial", 12, "bold"), width=22).pack(pady=15)

root.mainloop()
