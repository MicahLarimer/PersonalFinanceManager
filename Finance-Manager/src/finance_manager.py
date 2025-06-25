import csv
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from .transaction import Transaction
from .budget import Budget

class FinanceManager:
    def __init__(self):
        """Initialize lists, file paths, and load existing data."""
        self.transactions = []
        self.budgets = []
        self.transaction_file = "data/transactions.csv"
        self.budget_file = "data/budgets.json"
        os.makedirs("data", exist_ok=True)
        try:
            self.load_transactions()
            self.load_budgets()
        except Exception as e:
            print(f"Error loading data on startup: {e}")

    def add_transaction(self, date, transaction_type, category, amount, description=""):
        """Add a transaction and update budget if expense."""
        new_transaction = Transaction(date, transaction_type, category, amount, description)
        self.transactions.append(new_transaction)
        if transaction_type == "expense":
            for budget in self.budgets:
                if budget.category == category:
                    budget.add_expense(new_transaction)
                    break
            else:
                print(f"No budget found for category '{category}'")

    def add_budget(self, category, allocated_amount, period=""):
        """Add a budget, checking for duplicates."""
        for budget in self.budgets:
            if budget.category == category:
                raise ValueError(f"Budget for category '{category}' already exists")
        new_budget = Budget(category, allocated_amount, period)
        self.budgets.append(new_budget)

    def view_transactions(self):
        """View all transactions."""
        if not self.transactions:
            print("No transactions found")
        else:
            for transaction in self.transactions:
                print(transaction)

    def view_budgets(self):
        """View all budgets."""
        if not self.budgets:
            print("No budgets found")
        else:
            for budget in self.budgets:
                print(budget)

    def save_transactions(self):
        """Save transactions to CSV file."""
        try:
            with open(self.transaction_file, mode='w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["date", "transaction_type", "category", "amount", "description"])
                for transaction in self.transactions:
                    details = transaction.get_details()
                    writer.writerow([
                        details["date"],
                        details["transaction_type"],
                        details["category"],
                        details["amount"],
                        details["description"]
                    ])
        except (PermissionError, OSError) as e:
            print(f"Error saving transactions: {e}")

    def load_transactions(self):
        """Load transactions from CSV file."""
        self.transactions.clear()
        if not os.path.exists(self.transaction_file):
            return
        try:
            with open(self.transaction_file, mode='r', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file)
                try:
                    next(reader)
                except StopIteration:
                    return
                for row in reader:
                    if len(row) != 5:
                        print(f"Skipping invalid transaction row: {row}")
                        continue
                    try:
                        parsed_date = datetime.strptime(row[0], "%Y-%m-%d")
                        amount = float(row[3])
                        transaction = Transaction(parsed_date, row[1], row[2], amount, row[4])
                        self.transactions.append(transaction)
                    except (ValueError, TypeError) as e:
                        print(f"Skipping invalid transaction row: {row}")
        except (PermissionError, OSError) as e:
            print(f"Error loading transactions: {e}")

    def save_budgets(self):
        """Save budgets to JSON file."""
        budget_data = []
        for budget in self.budgets:
            details = budget.get_details()
            budget_data.append(details)
        try:
            with open(self.budget_file, mode='w', encoding='utf-8') as json_file:
                json.dump(budget_data, json_file, indent=4)
        except (PermissionError, OSError) as e:
            print(f"Error saving budgets: {e}")

    def load_budgets(self):
        """Load budgets from JSON file."""
        self.budgets.clear()
        if not os.path.exists(self.budget_file):
            return
        try:
            with open(self.budget_file, mode='r', encoding='utf-8') as json_file:
                budget_data = json.load(json_file)
                for budget_dict in budget_data:
                    try:
                        budget = Budget(
                            budget_dict["category"],
                            budget_dict["allocated_amount"],
                            budget_dict["period"]
                        )
                        budget.spent_amount = budget_dict["spent_amount"]
                        self.budgets.append(budget)
                    except (KeyError, ValueError) as e:
                        print(f"Skipping invalid budget entry: {budget_dict}")
        except (PermissionError, OSError) as e:
            print(f"Error loading budgets: {e}")

    def report_totals(self):
        """Report total income, expenses, and net balance."""
        total_income = 0.0
        total_expenses = 0.0
        for transaction in self.transactions:
            if transaction.transaction_type == "income":
                total_income += transaction.amount
            elif transaction.transaction_type == "expense":
                total_expenses += transaction.amount
        if total_income == 0.0 and total_expenses == 0.0:
            print("No transactions available for report")
        else:
            net = total_income - total_expenses
            print(f"Total Income: ${total_income:.2f}, Total Expenses: ${total_expenses:.2f}, Net: ${net:.2f}")

    def report_category_spending(self):
        """Report expenses by category."""
        category_totals = {}
        for transaction in self.transactions:
            if transaction.transaction_type == "expense":
                category = transaction.category
                amount = transaction.amount
                category_totals[category] = category_totals.get(category, 0.0) + amount
        if not category_totals:
            print("No expenses available for report")
        else:
            print("Category Spending Breakdown:")
            for category, total in category_totals.items():
                print(f"{category}: ${total:.2f}")

    def report_monthly_summary(self):
        """Report income and expenses by month."""
        monthly_totals = {}
        for transaction in self.transactions:
            month = transaction.date.strftime("%Y-%m")
            if month not in monthly_totals:
                monthly_totals[month] = {"income": 0.0, "expenses": 0.0}
            if transaction.transaction_type == "income":
                monthly_totals[month]["income"] += transaction.amount
            elif transaction.transaction_type == "expense":
                monthly_totals[month]["expenses"] += transaction.amount
        if not monthly_totals:
            print("No transactions available for report")
        else:
            print("Monthly Summary:")
            for month in sorted(monthly_totals.keys()):
                totals = monthly_totals[month]
                print(f"{month}: Income: ${totals['income']:.2f}, Expenses: ${totals['expenses']:.2f}")

    def visualize_category_spending(self):
        """Create a pie chart of expenses by category."""
        category_totals = {}
        for transaction in self.transactions:
            if transaction.transaction_type == "expense":
                category = transaction.category
                amount = transaction.amount
                category_totals[category] = category_totals.get(category, 0.0) + amount
        if not category_totals:
            print("No expenses available for visualization")
            return
        categories = list(category_totals.keys())
        amounts = list(category_totals.values())
        plt.figure(figsize=(8, 6))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title("Category Spending Breakdown")
        output_file = "data/category_spending_pie.png"
        plt.savefig(output_file)
        plt.close()
        print(f"Pie chart saved to {output_file}")

    def run_menu(self):
        """Run command-line menu for user interaction."""
        while True:
            print("\n--- Personal Finance Manager ---")
            print("1. Add transaction")
            print("2. Add budget")
            print("3. View transactions")
            print("4. View budgets")
            print("5. Save data")
            print("6. Load data")
            print("7. Report: Total Income and Expenses")
            print("8. Report: Category Spending Breakdown")
            print("9. Report: Monthly Summary")
            print("10. Visualize: Category Spending Pie Chart")
            print("11. Exit")
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                try:
                    date_str = input("Enter date (YYYY-MM-DD): ").strip()
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                    transaction_type = input("Enter type (income/expense): ").lower().strip()
                    category = input("Enter category: ").strip()
                    amount = float(input("Enter amount: "))
                    description = input("Enter description (optional): ").strip()
                    self.add_transaction(date, transaction_type, category, amount, description)
                except ValueError as e:
                    print(f"Invalid input: {e}")
            elif choice == "2":
                try:
                    category = input("Enter budget category: ").strip()
                    allocated_amount = float(input("Enter allocated amount: "))
                    period = input("Enter budget period (optional): ").strip()
                    self.add_budget(category, allocated_amount, period)
                except ValueError as e:
                    print(f"Invalid input: {e}")
            elif choice == "3":
                self.view_transactions()
            elif choice == "4":
                self.view_budgets()
            elif choice == "5":
                self.save_transactions()
                self.save_budgets()
                print("Data saved successfully")
            elif choice == "6":
                self.load_transactions()
                self.load_budgets()
                print("Data loaded successfully")
            elif choice == "7":
                self.report_totals()
            elif choice == "8":
                self.report_category_spending()
            elif choice == "9":
                self.report_monthly_summary()
            elif choice == "10":
                self.visualize_category_spending()
            elif choice == "11":
                print("Exiting. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")