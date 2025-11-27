"""
Data Models for Café Retail Management System
Demonstrates: Encapsulation, Data Hiding, Inheritance, Polymorphism, Abstraction
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

# Abstract Base Class - Demonstrates Abstraction
class Entity(ABC):
    """Abstract base class for all entities"""
    
    @abstractmethod
    def to_dict(self):
        """Convert entity to dictionary"""
        pass
    
    @abstractmethod
    def __str__(self):
        """String representation"""
        pass


# Base Person Class - Demonstrates Inheritance
class Person(Entity):
    """Base class for all person-related entities"""
    
    def __init__(self, name: str, email: str = "", phone: str = ""):
        self._name = name  # Data hiding with underscore
        self._email = email
        self._phone = phone
    
    # Encapsulation with property decorators
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Name cannot be empty")
        self._name = value.strip()
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        self._email = value
    
    @property
    def phone(self):
        return self._phone
    
    @phone.setter
    def phone(self, value):
        self._phone = value
    
    def to_dict(self):
        """Polymorphism - can be overridden"""
        return {
            'name': self._name,
            'email': self._email,
            'phone': self._phone
        }
    
    def __str__(self):
        return f"{self._name}"


# User Class - Demonstrates Inheritance from Person
class User(Person):
    """User class for staff and admin"""
    
    def __init__(self, user_id: int, username: str, password: str, 
                 role: str, name: str, email: str = "", phone: str = ""):
        super().__init__(name, email, phone)  # Call parent constructor
        self._user_id = user_id
        self._username = username
        self._password = password  # In production, use hashing
        self._role = role  # 'admin' or 'staff'
    
    @property
    def user_id(self):
        return self._user_id
    
    @property
    def username(self):
        return self._username
    
    @property
    def role(self):
        return self._role
    
    def verify_password(self, password: str) -> bool:
        """Encapsulation - password verification"""
        return self._password == password
    
    def is_admin(self) -> bool:
        """Check if user has admin role"""
        return self._role.lower() == 'admin'
    
    def to_dict(self):
        """Polymorphism - overriding parent method"""
        data = super().to_dict()
        data.update({
            'user_id': self._user_id,
            'username': self._username,
            'role': self._role
        })
        return data
    
    def __str__(self):
        return f"{self._username} ({self._role})"


# Customer Class - Demonstrates Inheritance from Person
class Customer(Person):
    """Customer class with loyalty points and membership"""
    
    # Class variable for discount rates
    DISCOUNT_RATES = {
        'Regular': 0.0,
        'Student': 0.10,  # 10% discount
        'VIP': 0.15  # 15% discount
    }
    
    def __init__(self, customer_id: int, name: str, email: str = "", 
                 phone: str = "", address: str = "", customer_type: str = "Regular",
                 loyalty_points: int = 0):
        super().__init__(name, email, phone)
        self._customer_id = customer_id
        self._address = address
        self._customer_type = customer_type
        self._loyalty_points = loyalty_points
    
    @property
    def customer_id(self):
        return self._customer_id
    
    @property
    def address(self):
        return self._address
    
    @address.setter
    def address(self, value):
        self._address = value
    
    @property
    def customer_type(self):
        return self._customer_type
    
    @customer_type.setter
    def customer_type(self, value):
        if value not in self.DISCOUNT_RATES:
            raise ValueError(f"Invalid customer type: {value}")
        self._customer_type = value
    
    @property
    def loyalty_points(self):
        return self._loyalty_points
    
    def add_loyalty_points(self, points: int):
        """Add loyalty points"""
        self._loyalty_points += points
        # Auto-upgrade to VIP if points >= 100
        if self._loyalty_points >= 100 and self._customer_type != 'VIP':
            self._customer_type = 'VIP'
    
    def get_discount_rate(self) -> float:
        """Get discount rate based on customer type"""
        return self.DISCOUNT_RATES.get(self._customer_type, 0.0)
    
    def calculate_discount(self, amount: float) -> float:
        """Calculate discount amount"""
        return amount * self.get_discount_rate()
    
    def to_dict(self):
        """Polymorphism - overriding parent method"""
        data = super().to_dict()
        data.update({
            'customer_id': self._customer_id,
            'address': self._address,
            'customer_type': self._customer_type,
            'loyalty_points': self._loyalty_points,
            'discount_rate': self.get_discount_rate()
        })
        return data
    
    def __str__(self):
        return f"{self._name} ({self._customer_type}) - {self._loyalty_points} pts"


# Product Class
class Product(Entity):
    """Product/Service class"""
    
    def __init__(self, product_id: int, name: str, description: str,
                 price: float, stock_quantity: int, low_stock_threshold: int = 10,
                 category: str = "", is_service: bool = False, service_duration: int = 0):
        self._product_id = product_id
        self._name = name
        self._description = description
        self._price = price
        self._stock_quantity = stock_quantity
        self._low_stock_threshold = low_stock_threshold
        self._category = category
        self._is_service = is_service
        self._service_duration = service_duration
    
    @property
    def product_id(self):
        return self._product_id
    
    @property
    def name(self):
        return self._name
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value
    
    @property
    def stock_quantity(self):
        return self._stock_quantity
    
    @stock_quantity.setter
    def stock_quantity(self, value):
        if value < 0:
            raise ValueError("Stock quantity cannot be negative")
        self._stock_quantity = value
    
    @property
    def category(self):
        return self._category
    
    @property
    def is_service(self):
        return self._is_service
    
    def is_low_stock(self) -> bool:
        """Check if product is low in stock"""
        return self._stock_quantity <= self._low_stock_threshold
    
    def reduce_stock(self, quantity: int) -> bool:
        """Reduce stock quantity"""
        if self._stock_quantity >= quantity:
            self._stock_quantity -= quantity
            return True
        return False
    
    def add_stock(self, quantity: int):
        """Add stock quantity"""
        self._stock_quantity += quantity
    
    def to_dict(self):
        return {
            'product_id': self._product_id,
            'name': self._name,
            'description': self._description,
            'price': self._price,
            'stock_quantity': self._stock_quantity,
            'low_stock_threshold': self._low_stock_threshold,
            'category': self._category,
            'is_service': self._is_service,
            'service_duration': self._service_duration,
            'is_low_stock': self.is_low_stock()
        }
    
    def __str__(self):
        return f"{self._name} - ${self._price:.2f} (Stock: {self._stock_quantity})"


# Transaction Item Class
class TransactionItem:
    """Item in a transaction"""
    
    def __init__(self, product: Product, quantity: int):
        self._product = product
        self._quantity = quantity
        self._unit_price = product.price
    
    @property
    def product(self):
        return self._product
    
    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, value):
        if value <= 0:
            raise ValueError("Quantity must be positive")
        self._quantity = value
    
    @property
    def unit_price(self):
        return self._unit_price
    
    def get_subtotal(self) -> float:
        """Calculate subtotal for this item"""
        return self._unit_price * self._quantity
    
    def to_dict(self):
        return {
            'product_id': self._product.product_id,
            'product_name': self._product.name,
            'quantity': self._quantity,
            'unit_price': self._unit_price,
            'subtotal': self.get_subtotal()
        }
    
    def __str__(self):
        return f"{self._product.name} x{self._quantity} = ${self.get_subtotal():.2f}"


# Transaction Class
class Transaction(Entity):
    """Transaction/Sale class"""
    
    TAX_RATE = 0.10  # 10% tax
    LOYALTY_POINTS_RATE = 1  # 1 point per dollar
    
    def __init__(self, transaction_id: int = 0, customer: Optional[Customer] = None,
                 user: User = None, payment_method: str = "Cash"):
        self._transaction_id = transaction_id
        self._customer = customer
        self._user = user
        self._items: List[TransactionItem] = []
        self._payment_method = payment_method
        self._cash_received = 0.0
        self._transaction_date = datetime.now()
        self._status = "Completed"
    
    @property
    def transaction_id(self):
        return self._transaction_id
    
    @transaction_id.setter
    def transaction_id(self, value):
        self._transaction_id = value
    
    @property
    def customer(self):
        return self._customer
    
    @property
    def user(self):
        return self._user
    
    @property
    def items(self):
        return self._items
    
    @property
    def payment_method(self):
        return self._payment_method
    
    @payment_method.setter
    def payment_method(self, value):
        self._payment_method = value
    
    @property
    def cash_received(self):
        return self._cash_received
    
    @cash_received.setter
    def cash_received(self, value):
        self._cash_received = value
    
    def add_item(self, product: Product, quantity: int):
        """Add item to transaction"""
        # Check if product already in cart
        for item in self._items:
            if item.product.product_id == product.product_id:
                item.quantity += quantity
                return
        
        # Add new item
        self._items.append(TransactionItem(product, quantity))
    
    def remove_item(self, product_id: int):
        """Remove item from transaction"""
        self._items = [item for item in self._items if item.product.product_id != product_id]
    
    def clear_items(self):
        """Clear all items"""
        self._items.clear()
    
    def calculate_subtotal(self) -> float:
        """Calculate subtotal before discount and tax"""
        return sum(item.get_subtotal() for item in self._items)
    
    def calculate_discount(self) -> float:
        """Calculate discount amount"""
        if self._customer:
            return self._customer.calculate_discount(self.calculate_subtotal())
        return 0.0
    
    def calculate_tax(self) -> float:
        """Calculate tax amount"""
        subtotal_after_discount = self.calculate_subtotal() - self.calculate_discount()
        return subtotal_after_discount * self.TAX_RATE
    
    def calculate_total(self) -> float:
        """Calculate final total"""
        subtotal = self.calculate_subtotal()
        discount = self.calculate_discount()
        tax = self.calculate_tax()
        return subtotal - discount + tax
    
    def calculate_change(self) -> float:
        """Calculate change for cash payments"""
        if self._payment_method == "Cash":
            return max(0, self._cash_received - self.calculate_total())
        return 0.0
    
    def calculate_loyalty_points(self) -> int:
        """Calculate loyalty points earned"""
        return int(self.calculate_total() * self.LOYALTY_POINTS_RATE)
    
    def to_dict(self):
        return {
            'transaction_id': self._transaction_id,
            'customer': self._customer.to_dict() if self._customer else None,
            'user': self._user.to_dict() if self._user else None,
            'items': [item.to_dict() for item in self._items],
            'subtotal': self.calculate_subtotal(),
            'discount': self.calculate_discount(),
            'tax': self.calculate_tax(),
            'total': self.calculate_total(),
            'payment_method': self._payment_method,
            'cash_received': self._cash_received,
            'change': self.calculate_change(),
            'loyalty_points': self.calculate_loyalty_points(),
            'transaction_date': self._transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self._status
        }
    
    def __str__(self):
        return f"Transaction #{self._transaction_id} - ${self.calculate_total():.2f}"
