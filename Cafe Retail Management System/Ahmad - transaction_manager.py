"""
Transaction Manager
Handles sales, billing, and receipt generation
Demonstrates: Complex business logic, control structures
"""

from typing import Optional, List
from models import Transaction, Customer, User, Product
from database import DatabaseConnection
from product_manager import ProductManager
from customer_manager import CustomerManager

class TransactionManager:
    """Manages transaction processing"""
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.product_manager = ProductManager()
        self.customer_manager = CustomerManager()
        self._current_transaction: Optional[Transaction] = None
    
    def start_new_transaction(self, user: User, customer: Optional[Customer] = None,
                             payment_method: str = "Cash") -> Transaction:
        """Start a new transaction"""
        self._current_transaction = Transaction(
            customer=customer,
            user=user,
            payment_method=payment_method
        )
        return self._current_transaction
    
    @property
    def current_transaction(self) -> Optional[Transaction]:
        """Get current transaction"""
        return self._current_transaction
    
    def add_item_to_cart(self, product_id: int, quantity: int) -> tuple[bool, str]:
        """Add item to current transaction"""
        try:
            if not self._current_transaction:
                return False, "No active transaction"
            
            # Get product
            product = self.product_manager.get_product(product_id)
            if not product:
                return False, "Product not found"
            
            # Check stock availability
            if not self.product_manager.check_stock_availability(product_id, quantity):
                return False, f"Insufficient stock. Available: {product.stock_quantity}"
            
            # Add to transaction
            self._current_transaction.add_item(product, quantity)
            return True, "Item added to cart"
            
        except Exception as e:
            return False, f"Error adding item: {str(e)}"
    
    def remove_item_from_cart(self, product_id: int) -> tuple[bool, str]:
        """Remove item from current transaction"""
        try:
            if not self._current_transaction:
                return False, "No active transaction"
            
            self._current_transaction.remove_item(product_id)
            return True, "Item removed from cart"
            
        except Exception as e:
            return False, f"Error removing item: {str(e)}"
    
    def process_transaction(self, cash_received: float = 0.0) -> tuple[bool, str, int]:
        """
        Process and save transaction
        Returns: (success, message, transaction_id)
        """
        try:
            if not self._current_transaction:
                return False, "No active transaction", 0
            
            if len(self._current_transaction.items) == 0:
                return False, "Cart is empty", 0
            
            # Validate cash payment
            if self._current_transaction.payment_method == "Cash":
                self._current_transaction.cash_received = cash_received
                if cash_received < self._current_transaction.calculate_total():
                    return False, "Insufficient cash received", 0
            
            # Check stock availability for all items
            for item in self._current_transaction.items:
                if not self.product_manager.check_stock_availability(
                    item.product.product_id, item.quantity):
                    return False, f"Insufficient stock for {item.product.name}", 0
            
            # Calculate transaction details
            subtotal = self._current_transaction.calculate_subtotal()
            discount = self._current_transaction.calculate_discount()
            tax = self._current_transaction.calculate_tax()
            total = self._current_transaction.calculate_total()
            change = self._current_transaction.calculate_change()
            
            # Save transaction to database
            trans_query = """
                INSERT INTO transactions (customer_id, user_id, subtotal, discount_amount,
                                        tax_amount, total_amount, payment_method,
                                        cash_received, change_given, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            customer_id = self._current_transaction.customer.customer_id if self._current_transaction.customer else None
            
            success = self.db.execute_query(trans_query, (
                customer_id,
                self._current_transaction.user.user_id,
                subtotal,
                discount,
                tax,
                total,
                self._current_transaction.payment_method,
                cash_received if self._current_transaction.payment_method == "Cash" else None,
                change if self._current_transaction.payment_method == "Cash" else None,
                "Completed"
            ))
            
            if not success:
                return False, "Failed to save transaction", 0
            
            # Get transaction ID
            transaction_id = self.db.get_last_insert_id()
            self._current_transaction.transaction_id = transaction_id
            
            # Save transaction items
            for item in self._current_transaction.items:
                item_query = """
                    INSERT INTO transaction_items (transaction_id, product_id, quantity,
                                                  unit_price, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """
                self.db.execute_query(item_query, (
                    transaction_id,
                    item.product.product_id,
                    item.quantity,
                    item.unit_price,
                    item.get_subtotal()
                ))
                
                # Update product stock
                self.product_manager.update_stock(item.product.product_id, -item.quantity)
            
            # Update customer loyalty points
            if self._current_transaction.customer:
                loyalty_points = self._current_transaction.calculate_loyalty_points()
                self.customer_manager.update_loyalty_points(
                    self._current_transaction.customer.customer_id,
                    loyalty_points
                )
            
            return True, "Transaction completed successfully!", transaction_id
            
        except Exception as e:
            return False, f"Error processing transaction: {str(e)}", 0
    
    def cancel_transaction(self):
        """Cancel current transaction"""
        self._current_transaction = None
    
    def get_transaction(self, transaction_id: int) -> Optional[dict]:
        """Get transaction details by ID"""
        try:
            # Get transaction
            trans_query = """
                SELECT t.transaction_id, t.transaction_date, t.subtotal, t.discount_amount,
                       t.tax_amount, t.total_amount, t.payment_method, t.cash_received,
                       t.change_given, t.status, u.name as staff_name, u.username,
                       c.name as customer_name, c.customer_type
                FROM transactions t
                JOIN users u ON t.user_id = u.user_id
                LEFT JOIN customers c ON t.customer_id = c.customer_id
                WHERE t.transaction_id = %s
            """
            trans_result = self.db.fetch_one(trans_query, (transaction_id,))
            
            if not trans_result:
                return None
            
            # Get transaction items
            items_query = """
                SELECT ti.product_id, p.name, ti.quantity, ti.unit_price, ti.subtotal
                FROM transaction_items ti
                JOIN products p ON ti.product_id = p.product_id
                WHERE ti.transaction_id = %s
            """
            items_results = self.db.fetch_all(items_query, (transaction_id,))
            
            items = []
            for item in items_results:
                items.append({
                    'product_id': item[0],
                    'product_name': item[1],
                    'quantity': item[2],
                    'unit_price': float(item[3]),
                    'subtotal': float(item[4])
                })
            
            return {
                'transaction_id': trans_result[0],
                'date': trans_result[1].strftime('%Y-%m-%d %H:%M:%S'),
                'subtotal': float(trans_result[2]),
                'discount': float(trans_result[3]),
                'tax': float(trans_result[4]),
                'total': float(trans_result[5]),
                'payment_method': trans_result[6],
                'cash_received': float(trans_result[7]) if trans_result[7] else 0,
                'change_given': float(trans_result[8]) if trans_result[8] else 0,
                'status': trans_result[9],
                'staff_name': trans_result[10],
                'staff_username': trans_result[11],
                'customer_name': trans_result[12] if trans_result[12] else "Walk-in",
                'customer_type': trans_result[13] if trans_result[13] else "N/A",
                'items': items
            }
            
        except Exception as e:
            print(f"Error getting transaction: {e}")
            return None
    
    def process_refund(self, transaction_id: int) -> tuple[bool, str]:
        """Process refund for a transaction"""
        try:
            # Get transaction details
            transaction = self.get_transaction(transaction_id)
            if not transaction:
                return False, "Transaction not found"
            
            if transaction['status'] == 'Refunded':
                return False, "Transaction already refunded"
            
            # Restore stock for all items
            for item in transaction['items']:
                self.product_manager.update_stock(item['product_id'], item['quantity'])
            
            # Update transaction status
            query = """
                UPDATE transactions
                SET status = 'Refunded'
                WHERE transaction_id = %s
            """
            success = self.db.execute_query(query, (transaction_id,))
            
            if success:
                return True, "Refund processed successfully!"
            else:
                return False, "Failed to process refund"
                
        except Exception as e:
            return False, f"Error processing refund: {str(e)}"
