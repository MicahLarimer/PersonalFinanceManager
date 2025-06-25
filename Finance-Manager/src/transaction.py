# Transaction class for Personal Finance Manager
from datetime import datetime

class Transaction:
    """Represents a financial transaction with date, type, category, amount, and description."""
    
   
    def __init__(self,date,transaction_type,category,amount,description = ""):
        """Initialize a transaction with date, type, category, amount, and optional description."""
        # Validate date
        if isinstance(date,str):
            try:
                self.date = datetime.strptime(date, '%Y-%m-%d')
            except ValueError:        
                raise ValueError("Invalid date format. Use YYYY-MM-DD")
        elif isinstance(date, datetime):
            self.date = date
        else:
            raise TypeError("Date must be datetime or string in YYYY-MM-DD format")
        
        # Validate income
        if transaction_type not in ["income" , "expense"]:
            raise ValueError("Transaction type must be 'income' or 'expense'")
        self.transaction_type = transaction_type

        # Validate category
        if not isinstance(category,str) or not category.strip():
            raise ValueError("Category must be a non-empty string")
        self.category = category
        
        # Validate amount
        if not isinstance(amount,(int,float)):
            raise TypeError("Amount must be a number")
        if amount < 0:
            raise ValueError("Amount must be a non-negative number")
        self.amount = float(amount)

        # Validate description
        if not isinstance(description, str):
            raise ValueError("Description must be a string.")
        self.description = description

    def get_details(self):
        """Return transaction details as a dictionary."""
        return {"date": self.date.strftime('%Y-%m-%d'),
                "transaction_type": self.transaction_type,
                "category": self.category,
                "amount": self.amount,
                "description": self.description
        }

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d')} | {self.transaction_type} | {self.category} | ${self.amount:.2f} | {self.description}"
