#SD1_COURSEORK_3
#ID - 20231262

import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from CW3_GUI import FinanceTrackerGUI  

# Global dictionary to store expenses by category
expenses = {}
transaction_counter = 1  # Initialize transaction counter

# File handling functions
# Loads transactions from a JSON file.
def load_transactions():
    global expenses
    try:
        with open("expenses.json", "r") as file:
            expenses = json.load(file)
    except FileNotFoundError:
        expenses = {}  # Initialize as empty if file doesn't exist
    except json.decoder.JSONDecodeError:
        expenses = {}  # Handle invalid JSON format

# Saves transactions to the JSON file.
def save_transactions():
    with open('expenses.json', 'w+') as file:
        json.dump(expenses, file)

# Get a valid date
def valid_date(prompt):
    while True:
        date_str = input(prompt)
        try:
            date_object = datetime.strptime(date_str, "%Y-%m-%d")
            return date_object.strftime("%Y-%m-%d")  # Return formatted date string
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

# Function to open the GUI
def open_gui():
    root = tk.Tk()
    app = FinanceTrackerGUI(root)
    app.display_transactions(app.transactions)
    root.mainloop()

# main menu at the start
def main_menu():
    load_transactions()
    global transaction_counter
    # Update transaction counter based on existing transactions
    if expenses:
        transaction_counter = max(int(t["transaction_number"]) for t_list in expenses.values() for t in t_list) + 1

    while True:
        print()
        print(" ****Personal Finance Tracker**** ")
        print()
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Bulk Import Transactions from File")
        print("7. Open GUI to Display Transactions")  
        print("8. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            update_transaction()
        elif choice == '4':
            delete_transaction()
        elif choice == '5':
            display_summary()
        elif choice == '6':
            bulk_import_transactions()
        elif choice == '7':
            open_gui()  
        elif choice == '8':
            print("Exiting program.")
            save_transactions()
            break
        else:
            print("Invalid choice. Please try again.")

# Adds a new transaction.
def add_transaction():
    global transaction_counter
    category = input("Enter transaction category: ")
    while True:
        try:
            amount = float(input("Enter transaction amount: Rs."))
            break
        except ValueError:
            print("Please enter a valid amount!")

    description = input("Enter transaction description (optional): ")
    date = valid_date("Enter transaction date (YYYY-MM-DD): ")

    new_transaction = {
        "transaction_number": str(transaction_counter),
        "amount": amount,
        "description": description,
        "date": date
    }

    if category in expenses:
        expenses[category].append(new_transaction)
    else:
        expenses[category] = [new_transaction]

    save_transactions()
    print("Transaction successfully added!")
    transaction_counter += 1  # Increment transaction counter

# Displays all transactions.
def view_transactions():
    if not expenses:
        print("No transactions found.")
        return

    print("{:<15} {:<15} {:<10} {:<10} {:<15}".format(
        "Transaction #", "Category", "Amount(Rs.)", "Date", "Description"))

    for category, category_transactions in expenses.items():
        for transaction in category_transactions:
            print("{:<15} {:<15} {:<10.2f} {:<10} {:<15}".format(
                transaction["transaction_number"],
                category,
                transaction["amount"],
                transaction["date"],
                transaction["description"] if transaction["description"] else ""
            ))

# Updates an existing transaction.
def update_transaction():
    print()
    view_transactions()
    print()
    update_number = input("Enter the transaction number to update: ")

    for current_category, category_transactions in expenses.items():
        for transaction in category_transactions:
            if transaction["transaction_number"] == update_number:
                print()
                print("Transaction found:")
                print()
                print("Category:", current_category)
                print("Amount:", transaction["amount"])
                print("Date:", transaction["date"])
                print("Description:", transaction["description"] if transaction["description"] else "")
                print()

                new_amount = input("Enter the new amount or press Enter to keep current: ")
                new_description = input("Enter the new description or press Enter to keep current: ")
                new_date = valid_date("Enter the new transaction date (YYYY-MM-DD) or press Enter to keep current: ")
                new_category = input("Enter the new category or press Enter to keep current: ")

                if new_amount:
                    transaction["amount"] = float(new_amount)
                if new_description:
                    transaction["description"] = new_description
                if new_date:
                    transaction["date"] = new_date
                if new_category and new_category != current_category:
                    # Remove transaction from current category
                    category_transactions.remove(transaction)
                    if not category_transactions:  # Remove category if empty
                        del expenses[current_category]
                    # Add transaction to new category
                    if new_category in expenses:
                        expenses[new_category].append(transaction)
                    else:
                        expenses[new_category] = [transaction]

                save_transactions()
                print("Transaction successfully updated!")
                return

    print("Transaction not found.")

# Deletes a transaction.
def delete_transaction():
    print()
    view_transactions()
    print()
    delete_number = input("Enter the transaction number to delete: ")

    for category, category_transactions in expenses.items():
        for index, transaction in enumerate(category_transactions):
            if transaction["transaction_number"] == delete_number:
                category_transactions.pop(index)
                if not category_transactions:  # Remove category if empty
                    del expenses[category]
                save_transactions()
                print("Transaction successfully deleted!")
                return

    print("Transaction not found.")

# Displays a summary of expenses including totals by category.
def display_summary():
    if not expenses:
        print("No transactions found.")
        return

    total_expenses = 0
    category_totals = {}

    for category, category_transactions in expenses.items():
        category_total = sum(transaction["amount"] for transaction in category_transactions)
        category_totals[category] = category_total
        total_expenses += category_total

    print()
    print("Total Expenses: Rs.", total_expenses)
    print("Category-wise Expenses:")
    for category, total in category_totals.items():
        print(f"{category}: Rs. {total}")

    print("")

# Bulk imports transactions from a text file.
def bulk_import_transactions():
    global transaction_counter
    filename = input("Enter the filename to import transactions: ")
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    amount, date_str, category = line.split(",")
                    amount = float(amount.strip())
                    date = date_str  # Validate date
                    if date:
                        new_transaction = {
                            "transaction_number": str(transaction_counter),
                            "amount": amount,
                            "date": date,
                            "description": ""
                        }
                        if category in expenses:
                            expenses[category].append(new_transaction)
                        else:
                            expenses[category] = [new_transaction]
                        transaction_counter += 1  # Increment transaction counter

        save_transactions()
        print("Transactions imported successfully!")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred while importing transactions: {e}")


if __name__ == "__main__":
    main_menu()

