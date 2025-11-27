"""
Product/Inventory Manager
Handles product and inventory operations
Demonstrates: Encapsulation, Control Structures
"""

from typing import List, Optional
from models import Product
from database import DatabaseConnection

class ProductManager:
    """Manages product and inventory operations"""
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def add_product(self, name: str, description: str, price: float,
                   stock_quantity: int, low_stock_threshold: int,
                   category: str, is_service: bool = False,
                   service_duration: int = 0) -> tuple[bool, str]:
        """
        Add new product
        Returns: (success, message)
        """
        try:
            # Validation
            if not name or len(name.strip()) == 0:
                return False, "Product name is required"
            
            if price < 0:
                return False, "Price cannot be negative"
            
            if stock_quantity < 0:
                return False, "Stock quantity cannot be negative"
            
            # Insert into database
            query = """
                INSERT INTO products (name, description, price, stock_quantity,
                                    low_stock_threshold, category, is_service, service_duration)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            success = self.db.execute_query(query, (
                name.strip(), description, price, stock_quantity,
                low_stock_threshold, category, is_service, service_duration
            ))
            
            if success:
                return True, "Product added successfully!"
            else:
                return False, "Failed to add product"
                
        except Exception as e:
            return False, f"Error adding product: {str(e)}"
    
    def update_product(self, product_id: int, name: str, description: str,
                      price: float, stock_quantity: int, low_stock_threshold: int,
                      category: str) -> tuple[bool, str]:
        """Update product information"""
        try:
            if not name or len(name.strip()) == 0:
                return False, "Product name is required"
            
            if price < 0:
                return False, "Price cannot be negative"
            
            if stock_quantity < 0:
                return False, "Stock quantity cannot be negative"
            
            query = """
                UPDATE products
                SET name = %s, description = %s, price = %s, stock_quantity = %s,
                    low_stock_threshold = %s, category = %s
                WHERE product_id = %s
            """
            success = self.db.execute_query(query, (
                name.strip(), description, price, stock_quantity,
                low_stock_threshold, category, product_id
            ))
            
            if success:
                return True, "Product updated successfully!"
            else:
                return False, "Failed to update product"
                
        except Exception as e:
            return False, f"Error updating product: {str(e)}"
    
    def get_product(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        try:
            query = """
                SELECT product_id, name, description, price, stock_quantity,
                       low_stock_threshold, category, is_service, service_duration
                FROM products
                WHERE product_id = %s
            """
            result = self.db.fetch_one(query, (product_id,))
            
            if result:
                return Product(
                    product_id=result[0],
                    name=result[1],
                    description=result[2] or "",
                    price=float(result[3]),
                    stock_quantity=result[4],
                    low_stock_threshold=result[5],
                    category=result[6] or "",
                    is_service=bool(result[7]),
                    service_duration=result[8]
                )
            return None
            
        except Exception as e:
            print(f"Error getting product: {e}")
            return None
    
    def search_products(self, search_term: str = "", category: str = "") -> List[Product]:
        """Search products by name or category"""
        try:
            # Build query with control structures
            if search_term and category:
                query = """
                    SELECT product_id, name, description, price, stock_quantity,
                           low_stock_threshold, category, is_service, service_duration
                    FROM products
                    WHERE (name LIKE %s OR description LIKE %s) AND category = %s
                    ORDER BY name
                """
                search_pattern = f"%{search_term}%"
                results = self.db.fetch_all(query, (search_pattern, search_pattern, category))
            elif search_term:
                query = """
                    SELECT product_id, name, description, price, stock_quantity,
                           low_stock_threshold, category, is_service, service_duration
                    FROM products
                    WHERE name LIKE %s OR description LIKE %s
                    ORDER BY name
                """
                search_pattern = f"%{search_term}%"
                results = self.db.fetch_all(query, (search_pattern, search_pattern))
            elif category:
                query = """
                    SELECT product_id, name, description, price, stock_quantity,
                           low_stock_threshold, category, is_service, service_duration
                    FROM products
                    WHERE category = %s
                    ORDER BY name
                """
                results = self.db.fetch_all(query, (category,))
            else:
                query = """
                    SELECT product_id, name, description, price, stock_quantity,
                           low_stock_threshold, category, is_service, service_duration
                    FROM products
                    ORDER BY name
                """
                results = self.db.fetch_all(query)
            
            # Use list comprehension - data structure
            products = [
                Product(
                    product_id=row[0],
                    name=row[1],
                    description=row[2] or "",
                    price=float(row[3]),
                    stock_quantity=row[4],
                    low_stock_threshold=row[5],
                    category=row[6] or "",
                    is_service=bool(row[7]),
                    service_duration=row[8]
                )
                for row in results
            ]
            
            return products
            
        except Exception as e:
            print(f"Error searching products: {e}")
            return []
    
    def get_low_stock_products(self) -> List[Product]:
        """Get products with low stock levels"""
        try:
            query = """
                SELECT product_id, name, description, price, stock_quantity,
                       low_stock_threshold, category, is_service, service_duration
                FROM products
                WHERE stock_quantity <= low_stock_threshold
                ORDER BY stock_quantity ASC
            """
            results = self.db.fetch_all(query)
            
            products = []
            for row in results:
                products.append(Product(
                    product_id=row[0],
                    name=row[1],
                    description=row[2] or "",
                    price=float(row[3]),
                    stock_quantity=row[4],
                    low_stock_threshold=row[5],
                    category=row[6] or "",
                    is_service=bool(row[7]),
                    service_duration=row[8]
                ))
            
            return products
            
        except Exception as e:
            print(f"Error getting low stock products: {e}")
            return []
    
    def update_stock(self, product_id: int, quantity_change: int) -> tuple[bool, str]:
        """
        Update stock quantity
        quantity_change: positive to add stock, negative to reduce
        """
        try:
            product = self.get_product(product_id)
            if not product:
                return False, "Product not found"
            
            new_quantity = product.stock_quantity + quantity_change
            
            if new_quantity < 0:
                return False, "Insufficient stock"
            
            query = """
                UPDATE products
                SET stock_quantity = %s
                WHERE product_id = %s
            """
            success = self.db.execute_query(query, (new_quantity, product_id))
            
            if success:
                return True, "Stock updated successfully!"
            else:
                return False, "Failed to update stock"
                
        except Exception as e:
            return False, f"Error updating stock: {str(e)}"
    
    def get_all_categories(self) -> List[str]:
        """Get list of all product categories"""
        try:
            query = """
                SELECT DISTINCT category
                FROM products
                WHERE category IS NOT NULL AND category != ''
                ORDER BY category
            """
            results = self.db.fetch_all(query)
            return [row[0] for row in results]
            
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []
    
    def check_stock_availability(self, product_id: int, quantity: int) -> bool:
        """Check if sufficient stock is available"""
        product = self.get_product(product_id)
        if product:
            return product.stock_quantity >= quantity
        return False
