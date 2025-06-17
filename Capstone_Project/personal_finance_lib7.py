import csv
from datetime import datetime
transactions = []

def load_transactions(filename = 'financial_transactions_short.csv'):
    ERROR_LOG_FILE = 'errors.txt'
    try:
        with open(ERROR_LOG_FILE, 'w') as f:
            f.write(f"[{datetime.now()}] --- Transaction Processing Log Started ---\n")
        print(f"Log file '{ERROR_LOG_FILE}' has been created/cleared.")
    except IOError as e:
        print(f"Failed to initialize error log file '{ERROR_LOG_FILE}': {e}")
      
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
            item['date'] = parsed_date.strftime("%Y-%m-%d")
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

def add_transactions(transactions):
    max_id = 0
   
    print("--- Add New Transaction ---")
    
    for transaction in transactions:
        if int(transaction['transaction_id']) > max_id:
            max_id = int(transaction['transaction_id'])
    
    transaction_id = max_id + 1

    while True:
        date_str = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    customer_id = input("Enter customer ID: ")

    while True:
        amount_str = input("Enter amount: ").strip()
        try:
            amount = float(amount_str)
            break
        except ValueError:
            print("Invalid amount. Please enter numerical value.")

    type = input("Enter type (credit/debit/transfer): ").strip()
    if not type:
        print("Transaction type cannot be empty. Aborting...")
        return
    else:
        if type == "debit":
            amount = amount * -1
        else:
            amount = amount
            
    description = input("Enter description for transaction: ").strip()

    try:
        new_transaction = {
            'transaction_id': transaction_id,
            'date': date_str,
            'customer_id': customer_id,
            'amount': amount,
            'type': type,  
            'description': description
        }
        transactions.append(new_transaction)
        print(f"Enter date (YYYY-MM-DD): {date_str}")
        print(f"Enter customer ID: {customer_id}")
        print(f"Enter amount: {amount}")
        print(f"Enter type (credit/debit/transfer): {type}")
        print(f"Enter description: {description}")
        print(f"Transaction added!")
        print(transactions[-1])
    except Exception as e: # A more general exception for unexpected issues during transaction creation/append
        print(f"An unexpected error occurred while adding the transaction: {e}")

def view_transactions(transactions):
    print("\n--- Viewing Transactions ---")
    columns = [('transaction_id', 'ID', 6), ('date', 'Date', 12), ('customer_id', 'Customer', 10),
               ('amount', 'Amount', 12), ('type', 'Type', 10), ('description', 'Description', 40)]
    
    header_parts = []
    separator_parts = []
    for key, display_name, width in columns:
        header_parts.append(f"{display_name:<{width}}")
        separator_parts.append("-" * width)
    print(" | ".join(header_parts))
    print(" | ".join(separator_parts))

    for transaction in transactions:
        row_values = []
        for key, _, width in columns:
            value = transaction.get(key, '')

            if key == 'amount':
                try:
                    value = f"{float(value):.2f}"
                except (ValueError, TypeError):
                    value = "N/A"

            str_value = str(value)

            if len(str_value) > width:
                str_value = str_value[:width - 3] + "..."

            row_values.append(f"{str_value:<{width}}")

        print(" | ".join(row_values))

def update_transactions(transactions):
    print("\n--- Updating Transaction ---")

    if not transactions:
        print("No transactions to update.")
        return
    
    view_transactions(transactions)

    while True:
        try:
            transaction_to_update = int(input("\nEnter the ID of the transaction to update (or 0 to cancel): "))
            if transaction_to_update == 0:
                print("Update cancelled.")
                return
            break
        except ValueError:
            print("Invalid input. Please enter a numerical transaction ID.")

    found = None
    for transaction in transactions:
        if int(transaction.get('transaction_id', 0)) == transaction_to_update:
            found = transaction
            break
    
    if not found:
        print(f"Transaction with ID {transaction_to_update} not found.")
        return
    
    print(f"\nTransaction found. Current details for {transaction_to_update}: ")
    print(f"1. Description: {found.get('description', '')}")
    print(f"2. Type: {found.get('type', '')}")
    print(f"3. Amount: {found.get('amount', 0)}")

    while True:
        field_choice = input("Enter the number of the field to update (1-3): ")

        if field_choice == '0':
            print("Update cancelled.")
            return
        
        if field_choice == '1':
            new_description = input("Enter new description: ").strip()
            found['description'] = new_description
            print("Description updated successfully.")
            break
        elif field_choice == '2':
            while True:
                new_type = input("Enter new type (credit/debit/transfer): ").strip()
                if new_type in ["credit", "debit", "transfer"]:
                    if new_type == "debit":
                        found['type'] = new_type
                        found['amount'] = found['amount'] * -1
                        continue
                    else:
                        found['type'] = new_type
                        print("Type updated successfully.")
                        break
                else:
                    print("Invalid type. Please enter 'credit', 'debit', or 'transfer'.")
            break
        elif field_choice == '3':
            while True:
                try:
                    new_amount = float(input("Enter new amount: ").strip())
                    if found.get('type') == 'debit':
                        found['amount'] = new_amount * -1
                    else:
                        found['amount'] = new_amount
                    print("Amount updated successfully.")
                    break
                except ValueError:
                    print("Invalid amount. Please enter a numerical value.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 0 to cancel.")
    

def delete_transactions(transactions):
    print("\n--- Delete Transaction ---")

    if not transactions:
        print("Cannot delete transactions as no data was loaded.")
        return
    
    print("\nTransactions available for deletion:")

    view_transactions(transactions)

    while True:
        try:
            transaction_to_delete = int(input("\nEnter the ID of the transaction to delete (or 0 to cancel): "))

            if transaction_to_delete == 0:
                print("Deletion cancelled.")
                return
            
            found = False
            for i, transaction in enumerate(transactions):
                if transaction['transaction_id'] == transaction_to_delete:
                    print(f"\nFound transaction with ID {transaction_to_delete}:")
                    print(f"Date: {transaction['date']}, Customer: {transaction['customer_id']}, Amount: {transaction['amount']:.2f}, Type: {transaction['type']}")
                    confirm = input("Are you sure your want to delete this transaction? (yes/no): ").strip().lower()

                    if confirm == 'yes':
                        del transactions[i]
                        print(f"Transaction with ID {transaction_to_delete} deleted successfully.")
                    else:
                        print("Deletion aborted by user.")
                    found = True
                    break
            if not found:
                print(f"Transaction with ID {transaction_to_delete} not found.")
            
            break

        except ValueError:
            print("Invalid input. Please enter a numerical transaction ID.")
        except Exception as e:
            print(f"An unexpcted error occurred: {e}")
