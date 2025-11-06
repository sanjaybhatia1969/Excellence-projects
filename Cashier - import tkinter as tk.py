import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# ------------------------------
# Menu Data
# ------------------------------
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

order = []
order_history = {}
next_order_number = 1001


# ------------------------------
# Add item to order
# ------------------------------
def add_item(item_id):
    order.append(menu[item_id])
    update_order_list()


# ------------------------------
# Update current order display
# ------------------------------
def update_order_list():
    order_list.delete(0, tk.END)
    total = sum(item["price"] for item in order)
    for item in order:
        order_list.insert(tk.END, f"{item['name']} - ${item['price']:.2f}")
    total_label.config(text=f"Total: ${total:.2f}")


# ------------------------------
# Checkout
# ------------------------------
def checkout():
    global next_order_number
    if not order:
        messagebox.showwarning("Warning", "No items in the order!")
        return

    total = sum(item["price"] for item in order)
    discount = 0
    code_used = discount_code.get().strip().lower()
    if code_used == "10off":
        discount = total * 0.10

    final_total = total - discount
    payment_method = payment_var.get()
    order_number = next_order_number
    next_order_number += 1
    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save order (including discount info)
    order_history[order_number] = {
        "date": order_date,
        "items": list(order),
        "total": final_total,
        "payment": payment_method,
        "discount": discount,
        "discount_used": (code_used == "10off")
    }

    # Summary popup
    summary = (
        f"Order Number: #{order_number}\n"
        f"Date: {order_date}\n"
        f"Payment: {payment_method}\n"
        f"Subtotal: ${total:.2f}\n"
        f"Discount: ${discount:.2f}\n"
        f"Final Total: ${final_total:.2f}\n\nThank you!"
    )
    messagebox.showinfo("Order Completed", summary)

    print_receipt(order_number)
    order.clear()
    discount_code.delete(0, tk.END)
    update_order_list()


# ------------------------------
# Print Receipt (with 10% off info)
# ------------------------------
def print_receipt(order_number):
    if order_number not in order_history:
        messagebox.showerror("Error", "Order not found!")
        return

    data = order_history[order_number]
    r = tk.Toplevel(root)
    r.title(f"Receipt - Order #{order_number}")
    r.geometry("350x420")
    r.config(bg="white")

    t = tk.Text(r, wrap=tk.WORD, font=("Courier", 10))
    t.pack(padx=10, pady=10, fill="both", expand=True)

    t.insert(tk.END, "      ☕ Coffee Shop Receipt ☕\n")
    t.insert(tk.END, "-------------------------------------\n")
    t.insert(tk.END, f"Order Number: #{order_number}\n")
    t.insert(tk.END, f"Date: {data['date']}\n")
    t.insert(tk.END, f"Payment: {data['payment']}\n")
    t.insert(tk.END, "-------------------------------------\n")

    subtotal = sum(item["price"] for item in data["items"])
    for item in data["items"]:
        t.insert(tk.END, f"{item['name']:<20} ${item['price']:.2f}\n")

    t.insert(tk.END, "-------------------------------------\n")
    t.insert(tk.END, f"Subtotal: ${subtotal:.2f}\n")
    if data.get("discount_used"):
        t.insert(tk.END, f"Discount (10% off): -${data['discount']:.2f}\n")
    t.insert(tk.END, f"Total: ${data['total']:.2f}\n")
    t.insert(tk.END, "-------------------------------------\n")
    t.insert(tk.END, "Thank you! Please come again.\n")
    t.config(state="disabled")


# ------------------------------
# Refund (Multi-Select)
# ------------------------------
def open_refund_window(order_number):
    if order_number not in order_history:
        messagebox.showwarning("Not Found", f"Order #{order_number} not found!")
        return

    order_data = order_history[order_number]
    items = order_data["items"]

    win = tk.Toplevel(root)
    win.title(f"Refund - Order #{order_number}")
    win.geometry("340x340")
    win.config(bg="#f2f2f2")

    tk.Label(win, text=f"Order #{order_number} Items:",
             font=("Arial", 12, "bold"), bg="#f2f2f2").pack(pady=5)

    lb = tk.Listbox(win, width=38, height=10, selectmode=tk.MULTIPLE)
    lb.pack(pady=5)
    for item in items:
        lb.insert(tk.END, f"{item['name']} - ${item['price']:.2f}")

    def process_refund():
        selected_indices = list(lb.curselection())
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select items to refund.")
            return

        refunded_items = []
        selected_indices.sort(reverse=True)
        for idx in selected_indices:
            refunded_items.append(items.pop(idx))
            lb.delete(idx)

        total_refunded = sum(i["price"] for i in refunded_items)
        messagebox.showinfo("Refund Complete",
                            f"Refunded {len(refunded_items)} items\nTotal: ${total_refunded:.2f}")

        order_data["total"] = sum(i["price"] for i in items)
        if not items:
            del order_history[order_number]
            win.destroy()
            messagebox.showinfo("Order Closed",
                                f"Order #{order_number} fully refunded and removed.")

    tk.Button(win, text="Refund Selected Items", command=process_refund,
              bg="#f4cccc", font=("Arial", 11, "bold"), width=25).pack(pady=10)


