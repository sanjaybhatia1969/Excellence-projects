"""
Main Entry Point for Café Retail Management System
Run this file to start the application
"""

import tkinter as tk
from tkinter import messagebox

# Check database connection first
def check_database():
    """Verify database is accessible before starting GUI"""
    try:
        from database import DatabaseConnection, initialize_database
        
        # Try to connect
        db = DatabaseConnection()
        conn = db.get_connection()
        
        if conn is None:
            # Try to initialize database
            print("Attempting to initialize database...")
            if initialize_database():
                print("Database initialized successfully!")
                return True
            else:
                return False
        return True
        
    except Exception as e:
        print(f"Database error: {e}")
        return False


def main():
    """Main entry point"""
    print("=" * 50)
    print("  Café Retail Management System")
    print("=" * 50)
    print("\nStarting application...")
    
    # Check database
    if not check_database():
        print("\n⚠️  Database connection failed!")
        print("Please ensure:")
        print("  1. MySQL server is running")
        print("  2. Credentials in database.py are correct")
        print("  3. Run: python database.py to initialize")
        
        # Show error dialog
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Database Error",
            "Could not connect to MySQL database.\n\n"
            "Please check:\n"
            "1. MySQL server is running\n"
            "2. Credentials in database.py are correct\n\n"
            "Run 'python database.py' to initialize the database."
        )
        root.destroy()
        return
    
    print("✓ Database connection successful!")
    print("✓ Starting GUI...\n")
    
    # Import and start GUI
    try:
        from gui import CafeRetailGUI
        
        root = tk.Tk()
        app = CafeRetailGUI(root)
        root.mainloop()
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure gui.py is in the same directory.")
        
    except Exception as e:
        print(f"Application error: {e}")
        raise


if __name__ == "__main__":
    main()
