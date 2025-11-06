import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, scrolledtext
import random

# ---------------------- Data Structures ----------------------
customers = {}
transactions = []
customer_segments = {}
loyalty_points = {}
customer_feedback = {}

# ---------------------- Logic Functions ----------------------
def determine_loyalty(transaction_count):
    if transaction_count == 1:
        return "First-time Customer"
    elif transaction_count < 3:
        return "Repeat Customer"
    else:
        return "Loyal Customer"

def add_customer(customer_id, name, email):
    if customer_id in customers:
        raise Exception("Customer ID already exists.")
    customers[customer_id] = {
        'name': name,
        'email': email,
        'transactions': [],
        'loyalty_status': "New"
    }
    loyalty_points[customer_id] = 0
    customer_feedback[customer_id] = []

def edit_customer(customer_id, name=None, email=None):
    if customer_id not in customers:
        raise Exception("Customer ID not found.")
    if name:
        customers[customer_id]['name'] = name
    if email:
        customers[customer_id]['email'] = email

def delete_customer(customer_id):
    if customer_id not in customers:
        raise Exception("Customer ID not found.")
    del customers[customer_id]
    global transactions
    transactions = [t for t in transactions if t['customer_id'] != customer_id]
    loyalty_points.pop(customer_id, None)
    customer_feedback.pop(customer_id, None)

def add_transaction(customer_id, amount, date):
    if customer_id not in customers:
        raise Exception("Customer ID not found.")
    transaction = {'customer_id': customer_id, 'amount': amount, 'date': date}
    transactions.append(transaction)
    customers[customer_id]['transactions'].append(transaction)
    loyalty_points[customer_id] += amount // 10
    count = len(customers[customer_id]['transactions'])
    customers[customer_id]['loyalty_status'] = determine_loyalty(count)

def view_customer(customer_id):
    if customer_id not in customers:
        raise Exception("Customer ID not found.")
    info = customers[customer_id]
    return (
        f"Customer: {info['name']} (Email: {info['email']})\n"
        f"Loyalty Status: {info['loyalty_status']}, Points: {loyalty_points[customer_id]}\n"
        "Transactions:\n"
        + "\n".join(f" - Date: {t['date']}, Amount: {t['amount']}" for t in info['transactions'])
        + "\nFeedback log:\n"
        + "\n".join(f" - '{msg}'" for msg in customer_feedback[customer_id])
    )

def log_feedback(customer_id, feedback_msg):
    if customer_id not in customers:
        raise Exception("Customer ID not found.")
    customer_feedback[customer_id].append(feedback_msg)

def segment_customers():
    segments = {'High': [], 'Medium': [], 'Low': []}
    for cid, info in customers.items():
        total = sum(t['amount'] for t in info['transactions'])
        if total > 500:
            segments['High'].append(cid)
        elif total > 200:
            segments['Medium'].append(cid)
        else:
            segments['Low'].append(cid)
    global customer_segments
    customer_segments = segments

def send_personalized_offers():
    sent = []
    for cid, info in customers.items():
        if info['loyalty_status'] == "Loyal Customer":
            sent.append(f"Email to {info['name']} ({info['email']}): 'You earned {loyalty_points[cid]} points! Use them for an exclusive discount.'")
    return sent


