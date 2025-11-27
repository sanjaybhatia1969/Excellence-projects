"""
Main GUI Application for Café Retail Management System
Complete version with all management features working
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime

# Managers
from auth_manager import AuthenticationManager
from customer_manager import CustomerManager
from product_manager import ProductManager
from transaction_manager import TransactionManager
from report_manager import ReportManager
from staff_manager import StaffManager
from models import Transaction


class CafeRetailGUI:
    """Main Application GUI"""

    # ============================================================
    # INITIAL SETUP
    # ============================================================
    def __init__(self, root):
        self.root = root
        self.root.title("Café Retail Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f0f0')

        # Managers
        self.auth_manager = AuthenticationManager()
        self.customer_manager = CustomerManager()
        self.product_manager = ProductManager()
        self.transaction_manager = TransactionManager()
        self.report_manager = ReportManager()
        self.staff_manager = StaffManager()

        # Styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Header.TLabel", font=("Arial", 16, "bold"))

        # Start login screen
        self.show_login_screen()

    # ============================================================
    # UTILITY
    # ============================================================
    def clear_window(self):
        """Remove all widgets from root window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    # ============================================================
    # LOGIN SCREEN
    # ============================================================
    def show_login_screen(self):
        self.clear_window()

        login_frame = tk.Frame(self.root, bg="white", padx=40, pady=40)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(login_frame, text="☕ Café Management System",
                 font=("Arial", 20, "bold"), bg="white").pack(pady=20)

        # Username
        tk.Label(login_frame, text="Username:", bg="white").pack(anchor="w")
        self.username_entry = ttk.Entry(login_frame, width=30)
        self.username_entry.pack(pady=5)

        # Password
        tk.Label(login_frame, text="Password:", bg="white").pack(anchor="w")
        self.password_entry = ttk.Entry(login_frame, width=30, show="*")
        self.password_entry.pack(pady=5)

        # Login button
        tk.Button(login_frame, text="Login", bg="#27ae60", fg="white",
                  font=("Arial", 12, "bold"), width=25,
                  command=self.handle_login).pack(pady=20)

        # Hint
        tk.Label(login_frame,
                 text="Copyright © 2025 Execellence Corp. Powered by Sanjay Bhatia.",
                 bg="white", fg="#7f8c8d").pack()
        
        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self.handle_login())

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        success, message = self.auth_manager.login(username, password)

        if success:
            self.show_main_dashboard()
        else:
            messagebox.showerror("Login Failed", message)

    # ============================================================
    # MAIN DASHBOARD (AFTER LOGIN)
    # ============================================================
    def show_main_dashboard(self):
        self.clear_window()

        # Top Bar
        top_bar = tk.Frame(self.root, bg="#2c3e50", height=60)
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        tk.Label(top_bar, text="☕ Café Management System",
                 font=("Arial", 16, "bold"), fg="white", bg="#2c3e50").pack(side="left", padx=20, pady=15)

        # User info on right
        user_frame = tk.Frame(top_bar, bg="#2c3e50")
        user_frame.pack(side="right", padx=20)
        tk.Label(user_frame, text=f"Logged in: {self.auth_manager.get_user_display_name()}",
                 font=("Arial", 10), bg="#2c3e50", fg="white").pack()
        tk.Label(user_frame, text=f"Role: {self.auth_manager.current_user.role.upper()}",
                 font=("Arial", 9), bg="#2c3e50", fg="#bdc3c7").pack()

        # Sidebar
        sidebar = tk.Frame(self.root, bg="#34495e", width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Base menu buttons for all users
        menu_buttons = [
            ("🛒 New Sale", self.show_sales_screen),
            ("👥 Customers", self.show_customers_screen),
            ("📦 Products", self.show_products_screen),
            ("📊 Reports", self.show_reports_screen),
        ]
        
        # Add Staff Management for admin only
        if self.auth_manager.is_admin():
            menu_buttons.append(("👤 Staff", self.show_staff_screen))
        
        # Add Logout at the end
        menu_buttons.append(("🚪 Logout", self.handle_logout))

        for text, cmd in menu_buttons:
            btn = tk.Button(sidebar, text=text, bg="#34495e", fg="white",
                            font=("Arial", 11), bd=0, anchor="w", padx=20, pady=15,
                            activebackground="#2c3e50", activeforeground="white",
                            command=cmd)
            btn.pack(fill="x")
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg='#2c3e50'))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(bg='#34495e'))

        # Main Content Frame
        self.content_frame = tk.Frame(self.root, bg="#ecf0f1")
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.show_sales_screen()

    # ============================================================
    # LOGOUT
    # ============================================================
    def handle_logout(self):
        if messagebox.askyesno("Logout", "Are you sure?"):
            self.auth_manager.logout()
            self.show_login_screen()

    # ============================================================
    # SALES / POS SCREEN (SCROLLABLE)
    # ============================================================
    def show_sales_screen(self):
        # Clear
        for w in self.content_frame.winfo_children():
            w.destroy()

        # Header
        header = tk.Frame(self.content_frame, bg="#3498db", height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="🛒 Point of Sale", fg="white",
                 bg="#3498db", font=("Arial", 16, "bold")).pack(side="left", padx=20, pady=10)

        # Container
        main = tk.Frame(self.content_frame, bg="#ecf0f1")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # -------- LEFT (PRODUCT LIST)
        left = tk.Frame(main, bg="white", bd=1, relief="solid")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left, text="Products", font=("Arial", 12, "bold"), bg="white").pack(pady=10)

        search_frame = tk.Frame(left, bg="white")
        search_frame.pack(fill="x", padx=10)
        tk.Label(search_frame, text="Search:", bg="white").pack(side="left", padx=5)

        search_entry = ttk.Entry(search_frame, width=25)
        search_entry.pack(side="left", padx=5)

        ttk.Button(search_frame, text="Search",
                   command=lambda: self.load_products(products_tree,
                                                      search_entry.get())).pack(side="left")

        # Product Tree with scrollbar
        product_tree_frame = tk.Frame(left, bg="white")
        product_tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        product_scroll = ttk.Scrollbar(product_tree_frame, orient="vertical")
        product_scroll.pack(side="right", fill="y")
        
        products_tree = ttk.Treeview(product_tree_frame,
                                     columns=("ID", "Name", "Price", "Stock"),
                                     show="headings", height=15,
                                     yscrollcommand=product_scroll.set)
        product_scroll.config(command=products_tree.yview)
        
        for col in ("ID", "Name", "Price", "Stock"):
            products_tree.heading(col, text=col)
            products_tree.column(col, width=100)
        products_tree.pack(fill="both", expand=True)

        ttk.Button(left, text="Add to Cart",
                   command=lambda: self.add_to_cart(products_tree, cart_tree)).pack(pady=10)

        # -------- RIGHT (CART) - WITH SCROLL
        right_container = tk.Frame(main, bg="white", bd=1, relief="solid", width=420)
        right_container.pack(side="right", fill="both")
        right_container.pack_propagate(False)

        # Create canvas for scrolling
        cart_canvas = tk.Canvas(right_container, bg="white", highlightthickness=0)
        cart_scrollbar = ttk.Scrollbar(right_container, orient="vertical", command=cart_canvas.yview)
        
        # Scrollable frame inside canvas
        right = tk.Frame(cart_canvas, bg="white")
        
        # Configure canvas
        cart_canvas.configure(yscrollcommand=cart_scrollbar.set)
        
        # Pack scrollbar and canvas
        cart_scrollbar.pack(side="right", fill="y")
        cart_canvas.pack(side="left", fill="both", expand=True)
        
        # Create window in canvas
        canvas_frame = cart_canvas.create_window((0, 0), window=right, anchor="nw")
        
        # Configure scroll region when frame size changes
        def configure_scroll_region(event):
            cart_canvas.configure(scrollregion=cart_canvas.bbox("all"))
        
        def configure_canvas_width(event):
            cart_canvas.itemconfig(canvas_frame, width=event.width)
        
        right.bind("<Configure>", configure_scroll_region)
        cart_canvas.bind("<Configure>", configure_canvas_width)
        
        # Enable mouse wheel scrolling - only when mouse is over cart area
        def on_mousewheel(event):
            cart_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def bind_mousewheel(event):
            cart_canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        def unbind_mousewheel(event):
            cart_canvas.unbind_all("<MouseWheel>")
        
        # Only scroll when mouse is over the cart area
        right_container.bind("<Enter>", bind_mousewheel)
        right_container.bind("<Leave>", unbind_mousewheel)

        # Cart Header
        tk.Label(right, text="Shopping Cart", font=("Arial", 12, "bold"), bg="white").pack(pady=10)

        # Customer selection
        cust_frame = tk.Frame(right, bg="white")
        cust_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(cust_frame, text="Customer:", bg="white").pack(side="left")

        self.customer_var = tk.StringVar()
        customer_combo = ttk.Combobox(cust_frame, textvariable=self.customer_var, width=20)
        customer_combo.pack(side="left", padx=5)

        ttk.Button(cust_frame, text="Load",
                   command=lambda: self.load_customers_combo(customer_combo)).pack(side="left")

        # Cart Tree with scrollbar
        cart_tree_frame = tk.Frame(right, bg="white")
        cart_tree_frame.pack(fill="x", padx=10, pady=10)
        
        cart_tree_scroll = ttk.Scrollbar(cart_tree_frame, orient="vertical")
        cart_tree_scroll.pack(side="right", fill="y")
        
        cart_tree = ttk.Treeview(cart_tree_frame,
                                 columns=("Product", "Qty", "Price", "Total"),
                                 show="headings", height=8,
                                 yscrollcommand=cart_tree_scroll.set)
        cart_tree_scroll.config(command=cart_tree.yview)
        
        for col in ("Product", "Qty", "Price", "Total"):
            cart_tree.heading(col, text=col)
            cart_tree.column(col, width=85)
        cart_tree.pack(fill="x")

        ttk.Button(right, text="Remove Item",
                   command=lambda: self.remove_from_cart(cart_tree)).pack(pady=5)

        # Separator
        ttk.Separator(right, orient="horizontal").pack(fill="x", padx=10, pady=5)

        # Totals
        totals = tk.Frame(right, bg="white")
        totals.pack(fill="x", padx=10, pady=5)

        self.subtotal_label = tk.Label(totals, text="Subtotal: $0.00", bg="white", font=("Arial", 10))
        self.discount_label = tk.Label(totals, text="Discount: $0.00", bg="white", font=("Arial", 10))
        self.tax_label = tk.Label(totals, text="Tax: $0.00", bg="white", font=("Arial", 10))
        self.total_label = tk.Label(totals, text="TOTAL: $0.00", font=("Arial", 14, "bold"), bg="white", fg="#27ae60")

        self.subtotal_label.pack(anchor="w")
        self.discount_label.pack(anchor="w")
        self.tax_label.pack(anchor="w")
        self.total_label.pack(anchor="w", pady=5)

        # Separator
        ttk.Separator(right, orient="horizontal").pack(fill="x", padx=10, pady=5)

        # Payment Section
        pay_label = tk.Label(right, text="Payment Options", font=("Arial", 11, "bold"), bg="white")
        pay_label.pack(anchor="w", padx=10, pady=(5, 10))

        # Payment Method
        pay_method_frame = tk.Frame(right, bg="white")
        pay_method_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(pay_method_frame, text="Method:", bg="white", width=10, anchor="w").pack(side="left")
        self.payment_var = tk.StringVar(value="Cash")
        payment_combo = ttk.Combobox(pay_method_frame, textvariable=self.payment_var,
                     values=["Cash", "Credit", "Debit"], width=15, state="readonly")
        payment_combo.pack(side="left")

        # Cash Received
        cash_frame = tk.Frame(right, bg="white")
        cash_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(cash_frame, text="Cash Received:", bg="white", width=12, anchor="w").pack(side="left")
        self.cash_entry = ttk.Entry(cash_frame, width=15)
        self.cash_entry.pack(side="left")
        tk.Label(cash_frame, text="$", bg="white").pack(side="left", padx=(0, 5))

        # Process Sale Button
        tk.Button(right, text="💳 PROCESS SALE", bg="#27ae60", fg="white",
                  font=("Arial", 12, "bold"), height=2,
                  command=lambda: self.process_sale(cart_tree)).pack(fill="x", padx=10, pady=15)

        # Clear Cart Button
        tk.Button(right, text="🗑️ Clear Cart", bg="#e74c3c", fg="white",
                  font=("Arial", 10),
                  command=lambda: self.clear_cart(cart_tree)).pack(fill="x", padx=10, pady=(0, 15))

        self.cart_tree = cart_tree
        self.load_products(products_tree)
        self.load_customers_combo(customer_combo)

        self.transaction_manager.start_new_transaction(
            self.auth_manager.current_user, payment_method="Cash"
        )

    # ============================================================
    # CUSTOMER MANAGEMENT SCREEN
    # ============================================================
    def show_customers_screen(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

        # Header
        header = tk.Frame(self.content_frame, bg="#1abc9c", height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="👥 Customer Management",
                 fg="white", bg="#1abc9c",
                 font=("Arial", 16, "bold")).pack(side="left", padx=20, pady=10)

        # Main
        main = tk.Frame(self.content_frame, bg="#ecf0f1")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Controls
        controls = tk.Frame(main, bg="#ecf0f1")
        controls.pack(fill="x", pady=(0, 10))

        tk.Label(controls, text="Search:", bg="#ecf0f1").pack(side="left")
        search_entry = ttk.Entry(controls, width=30)
        search_entry.pack(side="left", padx=5)

        ttk.Button(controls, text="🔍 Search",
                   command=lambda: self.load_customers_list(tree, search_entry.get())).pack(side="left")

        ttk.Button(controls, text="➕ Add Customer",
                   command=lambda: self.show_add_customer_dialog(tree)).pack(side="left", padx=10)

        ttk.Button(controls, text="✏️ Edit",
                   command=lambda: self.show_edit_customer_dialog(tree)).pack(side="left")

        ttk.Button(controls, text="📊 History",
                   command=lambda: self.show_customer_history(tree)).pack(side="left", padx=5)
        
        ttk.Button(controls, text="🔄 Refresh",
                   command=lambda: self.load_customers_list(tree)).pack(side="left", padx=5)

        # Tree
        tree_frame = tk.Frame(main, bg="white", bd=1, relief="solid")
        tree_frame.pack(fill="both", expand=True)

        columns = ("ID", "Name", "Phone", "Email", "Type", "Points")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)
        
        self.load_customers_list(tree)

    def load_customers_list(self, tree, search_term=""):
        for i in tree.get_children():
            tree.delete(i)

        customers = self.customer_manager.search_customers(search_term)
        for c in customers:
            tree.insert("", "end", values=(
                c.customer_id, c.name, c.phone, c.email,
                c.customer_type, c.loyalty_points
            ))

    def show_add_customer_dialog(self, tree):
        win = tk.Toplevel(self.root)
        win.title("Add Customer")
        win.geometry("400x420")
        win.grab_set()

        frm = tk.Frame(win, bg="white", padx=20, pady=20)
        frm.pack(fill="both", expand=True)

        tk.Label(frm, text="Add Customer", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        entries = {}

        for label in ["Name", "Phone", "Email", "Address"]:
            tk.Label(frm, text=label, bg="white").pack(anchor="w", pady=(10, 0))
            e = ttk.Entry(frm, width=40)
            e.pack()
            entries[label] = e

        tk.Label(frm, text="Customer Type:", bg="white").pack(anchor="w", pady=(10, 0))
        type_var = tk.StringVar(value="Regular")
        type_combo = ttk.Combobox(frm, textvariable=type_var,
                                  values=self.customer_manager.get_customer_types())
        type_combo.pack(fill="x")

        def save():
            name = entries["Name"].get().strip()
            if not name:
                messagebox.showerror("Error", "Name is required")
                return

            success, msg, _ = self.customer_manager.add_customer(
                name=name,
                phone=entries["Phone"].get(),
                email=entries["Email"].get(),
                address=entries["Address"].get(),
                customer_type=type_var.get()
            )

            if success:
                messagebox.showinfo("Success", msg)
                self.load_customers_list(tree)
                win.destroy()
            else:
                messagebox.showerror("Error", msg)

        tk.Button(frm, text="Save", bg="#27ae60", fg="white",
                  command=save).pack(pady=15)

    def show_edit_customer_dialog(self, tree):
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select a customer")
            return

        item = tree.item(selection[0])
        customer_id = item["values"][0]
        customer = self.customer_manager.get_customer(customer_id)

        win = tk.Toplevel(self.root)
        win.title("Edit Customer")
        win.geometry("400x450")
        win.grab_set()

        frm = tk.Frame(win, bg="white", padx=20, pady=20)
        frm.pack(fill="both", expand=True)

        tk.Label(frm, text="Edit Customer", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        entries = {}

        def add_field(label, value):
            tk.Label(frm, text=label, bg="white").pack(anchor="w", pady=(10, 0))
            e = ttk.Entry(frm, width=40)
            e.insert(0, value or "")
            e.pack()
            entries[label] = e

        add_field("Name", customer.name)
        add_field("Phone", customer.phone)
        add_field("Email", customer.email)
        add_field("Address", customer.address)

        tk.Label(frm, text="Customer Type:", bg="white").pack(anchor="w", pady=(10, 0))
        type_var = tk.StringVar(value=customer.customer_type)
        type_combo = ttk.Combobox(frm, textvariable=type_var,
                                  values=self.customer_manager.get_customer_types())
        type_combo.pack(fill="x")

        def update():
            name = entries["Name"].get().strip()
            if not name:
                messagebox.showerror("Error", "Name is required")
                return

            success, msg = self.customer_manager.update_customer(
                customer_id,
                name=name,
                email=entries["Email"].get(),
                phone=entries["Phone"].get(),
                address=entries["Address"].get(),
                customer_type=type_var.get()
            )

            if success:
                messagebox.showinfo("Success", msg)
                self.load_customers_list(tree)
                win.destroy()
            else:
                messagebox.showerror("Error", msg)

        tk.Button(frm, text="Update", bg="#27ae60", fg="white",
                  command=update).pack(pady=20)

    def show_customer_history(self, tree):
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a customer")
            return

        item = tree.item(sel[0])
        customer_id = item["values"][0]
        customer = self.customer_manager.get_customer(customer_id)

        win = tk.Toplevel(self.root)
        win.title("Customer History")
        win.geometry("700x500")
        win.grab_set()

        header = tk.Frame(win, bg="#3498db", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text=f"{customer.name} ({customer.customer_type}) - {customer.loyalty_points} points",
                 bg="#3498db", fg="white", font=("Arial", 14, "bold")).pack(pady=15)

        tree_hist = ttk.Treeview(win,
                                 columns=("ID", "Date", "Amount", "Payment", "Staff"),
                                 show="headings")
        for col in ("ID", "Date", "Amount", "Payment", "Staff"):
            tree_hist.heading(col, text=col)
            tree_hist.column(col, width=120)
        tree_hist.pack(fill="both", expand=True, padx=10, pady=10)

        history = self.customer_manager.get_customer_transaction_history(customer_id)
        for h in history:
            tree_hist.insert("", "end", values=(
                h["transaction_id"],
                h["date"],
                f"${h['amount']:.2f}",
                h["payment_method"],
                h["staff_name"]
            ))

        ttk.Button(win, text="Close", command=win.destroy).pack(pady=10)

    # ============================================================
    # PRODUCT MANAGEMENT SCREEN
    # ============================================================
    def show_products_screen(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

        # Header
        header = tk.Frame(self.content_frame, bg="#9b59b6", height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="📦 Product Management",
                 font=("Arial", 16, "bold"), fg="white", bg="#9b59b6").pack(side="left", padx=20, pady=10)

        # Main container
        main = tk.Frame(self.content_frame, bg="#ecf0f1")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Controls
        controls = tk.Frame(main, bg="#ecf0f1")
        controls.pack(fill="x", pady=(0, 10))

        tk.Label(controls, text="Search:", bg="#ecf0f1").pack(side="left")
        search_entry = ttk.Entry(controls, width=25)
        search_entry.pack(side="left", padx=5)

        ttk.Button(controls, text="🔍 Search",
                   command=lambda: self.load_products_list(tree, search_entry.get())).pack(side="left")

        tk.Label(controls, text="Category:", bg="#ecf0f1").pack(side="left", padx=(20, 5))
        category_var = tk.StringVar(value="All")
        category_combo = ttk.Combobox(controls, textvariable=category_var, width=15)
        category_combo.pack(side="left")
        
        # Load categories
        categories = ["All"] + self.product_manager.get_all_categories()
        category_combo["values"] = categories

        ttk.Button(controls, text="Filter",
                   command=lambda: self.load_products_list(tree, search_entry.get(), 
                                                           "" if category_var.get() == "All" else category_var.get())).pack(side="left", padx=5)

        ttk.Button(controls, text="➕ Add Product",
                   command=lambda: self.show_add_product_dialog(tree)).pack(side="left", padx=20)

        ttk.Button(controls, text="✏️ Edit",
                   command=lambda: self.show_edit_product_dialog(tree)).pack(side="left")

        ttk.Button(controls, text="📦 Update Stock",
                   command=lambda: self.show_update_stock_dialog(tree)).pack(side="left", padx=5)

        ttk.Button(controls, text="⚠️ Low Stock",
                   command=lambda: self.show_low_stock_products(tree)).pack(side="left", padx=5)

        # Tree
        tree_frame = tk.Frame(main, bg="white", bd=1, relief="solid")
        tree_frame.pack(fill="both", expand=True)

        columns = ("ID", "Name", "Category", "Price", "Stock", "Threshold", "Status")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
        tree.column("ID", width=50)
        tree.column("Name", width=200)
        tree.column("Category", width=100)
        tree.column("Price", width=80)
        tree.column("Stock", width=80)
        tree.column("Threshold", width=80)
        tree.column("Status", width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)

        self.load_products_list(tree)

    def load_products_list(self, tree, search_term="", category=""):
        for i in tree.get_children():
            tree.delete(i)

        products = self.product_manager.search_products(search_term, category)
        for p in products:
            status = "⚠️ Low Stock" if p.is_low_stock() else "✅ OK"
            tree.insert("", "end", values=(
                p.product_id, p.name, p.category, f"${p.price:.2f}",
                p.stock_quantity, p._low_stock_threshold, status
            ))

    def show_add_product_dialog(self, tree):
        win = tk.Toplevel(self.root)
        win.title("Add Product")
        win.geometry("450x500")
        win.grab_set()

        frm = tk.Frame(win, bg="white", padx=20, pady=20)
        frm.pack(fill="both", expand=True)

        tk.Label(frm, text="Add New Product", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        entries = {}

        fields = [("Name", ""), ("Description", ""), ("Price", "0.00"), 
                  ("Stock Quantity", "0"), ("Low Stock Threshold", "10")]

        for label, default in fields:
            tk.Label(frm, text=label + ":", bg="white").pack(anchor="w", pady=(8, 0))
            e = ttk.Entry(frm, width=40)
            e.insert(0, default)
            e.pack()
            entries[label] = e

        tk.Label(frm, text="Category:", bg="white").pack(anchor="w", pady=(8, 0))
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(frm, textvariable=category_var, width=37)
        categories = self.product_manager.get_all_categories()
        category_combo["values"] = categories if categories else ["Coffee", "Tea", "Food", "Pastry", "Beverage"]
        category_combo.pack()

        def save():
            name = entries["Name"].get().strip()
            if not name:
                messagebox.showerror("Error", "Product name is required")
                return

            try:
                price = float(entries["Price"].get())
                stock = int(entries["Stock Quantity"].get())
                threshold = int(entries["Low Stock Threshold"].get())
            except ValueError:
                messagebox.showerror("Error", "Invalid number format")
                return

            success, msg = self.product_manager.add_product(
                name=name,
                description=entries["Description"].get(),
                price=price,
                stock_quantity=stock,
                low_stock_threshold=threshold,
                category=category_var.get()
            )

            if success:
                messagebox.showinfo("Success", msg)
                self.load_products_list(tree)
                win.destroy()
            else:
                messagebox.showerror("Error", msg)

        tk.Button(frm, text="Save Product", bg="#27ae60", fg="white",
                  font=("Arial", 11), command=save).pack(pady=20)

    def show_edit_product_dialog(self, tree):
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select a product to edit")
            return

        item = tree.item(selection[0])
        product_id = item["values"][0]
        product = self.product_manager.get_product(product_id)

        if not product:
            messagebox.showerror("Error", "Product not found")
            return

        win = tk.Toplevel(self.root)
        win.title("Edit Product")
        win.geometry("450x500")
        win.grab_set()

        frm = tk.Frame(win, bg="white", padx=20, pady=20)
        frm.pack(fill="both", expand=True)

        tk.Label(frm, text="Edit Product", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        entries = {}

        def add_field(label, value):
            tk.Label(frm, text=label + ":", bg="white").pack(anchor="w", pady=(8, 0))
            e = ttk.Entry(frm, width=40)
            e.insert(0, str(value) if value else "")
            e.pack()
            entries[label] = e

        add_field("Name", product.name)
        add_field("Description", product._description)
        add_field("Price", f"{product.price:.2f}")
        add_field("Stock Quantity", product.stock_quantity)
        add_field("Low Stock Threshold", product._low_stock_threshold)

        tk.Label(frm, text="Category:", bg="white").pack(anchor="w", pady=(8, 0))
        category_var = tk.StringVar(value=product.category)
        category_combo = ttk.Combobox(frm, textvariable=category_var, width=37)
        categories = self.product_manager.get_all_categories()
        category_combo["values"] = categories if categories else ["Coffee", "Tea", "Food", "Pastry", "Beverage"]
        category_combo.pack()

        def update():
            name = entries["Name"].get().strip()
            if not name:
                messagebox.showerror("Error", "Product name is required")
                return

            try:
                price = float(entries["Price"].get())
                stock = int(entries["Stock Quantity"].get())
                threshold = int(entries["Low Stock Threshold"].get())
            except ValueError:
                messagebox.showerror("Error", "Invalid number format")
                return

            success, msg = self.product_manager.update_product(
                product_id=product_id,
                name=name,
                description=entries["Description"].get(),
                price=price,
                stock_quantity=stock,
                low_stock_threshold=threshold,
                category=category_var.get()
            )

            if success:
                messagebox.showinfo("Success", msg)
                self.load_products_list(tree)
                win.destroy()
            else:
                messagebox.showerror("Error", msg)

        tk.Button(frm, text="Update Product", bg="#3498db", fg="white",
                  font=("Arial", 11), command=update).pack(pady=20)

    def show_update_stock_dialog(self, tree):
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select a product to update stock")
            return

        item = tree.item(selection[0])
        product_id = item["values"][0]
        product_name = item["values"][1]
        current_stock = item["values"][4]

        win = tk.Toplevel(self.root)
        win.title("Update Stock")
        win.geometry("350x250")
        win.grab_set()

        frm = tk.Frame(win, bg="white", padx=20, pady=20)
        frm.pack(fill="both", expand=True)

        tk.Label(frm, text="Update Stock", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        tk.Label(frm, text=f"Product: {product_name}", bg="white").pack(anchor="w", pady=5)
        tk.Label(frm, text=f"Current Stock: {current_stock}", bg="white").pack(anchor="w", pady=5)

        tk.Label(frm, text="Quantity Change (+/-):", bg="white").pack(anchor="w", pady=(15, 0))
        qty_entry = ttk.Entry(frm, width=20)
        qty_entry.pack(anchor="w")
        tk.Label(frm, text="(Positive to add, negative to reduce)", 
                 bg="white", fg="#7f8c8d", font=("Arial", 9)).pack(anchor="w")

        def update_stock():
            try:
                qty = int(qty_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Enter a valid number")
                return

            success, msg = self.product_manager.update_stock(product_id, qty)
            if success:
                messagebox.showinfo("Success", msg)
                self.load_products_list(tree)
                win.destroy()
            else:
                messagebox.showerror("Error", msg)

        tk.Button(frm, text="Update Stock", bg="#27ae60", fg="white",
                  command=update_stock).pack(pady=20)

    def show_low_stock_products(self, tree):
        for i in tree.get_children():
            tree.delete(i)

        products = self.product_manager.get_low_stock_products()
        for p in products:
            tree.insert("", "end", values=(
                p.product_id, p.name, p.category, f"${p.price:.2f}",
                p.stock_quantity, p._low_stock_threshold, "⚠️ Low Stock"
            ))

        if not products:
            messagebox.showinfo("Info", "No low stock products found!")

    # ============================================================
    # REPORTS SCREEN
    # ============================================================
    def show_reports_screen(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

        # Header
        header = tk.Frame(self.content_frame, bg="#e67e22", height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="📊 Business Reports", fg="white", bg="#e67e22",
                 font=("Arial", 16, "bold")).pack(side="left", padx=20, pady=10)

        # Main container
        main = tk.Frame(self.content_frame, bg="#ecf0f1")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Left panel - Report buttons
        left = tk.Frame(main, bg="white", bd=1, relief="solid", width=250)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)

        tk.Label(left, text="Select Report", font=("Arial", 12, "bold"), bg="white").pack(pady=15)

        reports = [
            ("📅 Daily Sales Report", self.show_daily_sales_report),
            ("👥 Revenue by Customer Type", self.show_customer_type_report),
            ("📦 Inventory Status", self.show_inventory_report),
            ("📈 Sales Trend (7 Days)", self.show_sales_trend_report),
            ("🏆 Top Customers", self.show_top_customers_report),
        ]

        for text, cmd in reports:
            btn = tk.Button(left, text=text, font=("Arial", 10), bg="#ecf0f1",
                          anchor="w", padx=15, pady=10, bd=0,
                          activebackground="#d5d5d5",
                          command=lambda c=cmd: c(report_area))
            btn.pack(fill="x", padx=10, pady=3)
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg='#d5d5d5'))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(bg='#ecf0f1'))

        # Right panel - Report display area
        right = tk.Frame(main, bg="white", bd=1, relief="solid")
        right.pack(side="right", fill="both", expand=True)

        tk.Label(right, text="Report Details", font=("Arial", 12, "bold"), bg="white").pack(pady=10)

        report_area = scrolledtext.ScrolledText(right, font=("Courier", 10), wrap="word", state="disabled")
        report_area.pack(fill="both", expand=True, padx=10, pady=10)

    def show_daily_sales_report(self, text_area):
        report = self.report_manager.get_daily_sales_report()
        
        content = f"""
{'='*60}
                    DAILY SALES REPORT
{'='*60}

Date: {report['date']}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*60}
SUMMARY
{'='*60}

Total Transactions: {report['transaction_count']}
Total Sales:        ${report['total_sales']:.2f}
Total Discounts:    ${report['total_discounts']:.2f}
Total Tax:          ${report['total_tax']:.2f}

{'='*60}
PAYMENT BREAKDOWN
{'='*60}
"""
        for p in report.get('payment_breakdown', []):
            content += f"\n{p['method']}: {p['count']} transactions - ${p['amount']:.2f}"

        content += f"""

{'='*60}
TOP 5 SELLING PRODUCTS
{'='*60}
"""
        for i, p in enumerate(report.get('top_products', []), 1):
            content += f"\n{i}. {p['product']} - Qty: {p['quantity']} - ${p['revenue']:.2f}"

        self._display_report(text_area, content)

    def show_customer_type_report(self, text_area):
        report = self.report_manager.get_revenue_by_customer_type_report()
        
        content = f"""
{'='*60}
              REVENUE BY CUSTOMER TYPE REPORT
{'='*60}

Period: Last 30 Days
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*60}
"""
        for r in report:
            content += f"""
Customer Type: {r['customer_type']}
  Transactions:  {r['transaction_count']}
  Total Revenue: ${r['total_revenue']:.2f}
  Avg Per Trans: ${r['average_transaction']:.2f}
  Discounts:     ${r['total_discounts']:.2f}
{'─'*40}
"""

        self._display_report(text_area, content)

    def show_inventory_report(self, text_area):
        report = self.report_manager.get_inventory_status_report()
        
        content = f"""
{'='*60}
                 INVENTORY STATUS REPORT
{'='*60}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*60}
OVERVIEW
{'='*60}

Total Products:      {report['total_products']}
Low Stock Items:     {report['low_stock_count']}
Total Inventory Value: ${report['total_inventory_value']:.2f}

{'='*60}
LOW STOCK ALERTS
{'='*60}
"""
        for p in report.get('low_stock_products', []):
            content += f"\n⚠️  {p['name']} - Stock: {p['current_stock']} (Threshold: {p['threshold']})"

        content += f"""

{'='*60}
INVENTORY BY CATEGORY
{'='*60}
"""
        for c in report.get('by_category', []):
            content += f"\n{c['category']}: {c['product_count']} products, {c['total_quantity']} units - ${c['value']:.2f}"

        self._display_report(text_area, content)

    def show_sales_trend_report(self, text_area):
        report = self.report_manager.get_sales_trend_report(7)
        
        content = f"""
{'='*60}
                SALES TREND (LAST 7 DAYS)
{'='*60}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*60}
DAILY BREAKDOWN
{'='*60}

{'Date':<15} {'Trans':<10} {'Sales':<15}
{'-'*40}
"""
        total_trans = 0
        total_sales = 0
        for day in report:
            content += f"{day['date']:<15} {day['transactions']:<10} ${day['total_sales']:.2f}\n"
            total_trans += day['transactions']
            total_sales += day['total_sales']

        content += f"""
{'-'*40}
{'TOTAL':<15} {total_trans:<10} ${total_sales:.2f}

Average Daily Sales: ${(total_sales/7 if len(report) > 0 else 0):.2f}
"""

        self._display_report(text_area, content)

    def show_top_customers_report(self, text_area):
        report = self.report_manager.get_top_customers_report(10)
        
        content = f"""
{'='*60}
                   TOP 10 CUSTOMERS
{'='*60}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*60}
"""
        for i, c in enumerate(report, 1):
            content += f"""
{i}. {c['name']} ({c['type']})
   Loyalty Points: {c['loyalty_points']}
   Total Visits:   {c['visit_count']}
   Total Spent:    ${c['total_spent']:.2f}
{'─'*40}
"""

        self._display_report(text_area, content)

    def _display_report(self, text_area, content):
        text_area.config(state="normal")
        text_area.delete("1.0", "end")
        text_area.insert("1.0", content)
        text_area.config(state="disabled")

    # ============================================================
    # STAFF MANAGEMENT SCREEN (ADMIN ONLY)
    # ============================================================
    def show_staff_screen(self):
        """Display staff management screen - Admin only"""
        # Check if user is admin
        if not self.auth_manager.is_admin():
            messagebox.showerror("Access Denied", "Only administrators can access staff management.")
            return
        
        for w in self.content_frame.winfo_children():
            w.destroy()

        # Header
        header = tk.Frame(self.content_frame, bg="#8e44ad", height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="👤 Staff Management",
                 fg="white", bg="#8e44ad",
                 font=("Arial", 16, "bold")).pack(side="left", padx=20, pady=10)

        # Main container
        main = tk.Frame(self.content_frame, bg="#ecf0f1")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Controls
        controls = tk.Frame(main, bg="#ecf0f1")
        controls.pack(fill="x", pady=(0, 10))

        tk.Label(controls, text="Search:", bg="#ecf0f1").pack(side="left")
        search_entry = ttk.Entry(controls, width=25)
        search_entry.pack(side="left", padx=5)

        ttk.Button(controls, text="🔍 Search",
                   command=lambda: self.load_staff_list(tree, search_entry.get())).pack(side="left")

        ttk.Button(controls, text="➕ Add Staff",
                   command=lambda: self.show_add_staff_dialog(tree)).pack(side="left", padx=20)

        ttk.Button(controls, text="✏️ Edit",
                   command=lambda: self.show_edit_staff_dialog(tree)).pack(side="left")

        ttk.Button(controls, text="🔑 Reset Password",
                   command=lambda: self.show_reset_password_dialog(tree)).pack(side="left", padx=5)

        ttk.Button(controls, text="🗑️ Delete",
                   command=lambda: self.delete_staff(tree)).pack(side="left", padx=5)

        ttk.Button(controls, text="🔄 Refresh",
                   command=lambda: self.load_staff_list(tree)).pack(side="left", padx=5)

        # Staff list
        tree_frame = tk.Frame(main, bg="white", bd=1, relief="solid")
        tree_frame.pack(fill="both", expand=True)

        columns = ("ID", "Username", "Name", "Role", "Email", "Phone", "Created")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        tree.heading("ID", text="ID")
        tree.heading("Username", text="Username")
        tree.heading("Name", text="Name")
        tree.heading("Role", text="Role")
        tree.heading("Email", text="Email")
        tree.heading("Phone", text="Phone")
        tree.heading("Created", text="Created")

        tree.column("ID", width=50)
        tree.column("Username", width=120)
        tree.column("Name", width=150)
        tree.column("Role", width=80)
        tree.column("Email", width=180)
        tree.column("Phone", width=120)
        tree.column("Created", width=100)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)

        self.load_staff_list(tree)

    def load_staff_list(self, tree, search_term=""):
        """Load staff list into treeview"""
        for i in tree.get_children():
            tree.delete(i)

        staff_list = self.staff_manager.get_all_staff(search_term)
        for s in staff_list:
            role_display = "👑 Admin" if s['role'] == 'admin' else "👤 Staff"
            tree.insert("", "end", values=(
                s['user_id'],
                s['username'],
                s['name'],
                role_display,
                s['email'],
                s['phone'],
                s['created_at']
            ))

    def show_add_staff_dialog(self, tree):
        """Show dialog to add new staff"""
        win = tk.Toplevel(self.root)
        win.title("Add New Staff")
        win.geometry("450x550")
        win.grab_set()
        win.resizable(False, False)

        frm = tk.Frame(win, bg="white", padx=30, pady=20)
        frm.pack(fill="both", expand=True)

        tk.Label(frm, text="Add New Staff Member", font=("Arial", 14, "bold"), 
                 bg="white").pack(pady=(0, 20))

        entries = {}

        # Username
        tk.Label(frm, text="Username: *", bg="white", anchor="w").pack(fill="x", pady=(10, 0))
        entries["username"] = ttk.Entry(frm, width=40)
        entries["username"].pack(fill="x")

        # Password
        tk.Label(frm, text="Password: *", bg="white", anchor="w").pack(fill="x", pady=(10, 0))
        entries["password"] = ttk.Entry(frm, width=40, show="*")
        entries["password"].pack(fill="x")

        # Confirm Password
        tk.Label(frm, text="Confirm Password: *", bg="white", anchor="w").pack(fill="x", pady=(10, 0))
        entries["confirm_password"] = ttk.Entry(frm, width=40, show="*")
        entries["confirm_password"].pack(fill="x")

        # Name
        tk.Label(frm, text="Full Name: *", bg="white", anchor="w").pack(fill="x", pady=(10, 0))
        entries["name"] = ttk.Entry(frm, width=40)
        entries["name"].pack(fill="x")

        # Email
        tk.Label(frm, text="Email:", bg="white", anchor="w").pack(fill="x", pady=(10, 0))
        entries["email"] = ttk.Entry(frm, width=40)
        entries["email"].pack(fill="x")

        # Phone
        tk.Label(frm, text="Phone:", bg="white", anchor="w").pack(fill="x", pady=(10, 0))
        entries["phone"] = ttk.Entry(frm, width=40)
        entries["phone"].pack(fill="x")

        # Address
        tk.Label(frm, text="Address:", bg="white", anchor="w").pack(fill="x", pady=(10, 0))
        entries["address"] = ttk.Entry(frm, width=40)
        entries["address"].pack(fill="x")

        # Role
        tk.Label(frm, text="Role: *", bg="white", anchor="w").pack(fill="x", pady=(10, 0))
        role_var = tk.StringVar(value="staff")
        role_frame = tk.Frame(frm, bg="white")
        role_frame.pack(fill="x")
        ttk.Radiobutton(role_frame, text="Staff", variable=role_var, value="staff").pack(side="left")
        ttk.Radiobutton(role_frame, text="Admin", variable=role_var, value="admin").pack(side="left", padx=20)

        tk.Label(frm, text="* Required fields", bg="white", fg="#7f8c8d", 
                 font=("Arial", 9)).pack(pady=(15, 0))

        def save():
            username = entries["username"].get().strip()
            password = entries["password"].get()
            confirm = entries["confirm_password"].get()
            name = entries["name"].get().strip()
            
            # Validation
            if not username:
                messagebox.showerror("Error", "Username is required")
                return
            
            if not password:
                messagebox.showerror("Error", "Password is required")
                return
            
            if password != confirm:
                messagebox.showerror("Error", "Passwords do not match")
                return
            
            if len(password) < 4:
                messagebox.showerror("Error", "Password must be at least 4 characters")
                return
            
            if not name:
                messagebox.showerror("Error", "Name is required")
                return
            
            success, msg = self.staff_manager.add_staff(
                username=username,
                password=password,
                name=name,
                email=entries["email"].get().strip(),
                phone=entries["phone"].get().strip(),
                address=entries["address"].get().strip(),
                role=role_var.get()
            )
            
            if success:
                messagebox.showinfo("Success", msg)
                self.load_staff_list(tree)
                win.destroy()
            else:
                messagebox.showerror("Error", msg)

        btn_frame = tk.Frame(frm, bg="white")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Save", bg="#27ae60", fg="white",
                  font=("Arial", 11), width=12, command=save).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancel", bg="#95a5a6", fg="white",
                  font=("Arial", 11), width=12, command=win.destroy).pack(side="left", padx=5)

    def show_edit_staff_dialog(self, tree):
        """Show dialog to edit staff"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a staff member to edit")
            return

        item = tree.item(selection[0])
        user_id = item["values"][0]
        staff = self.staff_manager.get_staff(user_id)

        if not staff:
            messagebox.showerror("Error", "Staff not found")
            return

        win = tk.Toplevel(self.root)
        win.title("Edit Staff")
        win.geometry("450x450")
        win.grab_set()
        win.resizable(False, False)

        frm = tk.Frame(win, bg="white", padx=30, pady=20)
        frm.pack(fill="both", expand=True)

        tk.Label(frm, text="Edit Staff Member", font=("Arial", 14, "bold"), 
                 bg="white").pack(pady=(0, 20))
        
        tk.Label(frm, text=f"Username: {staff['username']}", bg="white", 
                 font=("Arial", 10, "italic")).pack(anchor="w")

        entries = {}

        # Name
        tk.Label(frm, text="Full Name: *", bg="white", anchor="w").pack(fill="x", pady=(15, 0))
        entries["name"] = ttk.Entry(frm, width=40)
        entries["name"].insert(0, staff['name'])
        entries["name"].pack(fill="x")

        # Email
        tk.Label(frm, text="Email:", bg="white", anchor="w").pack(fill="x", pady=(10, 0))
        entries["email"] = ttk.Entry(frm, width=40)
        entries["email"].insert(0, staff['email'])
        entries["email"].pack(fill="x")

        # Phone
        tk.Label(frm, text="Phone:", bg="white", anchor="w").pack(fill="x", pady=(10, 0))
        entries["phone"] = ttk.Entry(frm, width=40)
        entries["phone"].insert(0, staff['phone'])
        entries["phone"].pack(fill="x")

        # Role
        tk.Label(frm, text="Role:", bg="white", anchor="w").pack(fill="x", pady=(10, 0))
        role_var = tk.StringVar(value=staff['role'])
        role_frame = tk.Frame(frm, bg="white")
        role_frame.pack(fill="x")
        ttk.Radiobutton(role_frame, text="Staff", variable=role_var, value="staff").pack(side="left")
        ttk.Radiobutton(role_frame, text="Admin", variable=role_var, value="admin").pack(side="left", padx=20)

        # Transaction count info
        trans_count = self.staff_manager.get_staff_transaction_count(user_id)
        tk.Label(frm, text=f"Transactions processed: {trans_count}", 
                 bg="white", fg="#7f8c8d").pack(pady=(20, 0))

        def update():
            name = entries["name"].get().strip()
            
            if not name:
                messagebox.showerror("Error", "Name is required")
                return
            
            success, msg = self.staff_manager.update_staff(
                user_id=user_id,
                name=name,
                email=entries["email"].get().strip(),
                phone=entries["phone"].get().strip(),
                role=role_var.get()
            )
            
            if success:
                messagebox.showinfo("Success", msg)
                self.load_staff_list(tree)
                win.destroy()
            else:
                messagebox.showerror("Error", msg)

        btn_frame = tk.Frame(frm, bg="white")
        btn_frame.pack(pady=25)
        
        tk.Button(btn_frame, text="Update", bg="#3498db", fg="white",
                  font=("Arial", 11), width=12, command=update).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancel", bg="#95a5a6", fg="white",
                  font=("Arial", 11), width=12, command=win.destroy).pack(side="left", padx=5)

    def show_reset_password_dialog(self, tree):
        """Show dialog to reset staff password"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a staff member")
            return

        item = tree.item(selection[0])
        user_id = item["values"][0]
        username = item["values"][1]
        name = item["values"][2]

        win = tk.Toplevel(self.root)
        win.title("Reset Password")
        win.geometry("400x280")
        win.grab_set()
        win.resizable(False, False)

        frm = tk.Frame(win, bg="white", padx=30, pady=20)
        frm.pack(fill="both", expand=True)

        tk.Label(frm, text="Reset Password", font=("Arial", 14, "bold"), 
                 bg="white").pack(pady=(0, 10))
        
        tk.Label(frm, text=f"Staff: {name} ({username})", bg="white").pack(pady=(0, 20))

        # New Password
        tk.Label(frm, text="New Password:", bg="white", anchor="w").pack(fill="x")
        new_password = ttk.Entry(frm, width=35, show="*")
        new_password.pack(fill="x", pady=(0, 10))

        # Confirm Password
        tk.Label(frm, text="Confirm Password:", bg="white", anchor="w").pack(fill="x")
        confirm_password = ttk.Entry(frm, width=35, show="*")
        confirm_password.pack(fill="x")

        def reset():
            new_pwd = new_password.get()
            confirm_pwd = confirm_password.get()
            
            if not new_pwd:
                messagebox.showerror("Error", "Password is required")
                return
            
            if new_pwd != confirm_pwd:
                messagebox.showerror("Error", "Passwords do not match")
                return
            
            if len(new_pwd) < 4:
                messagebox.showerror("Error", "Password must be at least 4 characters")
                return
            
            success, msg = self.staff_manager.update_password(user_id, new_pwd)
            
            if success:
                messagebox.showinfo("Success", msg)
                win.destroy()
            else:
                messagebox.showerror("Error", msg)

        btn_frame = tk.Frame(frm, bg="white")
        btn_frame.pack(pady=25)
        
        tk.Button(btn_frame, text="Reset Password", bg="#e74c3c", fg="white",
                  font=("Arial", 11), width=14, command=reset).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancel", bg="#95a5a6", fg="white",
                  font=("Arial", 11), width=10, command=win.destroy).pack(side="left", padx=5)

    def delete_staff(self, tree):
        """Delete selected staff member"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a staff member to delete")
            return

        item = tree.item(selection[0])
        user_id = item["values"][0]
        username = item["values"][1]
        name = item["values"][2]
        
        # Prevent self-deletion
        if user_id == self.auth_manager.current_user.user_id:
            messagebox.showerror("Error", "You cannot delete your own account!")
            return

        if messagebox.askyesno("Confirm Delete", 
                               f"Are you sure you want to delete staff member:\n\n"
                               f"Name: {name}\n"
                               f"Username: {username}\n\n"
                               f"This action cannot be undone!"):
            success, msg = self.staff_manager.delete_staff(user_id)
            
            if success:
                messagebox.showinfo("Success", msg)
                self.load_staff_list(tree)
            else:
                messagebox.showerror("Error", msg)

    # ============================================================
    # SUPPORT FUNCTIONS (from POS)
    # ============================================================
    def load_products(self, tree, term=""):
        for i in tree.get_children():
            tree.delete(i)

        products = self.product_manager.search_products(term)
        for p in products:
            tree.insert("", "end", values=(
                p.product_id, p.name, f"${p.price:.2f}", p.stock_quantity
            ))

    def load_customers_combo(self, combo):
        customers = self.customer_manager.search_customers()
        combo["values"] = ["Walk-in"] + [
            f"{c.customer_id}: {c.name} ({c.customer_type})" for c in customers
        ]
        combo.current(0)

    def add_to_cart(self, products_tree, cart_tree):
        selected = products_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a product")
            return

        item = products_tree.item(selected[0])
        product_id = int(item["values"][0])
        product_name = item["values"][1]

        # Ask quantity
        win = tk.Toplevel(self.root)
        win.title("Add to Cart")
        win.geometry("300x180")
        win.grab_set()
        win.resizable(False, False)
        
        # Center the window
        win.transient(self.root)
        
        frame = tk.Frame(win, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text=f"Product: {product_name}", font=("Arial", 10, "bold")).pack(pady=(0, 10))
        tk.Label(frame, text="Enter quantity:").pack()
        
        qty_entry = ttk.Entry(frame, width=15, justify="center")
        qty_entry.pack(pady=10)
        qty_entry.insert(0, "1")
        qty_entry.select_range(0, tk.END)
        qty_entry.focus_set()

        def add():
            qty_text = qty_entry.get().strip()
            if not qty_text:
                messagebox.showerror("Error", "Please enter a quantity")
                return
            
            try:
                q = int(qty_text)
                if q <= 0:
                    messagebox.showerror("Error", "Quantity must be greater than 0")
                    return
                    
                success, msg = self.transaction_manager.add_item_to_cart(product_id, q)
                
                # Close window first regardless of outcome
                win.destroy()
                
                if success:
                    self.update_cart_display(cart_tree)
                else:
                    messagebox.showerror("Error", msg)
                    
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")
            except Exception as e:
                win.destroy()
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Add", command=add, width=10).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=win.destroy, width=10).pack(side="left", padx=5)
        
        qty_entry.bind('<Return>', lambda e: add())
        qty_entry.bind('<Escape>', lambda e: win.destroy())

    def remove_from_cart(self, cart_tree):
        selected = cart_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an item to remove")
            return

        product_name = cart_tree.item(selected[0])["values"][0]
        trans = self.transaction_manager.current_transaction

        for item in trans.items:
            if item.product.name == product_name:
                self.transaction_manager.remove_item_from_cart(item.product.product_id)
                break

        self.update_cart_display(cart_tree)

    def clear_cart(self, cart_tree):
        """Clear all items from cart"""
        trans = self.transaction_manager.current_transaction
        if trans and len(trans.items) > 0:
            if messagebox.askyesno("Clear Cart", "Are you sure you want to clear all items from the cart?"):
                trans.clear_items()
                self.update_cart_display(cart_tree)

    def update_cart_display(self, cart_tree):
        for i in cart_tree.get_children():
            cart_tree.delete(i)

        trans = self.transaction_manager.current_transaction
        if not trans:
            return

        for item in trans.items:
            cart_tree.insert("", "end", values=(
                item.product.name,
                item.quantity,
                f"${item.unit_price:.2f}",
                f"${item.get_subtotal():.2f}"
            ))

        self.subtotal_label.config(text=f"Subtotal: ${trans.calculate_subtotal():.2f}")
        self.discount_label.config(text=f"Discount: ${trans.calculate_discount():.2f}")
        self.tax_label.config(text=f"Tax: ${trans.calculate_tax():.2f}")
        self.total_label.config(text=f"TOTAL: ${trans.calculate_total():.2f}")

    def process_sale(self, cart_tree):
        trans = self.transaction_manager.current_transaction

        if not trans or len(trans.items) == 0:
            messagebox.showwarning("Warning", "Cart is empty")
            return

        # Customer
        cust = self.customer_var.get()
        if cust != "Walk-in":
            cid = int(cust.split(":")[0])
            trans._customer = self.customer_manager.get_customer(cid)

        # Payment
        trans.payment_method = self.payment_var.get()

        # Cash
        cash = 0
        if trans.payment_method == "Cash":
            try:
                cash = float(self.cash_entry.get() or 0)
            except:
                messagebox.showerror("Error", "Invalid cash amount")
                return

        success, msg, tid = self.transaction_manager.process_transaction(cash)

        if success:
            self.show_receipt(tid)
            self.transaction_manager.start_new_transaction(
                self.auth_manager.current_user, payment_method="Cash"
            )
            self.update_cart_display(cart_tree)
            self.cash_entry.delete(0, "end")
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)

    def show_receipt(self, transaction_id):
        trans_data = self.transaction_manager.get_transaction(transaction_id)
        if not trans_data:
            return

        receipt_window = tk.Toplevel(self.root)
        receipt_window.title(f"Receipt - Transaction #{transaction_id}")
        receipt_window.geometry("400x600")

        receipt_text = scrolledtext.ScrolledText(receipt_window, font=('Courier', 10), wrap='word')
        receipt_text.pack(fill='both', expand=True, padx=10, pady=10)

        receipt = f"""
{'='*40}
     ☕ CAFÉ MANAGEMENT SYSTEM
{'='*40}

