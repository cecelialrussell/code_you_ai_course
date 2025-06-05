import csv
from datetime import datetime

def load_transactions(filename = 'financial_transactions_short.csv'):
    ERROR_LOG_FILE = 'errors.txt'
    try:
        with open(ERROR_LOG_FILE, 'w') as f:
            f.write(f"[{datetime.now()}] --- Transaction Processing Log Started ---\n")
        print(f"Log file '{ERROR_LOG_FILE}' has been created/cleared.")
    except IOError as e:
        print(f"Failed to initialize error log file '{ERROR_LOG_FILE}': {e}")
    
    transactions = []
    
    try:
        with open(filename, 'r', newline='') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                transactions.append(row)
                
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None
    
    for item in transactions:
        date_str = item['date']
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            try:
                parsed_date = datetime.strptime(date_str, "%d-%m-%Y")
            except ValueError:
                try:
                    parsed_date = datetime.strptime(date_str, "%m/%d/%Y")
                except ValueError:
                    parsed_date = None

        if parsed_date:
            item['date'] = parsed_date.strftime("%Y, %M, %d")
        else:
            with open(ERROR_LOG_FILE, 'a') as f:
                f.write(f"Error: Skipping transaction {item['transaction_id']}. Invalid date.\n")

    for item in transactions:
        try:
            if not item['amount'] or item['amount'].strip() =="":
                new_amount = 0.0
                print(f"Warning: Empty amount found for transaction {item['transaction_id']}. Setting to 0.0")
            else:
                new_amount = float(item['amount'])
            
            if item['type'] == "debit":
                item['amount'] = new_amount * -1
            elif item['type'] == "credit":
                item['amount'] = new_amount            
        except ValueError:
            with open(ERROR_LOG_FILE, 'a') as f:
                f.write(f"Error: Could not convert amount to float in transaction {item['transaction_id']}. Invalid amount.")
    
    print(f"There are {len(transactions)} transactions.")
    print(f"Transaction processing complete. Check {ERROR_LOG_FILE} for any logged issues.")

    return transactions

load_transactions()

### -----------------------------------------------------------------------------

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