# ------------------------------
# View All Orders (with Refund)
# ------------------------------
def view_all_orders():
    if not order_history:
        messagebox.showinfo("No Orders", "No orders have been made yet.")
        return

    hist = tk.Toplevel(root)
    hist.title("All Orders History")
    hist.geometry("450x400")
    hist.config(bg="#f2f2f2")

    tk.Label(hist, text="🧾 All Orders", font=("Arial", 13, "bold"), bg="#f2f2f2").pack(pady=10)

    lb = tk.Listbox(hist, width=60, height=15)
    lb.pack(padx=10, pady=5)
    for num, info in order_history.items():
        lb.insert(tk.END, f"Order #{num} | {info['date']} | ${info['total']:.2f} | {info['payment']}")

    def open_selected_order():
        sel = lb.curselection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select an order.")
            return
        line = lb.get(sel[0])
        order_no = int(line.split("#")[1].split()[0])
        open_refund_window(order_no)

    def open_receipt():
        sel = lb.curselection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select an order.")
            return
        line = lb.get(sel[0])
        order_no = int(line.split("#")[1].split()[0])
        print_receipt(order_no)

    btn_frame = tk.Frame(hist, bg="#f2f2f2")
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="View Receipt", command=open_receipt,
              bg="#a4c2f4", width=15, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Refund This Order", command=open_selected_order,
              bg="#f4cccc", width=15, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)

    lb.bind("<Double-1>", lambda e: open_receipt())


# ------------------------------
# GUI Setup
# ------------------------------
root = tk.Tk()
root.title("Coffee Shop System")
root.geometry("520x820")
root.config(bg="#f2f2f2")

tk.Label(root, text="☕ Coffee Shop Menu", font=("Arial", 16, "bold"), bg="#f2f2f2").pack(pady=10)

menu_frame = tk.Frame(root, bg="#f2f2f2")
menu_frame.pack()

tk.Label(menu_frame, text="☕ Coffee", font=("Arial", 13, "bold"), bg="#f2f2f2").pack()
for i in range(1, 8):
    item = menu[i]
    tk.Button(menu_frame, text=f"{i}. {item['name']} - ${item['price']:.2f}",
              command=lambda i=i: add_item(i), width=30, bg="#d9ead3").pack(pady=2)

tk.Label(menu_frame, text="🥐 Pastries", font=("Arial", 13, "bold"), bg="#f2f2f2").pack(pady=(8, 2))
for i in range(8, 11):
    item = menu[i]
    tk.Button(menu_frame, text=f"{i}. {item['name']} - ${item['price']:.2f}",
              command=lambda i=i: add_item(i), width=30, bg="#fce5cd").pack(pady=2)

tk.Label(root, text="🧾 Current Order:", font=("Arial", 12, "bold"), bg="#f2f2f2").pack(pady=10)
order_list = tk.Listbox(root, width=45, height=7)
order_list.pack()
total_label = tk.Label(root, text="Total: $0.00", font=("Arial", 12, "bold"), bg="#f2f2f2")
total_label.pack(pady=5)

tk.Label(root, text="Enter Discount Code:", font=("Arial", 11), bg="#f2f2f2").pack()
discount_code = tk.Entry(root, width=20)
discount_code.pack(pady=5)

tk.Label(root, text="Select Payment Method:", font=("Arial", 11), bg="#f2f2f2").pack()
payment_frame = tk.Frame(root, bg="#f2f2f2")
payment_frame.pack(pady=5)
payment_var = tk.StringVar(value="Cash")
tk.Radiobutton(payment_frame, text="Cash", variable=payment_var, value="Cash", bg="#f2f2f2").pack(side=tk.LEFT, padx=20)
tk.Radiobutton(payment_frame, text="Card", variable=payment_var, value="Card", bg="#f2f2f2").pack(side=tk.LEFT, padx=20)

btn_frame = tk.Frame(root, bg="#f2f2f2")
btn_frame.pack(pady=15)
tk.Button(btn_frame, text="Checkout", command=checkout, bg="#a4c2f4",
          font=("Arial", 12, "bold"), width=15).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="All Orders", command=view_all_orders, bg="#b6d7a8",
          font=("Arial", 12, "bold"), width=15).pack(side=tk.LEFT, padx=10)

root.mainloop()