# ---------------------- GUI Design ----------------------
def gui_main():
    root = tk.Tk()
    root.title("Loyalty Manager Pro")
    root.geometry("850x600")
    root.configure(bg="#eef2f3")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=6, background="#2d89ef", foreground="white")
    style.map("TButton", background=[("active", "#1b5fab")])

    title = tk.Label(root, text="Customer Loyalty Management System", bg="#2d89ef", fg="white",
                     font=("Segoe UI", 18, "bold"), pady=10)
    title.pack(fill=tk.X)

    # Frame for Inputs
    input_frame = tk.Frame(root, bg="white", bd=2, relief="groove")
    input_frame.pack(padx=20, pady=10, fill="x")

    tk.Label(input_frame, text="Customer ID:", bg="white", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    tk.Label(input_frame, text="Name:", bg="white", font=("Segoe UI", 11)).grid(row=0, column=2, sticky="w", padx=10, pady=5)
    tk.Label(input_frame, text="Email:", bg="white", font=("Segoe UI", 11)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    tk.Label(input_frame, text="Amount:", bg="white", font=("Segoe UI", 11)).grid(row=1, column=2, sticky="w", padx=10, pady=5)
    tk.Label(input_frame, text="Date (YYYY-MM-DD):", bg="white", font=("Segoe UI", 11)).grid(row=2, column=0, sticky="w", padx=10, pady=5)

    id_entry = ttk.Entry(input_frame, width=20)
    name_entry = ttk.Entry(input_frame, width=20)
    email_entry = ttk.Entry(input_frame, width=25)
    amount_entry = ttk.Entry(input_frame, width=10)
    date_entry = ttk.Entry(input_frame, width=15)

    id_entry.grid(row=0, column=1, padx=5, pady=5)
    name_entry.grid(row=0, column=3, padx=5, pady=5)
    email_entry.grid(row=1, column=1, padx=5, pady=5)
    amount_entry.grid(row=1, column=3, padx=5, pady=5)
    date_entry.grid(row=2, column=1, padx=5, pady=5)

    # Output box
    output_box = scrolledtext.ScrolledText(root, width=90, height=15, font=("Consolas", 10))
    output_box.pack(padx=20, pady=10)

    def display_output(msg):
        output_box.insert(tk.END, msg + "\n\n")
        output_box.see(tk.END)

    # Button Frame
    btn_frame = tk.Frame(root, bg="#eef2f3")
    btn_frame.pack(pady=5)

    def gui_add_customer():
        try:
            cid = int(id_entry.get())
            name = name_entry.get()
            email = email_entry.get()
            add_customer(cid, name, email)
            display_output(f"✅ Customer '{name}' added successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def gui_edit_customer():
        try:
            cid = int(id_entry.get())
            name = name_entry.get()
            email = email_entry.get()
            edit_customer(cid, name if name else None, email if email else None)
            display_output(f"✏️ Customer {cid} updated.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def gui_delete_customer():
        try:
            cid = int(id_entry.get())
            delete_customer(cid)
            display_output(f"🗑️ Customer {cid} deleted.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def gui_add_transaction():
        try:
            cid = int(id_entry.get())
            amount = float(amount_entry.get())
            date = date_entry.get()
            add_transaction(cid, amount, date)
            display_output(f"💰 Transaction added for Customer {cid}: {amount} on {date}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def gui_view_customer():
        try:
            cid = int(id_entry.get())
            info = view_customer(cid)
            display_output(info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def gui_log_feedback():
        try:
            cid = int(id_entry.get())
            feedback = simpledialog.askstring("Feedback", "Enter feedback:")
            log_feedback(cid, feedback)
            display_output(f"🗒️ Feedback logged for Customer {cid}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def gui_segment_customers():
        try:
            segment_customers()
            info = "\n".join(f"{seg}: {', '.join(map(str, ids))}" for seg, ids in customer_segments.items())
            display_output("📊 Customer Segments:\n" + info)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def gui_send_offers():
        offers = send_personalized_offers()
        if offers:
            for o in offers:
                display_output("📧 " + o)
        else:
            display_output("No loyal customer offers available now.")

    ttk.Button(btn_frame, text="Add Customer", command=gui_add_customer).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(btn_frame, text="Edit Customer", command=gui_edit_customer).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(btn_frame, text="Delete Customer", command=gui_delete_customer).grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(btn_frame, text="Add Transaction", command=gui_add_transaction).grid(row=0, column=3, padx=5, pady=5)
    ttk.Button(btn_frame, text="View Customer", command=gui_view_customer).grid(row=1, column=0, padx=5, pady=5)
    ttk.Button(btn_frame, text="Log Feedback", command=gui_log_feedback).grid(row=1, column=1, padx=5, pady=5)
    ttk.Button(btn_frame, text="Segment Customers", command=gui_segment_customers).grid(row=1, column=2, padx=5, pady=5)
    ttk.Button(btn_frame, text="Send Offers", command=gui_send_offers).grid(row=1, column=3, padx=5, pady=5)
    ttk.Button(btn_frame, text="Quit", command=root.destroy).grid(row=2, column=1, padx=5, pady=10)

    root.mainloop()


if __name__ == "__main__":
    gui_main()
