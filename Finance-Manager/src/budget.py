from .transaction import Transaction

class Budget:
    """Represents a budget for a category with allocated and spent amounts."""
    
    def __init__(self, category, allocated_amount, period=""):
        """Initialize a budget with category, allocated amount, and optional period."""
        # Validate category
        if not isinstance(category, str) or not category.strip():
            raise ValueError("Category must be a non-empty string")
        self.category = category
        self.spent_amount = 0.0
        
        # Validate allocated_amount
        if not isinstance(allocated_amount, (int, float)):
            raise TypeError("Allocated amount must be a number")
        if allocated_amount <= 0:
            raise ValueError("Allocated amount must be positive")
        self.allocated_amount = float(allocated_amount)
        
        # Validate period
        if not isinstance(period, str):
            raise TypeError("Period must be a string")
        self.period = period
        
        # Initialize spent_amount
        self.spent_amount = 0.0
        
    def add_expense(self, transaction):
        """Add an expense transaction to the budget."""
        if not isinstance(transaction, Transaction):
            raise TypeError("Input must be a Transaction object")
        if transaction.transaction_type != "expense":
            raise ValueError("Transaction must be an expense")
        if transaction.category != self.category:
            raise ValueError("Transaction category must match budget category")
        
        # Update spent_amount
        self.spent_amount += transaction.amount
    
    def get_remaining(self):
        """Calculate remaining balance."""
        return self.allocated_amount - self.spent_amount
    
    def get_details(self):
        """Return budget details as a dictionary."""
        return {
            "category": self.category,
            "allocated_amount": self.allocated_amount,
            "spent_amount": self.spent_amount,
            "remaining": self.get_remaining(),
            "period": self.period
        }
    
    def __str__(self):
        """Return formatted string for display."""
        remaining = self.get_remaining()
        result = f"{self.category}: ${self.allocated_amount:.2f} allocated, ${self.spent_amount:.2f} spent, ${remaining:.2f} remaining"
        if self.period:
            result += f", Period: {self.period}"
        return result