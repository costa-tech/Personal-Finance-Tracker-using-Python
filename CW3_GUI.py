import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import datetime

# Defining the FinanceTrackerGUI class
class FinanceTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.transactions = self.load_transactions("expenses.json")
        self.create_widgets()

    # load transactions from a JSON file
    def load_transactions(self, filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                transactions = {}
                for category, items in data.items():
                    for item in items:
                        if category.strip() not in transactions:
                            transactions[category.strip()] = []
                        transactions[category.strip()].append(item)
                return transactions
        except FileNotFoundError:
            return {}

    # Method to save transactions to a JSON file
    def save_transactions(self):
        filename = "transactions.json"
        with open(filename, "w") as file:
            json.dump(self.transactions, file, indent=4)

    # Method to create GUI widgets
    def create_widgets(self):
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview widget to display transactions
        self.transaction_tree = ttk.Treeview(self.table_frame, columns=("transaction_number", "amount", "category", "date"), show="headings")
        self.transaction_tree.heading("transaction_number", text="Transaction Number")
        self.transaction_tree.heading("amount", text="Amount")
        self.transaction_tree.heading("category", text="Category")
        self.transaction_tree.heading("date", text="Date")
        self.transaction_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for the transaction table
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.transaction_tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.transaction_tree.configure(yscrollcommand=self.scrollbar.set)

        # Search bar for filtering transactions
        self.search_bar = tk.Entry(self.root)
        self.search_bar.pack(pady=10)
        self.search_button = tk.Button(self.root, text="Search", command=self.search_transactions)
        self.search_button.pack(pady=10)

        # Sorting options dropdown menu
        sort_options = ["Date (Oldest to Newest)", "Category (A to Z)", "Amount (Smallest to Largest) \nCategory Wise", "Transaction Number (Ascending) \nCategory Wise"]
        self.sort_var = tk.StringVar(self.root)
        self.sort_var.set(sort_options[0])  # Default sorting option
        sort_dropdown = tk.OptionMenu(self.root, self.sort_var, *sort_options, command=self.sort_transactions)
        sort_dropdown.pack(pady=10)

        # Refresh button to refresh the transaction table
        self.refresh_button = tk.Button(self.root, text="Refresh", command=lambda: self.display_transactions(self.transactions))
        self.refresh_button.pack(pady=10)

    # Method to display transactions in the table
    def display_transactions(self, transactions):
        self.transaction_tree.delete(*self.transaction_tree.get_children())
        for category, data in transactions.items():
            for transaction in data:
                self.transaction_tree.insert("", tk.END, values=(
                    transaction["transaction_number"],
                    transaction["amount"],
                    category,
                    transaction["date"]
                ))
        self.save_transactions()

    # Method to filter transactions based on search criteria
    def search_transactions(self):
        search_term = self.search_bar.get().lower()
        filtered_transactions = {}
        for category, data in self.transactions.items():
            filtered_data = []
            for transaction in data:
                # Check if the search term matches any value in the transaction or the category name
                if any(term.lower() in str(value).lower() for term in search_term.split() for value in transaction.values()) or search_term.lower() in category.lower():
                    filtered_data.append(transaction)
            if filtered_data:
                filtered_transactions[category] = filtered_data
        
        # If no search results found, display a message box
        if not filtered_transactions:
            messagebox.showinfo("Search Results", "No search found.")

        self.display_transactions(filtered_transactions)

    # Method to sort transactions based on selected option
    def sort_transactions(self, selected_option):
        if selected_option == "Date (Oldest to Newest)":
            # Create a dictionary of transaction numbers and their corresponding dates
            transactions_with_dates = {}
            for category, data in self.transactions.items():
                for transaction in data:
                    transactions_with_dates[transaction["transaction_number"]] = transaction["date"]
            
            # Sort transactions by date
            sorted_transactions = sorted(transactions_with_dates.items(), key=lambda x: datetime.datetime.strptime(x[1], "%Y-%m-%d"))
            
            # Clear existing entries in the transaction tree
            self.transaction_tree.delete(*self.transaction_tree.get_children())

            # Insert sorted transactions into the transaction tree
            for transaction_number, date in sorted_transactions:
                category = next(category for category, data in self.transactions.items() if any(tx["transaction_number"] == transaction_number for tx in data))
                transaction = next(tx for tx in self.transactions[category] if tx["transaction_number"] == transaction_number)
                self.transaction_tree.insert("", tk.END, values=(
                    transaction_number,
                    transaction["amount"],
                    category,
                    date
                ))

        else:
            if selected_option == "Category (A to Z)":
                sorted_transactions = sorted(self.transactions.items(), key=lambda x: x[0])
            elif selected_option == "Amount (Smallest to Largest) \nCategory Wise":
                sorted_transactions = [(category, sorted(data, key=lambda x: float(x["amount"]))) for category, data in self.transactions.items()]
            elif selected_option == "Transaction Number (Ascending) \nCategory Wise":
                sorted_transactions = [(category, sorted(data, key=lambda x: int(x["transaction_number"]))) for category, data in self.transactions.items()]

            # Clear existing entries in the transaction tree
            self.transaction_tree.delete(*self.transaction_tree.get_children())

            # Insert sorted transactions into the transaction tree
            for category, data in sorted_transactions:
                for transaction in data:
                    self.transaction_tree.insert("", tk.END, values=(
                        transaction["transaction_number"],
                        transaction["amount"],
                        category,
                        transaction["date"]
                    ))

def main():
    root = tk.Tk()
    app = FinanceTrackerGUI(root)
    app.display_transactions(app.transactions)
    root.mainloop()

if __name__ == "__main__":
    main()