Transaction ID: {trans_data['transaction_id']}
Date: {trans_data['date']}
Staff: {trans_data['staff_name']}
Customer: {trans_data['customer_name']}

{'='*40}
ITEMS:
{'='*40}

"""
        for item in trans_data['items']:
            receipt += f"{item['product_name']}\n"
            receipt += f"  {item['quantity']} x ${item['unit_price']:.2f} = ${item['subtotal']:.2f}\n\n"

        receipt += f"""{'='*40}

Subtotal:        ${trans_data['subtotal']:>10.2f}
Discount:        ${trans_data['discount']:>10.2f}
Tax (10%):       ${trans_data['tax']:>10.2f}
{'='*40}
TOTAL:           ${trans_data['total']:>10.2f}
{'='*40}

Payment: {trans_data['payment_method']}
"""

        if trans_data['payment_method'] == 'Cash':
            receipt += f"""Cash:            ${trans_data['cash_received']:>10.2f}
Change:          ${trans_data['change_given']:>10.2f}
"""

        receipt += f"""
{'='*40}
    Thank you! Visit again! ☕
{'='*40}
"""

        receipt_text.insert('1.0', receipt)
        receipt_text.config(state='disabled')

        ttk.Button(receipt_window, text="Close", command=receipt_window.destroy).pack(pady=10)


# Start App
def main():
    root = tk.Tk()
    CafeRetailGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
