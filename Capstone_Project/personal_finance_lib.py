import csv
from datetime import datetime

transactions = []

def load_transactions(filename = 'financial_transactions_short.csv'):
    global transactions
    ERROR_LOG_FILE = 'errors.txt'
    try:
        with open(ERROR_LOG_FILE, 'w') as f:
            f.write(f"[{datetime.now()}] --- Transaction Processing Log Started ---\n")
        print(f"Log file '{ERROR_LOG_FILE}' has been created/cleared.")
    except IOError as e:
        print(f"Failed to initialize error log file '{ERROR_LOG_FILE}': {e}")
      
    transactions.clear()
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
            if not item['amount']:
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


    print({len(transactions)})
    print(f"There are {len(transactions)} transactions.")
    print(f"Transaction processing complete. Check {ERROR_LOG_FILE} for any logged issues.")

    return transactions

#---------------------------------------------------------------------

def add_transactions(filename = 'financial_transactions_short.csv'):
    global transactions
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
   
    print("--- Add New Transaction ---")
    
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
      
    description = input("Enter description for transaction: ").strip()

    try:
        new_transaction = {'transaction_id': transaction_id, 'date': date_str, 'customer_id': customer_id, 'amount': amount, 'type': type, 'description': description}
        transactions.append(new_transaction)
        print(f"Enter date (YYYY-MM-DD): {date_str}")
        print(f"Enter customer ID: {customer_id}")
        print(f"Enter amount: {amount}")
        print(f"Enter type (credit/debit/transfer): {type}")
        print(f"Enter description: {description}")
        print(f"Transaction added!")
        print(transactions)
    except IOError as e:
        print(f"Error writing to file '{filename}': {e}")

    #----------------------------------------------------

def view_transactions(filename = 'financial_transactions_short.csv'):
    global transactions
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

#-----------------------------------------------------

def update_transactions(filename='financial_transactions_short.csv'):
    global transactions
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

    if transactions is None:
        print("Cannot update transactions as no data was loaded.")
        return
    
    print("\nUpdating:")

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

    while True:
        try:
            selection = int(input(f"Select transaction (1-{len(transactions)}): "))
            if 1 <= selection <= len(transactions):
                selected_transaction_index = selection - 1
                break
            else:
                print(f"Invalid selection. Please enter a number between 1 and {len(transactions)}")
        except ValueError:
            print("Invalid input. Please enter a number.")

    selected_transaction = transactions[selected_transaction_index]

    while True:
        field_to_change = input("Change which field? (description, type, amount): ").strip().lower()
        if field_to_change in ['description', 'type', 'amount']:
            break
        else:
            print("Invalid field. Please choose from 'description', 'type', or 'amount'.")
    
    new_value = input(f"New {field_to_change}: ").strip()

    if field_to_change == 'amount':
        try:
            float(new_value)
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
            return
    
    selected_transaction[field_to_change] = new_value

    try:
        if transactions:
            fieldnames = transactions[0].keys()
        else:
            fieldnames = [col[0] for col in columns]
        
        with open(filename, 'w', newline='') as file:
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(transactions)
        print(f"Select transaction (1-{len(transactions)}): {selection}")
        print(f"Change which field? (description, type, amount): {field_to_change}")
        print(f"New {field_to_change}: {new_value}")
        print("Transaction updated!")
    except IOError as e:
        print(f"Error writing updated transactions to '{filename}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred during file write: {e}")

#---------------------------------------------------------------------

def delete_transactions(filename='financial_transactions_short.csv'):
    global transactions
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

    if not transactions:
        print("Cannot delete transactions as no data was loaded.")
        return
    
    print("\nTransactions available for deletion:")

    columns = [('transaction_id', 'ID', 6), ('date', 'Date', 12), ('customer_id', 'Customer', 10),
               ('amount', 'Amount', 12), ('type', 'Type', 10), ('description', 'Description', 40)]
    
    header_parts = []
    separator_parts = []
    for key, display_name, width in columns:
        header_parts.append(f"{display_name:<{width}}")
        separator_parts.append("-" * width)
    print(" | ".join(header_parts))
    print(" | ".join(separator_parts))

    for i, transaction in enumerate(transactions):
        row_values = []
        transaction_display_id = i + 1
        row_values.append(f"{transaction_display_id:<{columns[0][2]}}")
        
        for key, _, width in columns[1:]:
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

    while True:
        try:
            selection = int(input(f"Select transaction to delete (1-{len(transactions)}): "))
            if 1 <= selection <= len(transactions):
                selected_transaction_index = selection - 1
                break
            else:
                print(f"Invalid selection. Please enter a number between 1 and {len(transactions)}")
        except ValueError:
            print("Invalid input. Please enter a number.")

    selected_transaction = transactions[selected_transaction_index]

    print("\nYou have selected the following transaction for deletion: ")
    print("-" * 60)
    for key, display_name, _ in columns:
        value = selected_transaction.get(key, 'N/A')
        if key == 'amount':
            try:
                value = f"{float(value):.2f}"
            except (ValueError, TypeError):
                value = "N/A"
        print(f"{display_name}: {value}")
    print("-" * 60)

    confirm = input("Are you sure you want to delete this transaction? (yes/no): ").strip().lower()

    if confirm == 'yes':
        del transactions[selected_transaction_index]
        try:
            if transactions:
                fieldnames = transactions[0].keys()
            else:
                fieldnames = [col[0] for col in columns]
            with open(filename, 'w', newline='') as file:
                csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
                csv_writer.writeheader()
                csv_writer.writerows(transactions)
            print(f"Select transaction (1 - {len(transactions)}): {selection}")
            print(f"Are you sure? (yes/no): {confirm}")
            print("Transaction deleted successfully!")
        except IOError as e:
            print(f"Error writing updated transactions to '{filename}': {e}")
        except Exception as e:
            print(f"An unexpected error occurred during file write: {e}")
    else:
        print("Transaction deletion cancelled.")