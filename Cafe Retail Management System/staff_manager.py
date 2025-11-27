"""
Staff Manager
Handles staff/user management operations (Admin only)
"""

from typing import List, Optional, Tuple
from database import DatabaseConnection

class StaffManager:
    """Manages staff/user operations"""
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def add_staff(self, username: str, password: str, name: str, 
                  email: str = "", phone: str = "", address: str = "",
                  role: str = "staff") -> Tuple[bool, str]:
        """
        Add new staff member
        Returns: (success, message)
        """
        try:
            # Validation
            if not username or len(username.strip()) == 0:
                return False, "Username is required"
            
            if not password or len(password) < 4:
                return False, "Password must be at least 4 characters"
            
            if not name or len(name.strip()) == 0:
                return False, "Name is required"
            
            if role not in ['admin', 'staff']:
                return False, "Invalid role. Must be 'admin' or 'staff'"
            
            # Check if username already exists
            check_query = "SELECT COUNT(*) FROM users WHERE username = %s"
            result = self.db.fetch_one(check_query, (username.strip(),))
            if result and result[0] > 0:
                return False, "Username already exists"
            
            # Insert into database
            query = """
                INSERT INTO users (username, password, role, name, email, phone, address)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            success = self.db.execute_query(query, (
                username.strip(), 
                password,  # In production, hash this password
                role,
                name.strip(), 
                email, 
                phone,
                address
            ))
            
            if success:
                return True, f"Staff '{name}' added successfully!"
            else:
                return False, "Failed to add staff"
                
        except Exception as e:
            # Check if it's a column doesn't exist error (address column missing)
            if "Unknown column 'address'" in str(e):
                # Try without address
                return self._add_staff_without_address(username, password, name, email, phone, role)
            return False, f"Error adding staff: {str(e)}"
    
    def _add_staff_without_address(self, username: str, password: str, name: str,
                                    email: str, phone: str, role: str) -> Tuple[bool, str]:
        """Fallback method if address column doesn't exist"""
        try:
            query = """
                INSERT INTO users (username, password, role, name, email, phone)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            success = self.db.execute_query(query, (
                username.strip(), password, role, name.strip(), email, phone
            ))
            
            if success:
                return True, f"Staff '{name}' added successfully!"
            else:
                return False, "Failed to add staff"
        except Exception as e:
            return False, f"Error adding staff: {str(e)}"
    
    def update_staff(self, user_id: int, name: str, email: str, 
                     phone: str, address: str = "", role: str = "staff") -> Tuple[bool, str]:
        """Update staff information (not password)"""
        try:
            if not name or len(name.strip()) == 0:
                return False, "Name is required"
            
            if role not in ['admin', 'staff']:
                return False, "Invalid role"
            
            query = """
                UPDATE users
                SET name = %s, email = %s, phone = %s, role = %s
                WHERE user_id = %s
            """
            success = self.db.execute_query(query, (
                name.strip(), email, phone, role, user_id
            ))
            
            if success:
                return True, "Staff updated successfully!"
            else:
                return False, "Failed to update staff"
                
        except Exception as e:
            return False, f"Error updating staff: {str(e)}"
    
    def update_password(self, user_id: int, new_password: str) -> Tuple[bool, str]:
        """Update staff password"""
        try:
            if not new_password or len(new_password) < 4:
                return False, "Password must be at least 4 characters"
            
            query = "UPDATE users SET password = %s WHERE user_id = %s"
            success = self.db.execute_query(query, (new_password, user_id))
            
            if success:
                return True, "Password updated successfully!"
            else:
                return False, "Failed to update password"
                
        except Exception as e:
            return False, f"Error updating password: {str(e)}"
    
    def delete_staff(self, user_id: int) -> Tuple[bool, str]:
        """Delete staff member"""
        try:
            # Check if user has any transactions
            check_query = "SELECT COUNT(*) FROM transactions WHERE user_id = %s"
            result = self.db.fetch_one(check_query, (user_id,))
            
            if result and result[0] > 0:
                return False, "Cannot delete staff with transaction history. Consider deactivating instead."
            
            query = "DELETE FROM users WHERE user_id = %s"
            success = self.db.execute_query(query, (user_id,))
            
            if success:
                return True, "Staff deleted successfully!"
            else:
                return False, "Failed to delete staff"
                
        except Exception as e:
            return False, f"Error deleting staff: {str(e)}"
    
    def get_staff(self, user_id: int) -> Optional[dict]:
        """Get staff by ID"""
        try:
            query = """
                SELECT user_id, username, role, name, email, phone, created_at
                FROM users
                WHERE user_id = %s
            """
            result = self.db.fetch_one(query, (user_id,))
            
            if result:
                return {
                    'user_id': result[0],
                    'username': result[1],
                    'role': result[2],
                    'name': result[3],
                    'email': result[4] or "",
                    'phone': result[5] or "",
                    'created_at': result[6].strftime('%Y-%m-%d %H:%M') if result[6] else ""
                }
            return None
            
        except Exception as e:
            print(f"Error getting staff: {e}")
            return None
    
    def get_all_staff(self, search_term: str = "") -> List[dict]:
        """Get all staff members"""
        try:
            if search_term:
                query = """
                    SELECT user_id, username, role, name, email, phone, created_at
                    FROM users
                    WHERE name LIKE %s OR username LIKE %s OR email LIKE %s
                    ORDER BY name
                """
                search_pattern = f"%{search_term}%"
                results = self.db.fetch_all(query, (search_pattern, search_pattern, search_pattern))
            else:
                query = """
                    SELECT user_id, username, role, name, email, phone, created_at
                    FROM users
                    ORDER BY role, name
                """
                results = self.db.fetch_all(query)
            
            staff_list = []
            for row in results:
                staff_list.append({
                    'user_id': row[0],
                    'username': row[1],
                    'role': row[2],
                    'name': row[3],
                    'email': row[4] or "",
                    'phone': row[5] or "",
                    'created_at': row[6].strftime('%Y-%m-%d') if row[6] else ""
                })
            
            return staff_list
            
        except Exception as e:
            print(f"Error getting staff list: {e}")
            return []
    
    def get_staff_transaction_count(self, user_id: int) -> int:
        """Get number of transactions processed by staff"""
        try:
            query = "SELECT COUNT(*) FROM transactions WHERE user_id = %s"
            result = self.db.fetch_one(query, (user_id,))
            return result[0] if result else 0
        except Exception as e:
            print(f"Error getting transaction count: {e}")
            return 0
