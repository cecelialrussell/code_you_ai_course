import csv
from datetime import datetime

def add_transactions(filename = 'financial_transactions_short.csv'):
    transactions = []
    max_id = 0
    try:
        with open(filename, 'r', newline='') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                transactions.append(row)
                current_id = int(row['transaction_id'])
                if current_id > max_id:
                    max_id = current_id                
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None
    transaction_count = len(transactions)

    print("--- Add New Transaction ---")
    
    transaction_id = max_id + 1

    transaction_date = input("Enter date (YYYY-MM-DD): ")
    try:
        date = datetime.strptime(transaction_date, "%Y-%m-%d")
    except ValueError:
        print(f"Error: Date {transaction_date} does not match expected format.")

    customer_id = input("Enter customer ID: ")
    type = input("Enter type (credit/debit/transfer): ").strip()
    
    if not type:
        print("Transaction type cannot be empty. Aborting...")
        return
    
    while True:
        amount_str = input("Enter amount: ").strip()
        try:
            amount = float(amount_str)
            break
        except ValueError:
            print("Invalid amount. Please enter numerical value.")
    
    description = input("Enter description: ").strip()


    new_row = {'transaction_id': transaction_id, 'date': date, 'customer_id': customer_id, 'amount': amount, 'type': type, 'description': description}

    try:
        fieldnames = ['transaction_id', 'date', 'customer_id', 'amount', 'type', 'description']
        with open(filename, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(new_row)
        print(f"Enter date (YYYY-MM-DD): {date}")
        print(f"Enter customer ID: {customer_id}")
        print(f"Enter amount: {amount}")
        print(f"Enter type (credit/debit/transfer): {type}")
        print(f"Enter description: {description}")
        print(f"Transaction added!")
    except IOError as e:
        print(f"Error writing to file '{filename}': {e}")

add_transactions()