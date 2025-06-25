import unittest
import os
import io
from contextlib import redirect_stdout
from datetime import datetime
from src.finance_manager import FinanceManager
from src.transaction import Transaction
from src.budget import Budget

class TestFinanceManager(unittest.TestCase):
    def setUp(self):
        """Set up a FinanceManager instance before each test."""
        self.manager = FinanceManager()
        for file in ["data/transactions.csv", "data/budgets.json", "data/category_spending_pie.png"]:
            if os.path.exists(file):
                os.remove(file)

    def test_add_transaction(self):
        """Test adding a valid transaction."""
        date = datetime(2025, 6, 25)
        self.manager.add_transaction(date, "income", "Salary", 1000.0, "Paycheck")
        self.assertEqual(len(self.manager.transactions), 1)
        transaction = self.manager.transactions[0]
        self.assertEqual(transaction.category, "Salary")
        self.assertEqual(transaction.amount, 1000.0)

    def test_add_budget(self):
        """Test adding a valid budget."""
        self.manager.add_budget("Food", 500.0, "June 2025")
        self.assertEqual(len(self.manager.budgets), 1)
        budget = self.manager.budgets[0]
        self.assertEqual(budget.category, "Food")
        self.assertEqual(budget.allocated_amount, 500.0)

    def test_save_load_transactions(self):
        """Test saving and loading transactions."""
        date = datetime(2025, 6, 25)
        self.manager.add_transaction(date, "expense", "Food", 50.0, "Groceries")
        self.manager.save_transactions()
        self.manager.transactions.clear()
        self.manager.load_transactions()
        self.assertEqual(len(self.manager.transactions), 1)
        transaction = self.manager.transactions[0]
        self.assertEqual(transaction.category, "Food")
        self.assertEqual(transaction.amount, 50.0)

    def test_save_load_budgets(self):
        """Test saving and loading budgets."""
        self.manager.add_budget("Food", 500.0, "June 2025")
        self.manager.budgets[0].spent_amount = 50.0
        self.manager.save_budgets()
        self.manager.budgets.clear()
        self.manager.load_budgets()
        self.assertEqual(len(self.manager.budgets), 1)
        budget = self.manager.budgets[0]
        self.assertEqual(budget.spent_amount, 50.0)

    def test_report_totals(self):
        """Test total income and expenses report."""
        date = datetime(2025, 6, 25)
        self.manager.add_transaction(date, "income", "Salary", 1000.0, "Paycheck")
        self.manager.add_transaction(date, "expense", "Food", 50.0, "Groceries")
        with io.StringIO() as buf, redirect_stdout(buf):
            self.manager.report_totals()
            output = buf.getvalue()
        self.assertIn("Total Income: $1000.00", output)
        self.assertIn("Total Expenses: $50.00", output)
        self.assertIn("Net: $950.00", output)

    def test_report_category_spending(self):
        """Test category spending report."""
        date = datetime(2025, 6, 25)
        self.manager.add_transaction(date, "expense", "Food", 50.0, "Groceries")
        self.manager.add_transaction(date, "expense", "Rent", 300.0, "Apartment")
        with io.StringIO() as buf, redirect_stdout(buf):
            self.manager.report_category_spending()
            output = buf.getvalue()
        self.assertIn("Food: $50.00", output)
        self.assertIn("Rent: $300.00", output)

    def test_report_monthly_summary(self):
        """Test monthly summary report."""
        date1 = datetime(2025, 6, 25)
        date2 = datetime(2025, 7, 1)
        self.manager.add_transaction(date1, "income", "Salary", 1000.0, "Paycheck")
        self.manager.add_transaction(date1, "expense", "Food", 50.0, "Groceries")
        self.manager.add_transaction(date2, "expense", "Rent", 300.0, "Apartment")
        with io.StringIO() as buf, redirect_stdout(buf):
            self.manager.report_monthly_summary()
            output = buf.getvalue()
        self.assertIn("2025-06: Income: $1000.00, Expenses: $50.00", output)
        self.assertIn("2025-07: Income: $0.00, Expenses: $300.00", output)

    def test_visualize_category_spending(self):
        """Test category spending visualization."""
        date = datetime(2025, 6, 25)
        self.manager.add_transaction(date, "expense", "Food", 50.0, "Groceries")
        self.manager.add_transaction(date, "expense", "Rent", 300.0, "Apartment")
        self.manager.visualize_category_spending()
        output_file = "data/category_spending_pie.png"
        self.assertTrue(os.path.exists(output_file))

if __name__ == '__main__':
    unittest.main()