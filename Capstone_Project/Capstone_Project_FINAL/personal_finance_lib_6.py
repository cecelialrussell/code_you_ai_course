import csv
from datetime import datetime
import os 

transactions = []
max_id = 0
ERROR_LOG_FILE = 'errors.txt'

def _log_error(message):
    with open(ERROR_LOG_FILE, 'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def load_transactions(filename='financial_transactions_short.csv'):
    global transactions 
    global max_id 

    transactions = [] 
    current_max_id = 0

    try:
        with open(filename, 'r', newline='') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                processed_row = row.copy() 

                date_str = processed_row.get('date', '').strip()
                parsed_date = None
                date_formats = ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y"] 

                if date_str:
                     for fmt in date_formats:
                        try:
                            parsed_date = datetime.strptime(date_str, fmt)
                            break 
                        except ValueError:
                            continue 
                    
                if parsed_date:
                    processed_row['date'] = parsed_date
                else:
                    _log_error(f"Warning: Empty date found for transaction {processed_row.get('transaction_id', 'N/A')}. Setting date to None.")
                    processed_row['date'] = None

                try:
                    amount_str = processed_row.get('amount', '').strip()
                    new_amount = 0.0 
                    
                    if not amount_str:
                        _log_error(f"Warning: Empty amount found for transaction {processed_row.get('transaction_id', 'N/A')}. Setting to 0.0.")
                    else:
                        new_amount = float(amount_str) 
                    
                    transaction_type = processed_row.get('type', '').strip().lower()
                    if transaction_type == "debit":
                        processed_row['amount'] = new_amount * -1 
                    elif transaction_type == 'credit':
                        processed_row['amount'] = new_amount 
                    else:
                        processed_row['amount'] = new_amount 
                        if transaction_type: 
                            _log_error(f"Warning: Unrecognizable type '{transaction_type}' for transaction {processed_row.get('transaction_id', 'N/A')}. Amount stored as is.")
                except (ValueError, TypeError):
                    _log_error(f"Error: Could not convert amount to float in transaction {processed_row.get('transaction_id', 'N/A')}. Invalid amount '{processed_row.get('amount', '')}'.")
                    processed_row['amount'] = 0.0 

                transaction_id_val = processed_row.get('transaction_id')
                if transaction_id_val is not None:
                    try:
                        current_max_id = max(current_max_id, int(transaction_id_val))
                    except (ValueError, TypeError):
                        _log_error(f"Warning: Invalid transaction_id '{transaction_id_val}' found. Not using for max_id calculation.")

                transactions.append(processed_row)

        max_id = current_max_id 

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found. No transactions loaded.")
        _log_error(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred during file loading: {e}")
        _log_error(f"An unexpected error occurred during file loading: {e}")
    
    print(f"\n--- Load Report ---")
    print(f"There are {len(transactions)} transactions loaded.")
    print(f"Current maximum transaction ID: {max_id}")
    print(f"Transaction processing complete. Check {ERROR_LOG_FILE} for any logged issues.")

def add_transactions():

    global transactions
    global max_id

    current_max_id_in_memory = 0
    for t in transactions:
        try:
            current_max_id_in_memory = max(current_max_id_in_memory, int(t.get('transaction_id', 0)))
        except (ValueError, TypeError):
            pass

    transaction_id = current_max_id_in_memory + 1
    max_id = transaction_id 

    print("\n--- Add New Transaction ---")
    
    while True:
        date_str = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    customer_id = input("Enter customer ID: ").strip()
    if not customer_id:
        _log_error("Warning: Customer ID cannot be empty. Setting to 'N/A'.")
        customer_id = 'N/A' 

    while True:
        amount_str = input("Enter amount: ").strip()
        try:
            amount = float(amount_str)
            break
        except ValueError:
            print("Invalid amount. Please enter a numerical value.")

    transaction_type = input("Enter type (credit/debit/transfer): ").strip().lower()
    if not transaction_type:
        print("Transaction type cannot be empty. Aborting new transaction.")
        return 
        
    description = input("Enter description for transaction: ").strip()

    try:
        new_transaction = {
            'transaction_id': transaction_id,
            'date': date_str, 
            'customer_id': customer_id,
            'amount': amount,
            'type': transaction_type, 
            'description': description
        }
        transactions.append(new_transaction)
        print(f"\nTransaction {transaction_id} added successfully!")
        print(new_transaction) 
    except Exception as e: 
        print(f"Unable to add transaction: {e}")
        _log_error(f"Error adding transaction: {e}")


def view_transactions(transactions): 

    if not transactions:
        print(f"\nNo transactions to display. Load or add some transactions.")
        return
    
    print("\n--- Current Transactions ---")
    columns = [
        ('transaction_id', 'ID', 6), 
        ('date', 'Date', 12), 
        ('customer_id', 'Customer', 10),
        ('amount', 'Amount', 12), 
        ('type', 'Type', 10), 
        ('description', 'Description', 40)
    ]
    
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

def update_transactions(filename='financial_transactions_short.csv'):
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

def delete_transactions(transactions_list):

    print("\n--- Delete Transaction ---")
    if not transactions_list:
        print("No transactions to delete. The list is empty.")
        return transactions_list 

    view_transactions(transactions_list) 

    try:
        id_to_delete = int(input("Enter the ID of the transaction to delete: "))
    except ValueError:
        print("Invalid input. Please enter a numerical transaction ID.")
        return transactions_list 
    
    found = False
    new_transactions = []
    deleted_count = 0

    for transaction in transactions_list:
        if transaction.get('transaction_id') == id_to_delete:
            print(f"Found and deleting transaction: {transaction}")
            found = True
            deleted_count += 1
        else:
            new_transactions.append(transaction) 
    
    if found:
        print(f"Successfully deleted {deleted_count} transaction(s) with ID {id_to_delete}.")
        return new_transactions 
    else:
        print(f"Transaction with ID {id_to_delete} not found.")
        return transactions_list 


def save_transactions(filename=DATA_FILE):

    global transactions
    if not transactions:
        print("No transactions to save.")
        return

    headers = list(transactions[0].keys()) if transactions else []
    if 'transaction_id' in headers:
        headers.insert(0, headers.pop(headers.index('transaction_id'))) 

    required_headers = ['transaction_id', 'date', 'customer_id', 'amount', 'type', 'description']
    for rh in required_headers:
        if rh not in headers:
            headers.append(rh)

    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            for transaction in transactions:
                row_to_write = {header: transaction.get(header, '') for header in headers}
                
                if 'date' in row_to_write and isinstance(row_to_write['date'], datetime):
                    row_to_write['date'] = row_to_write['date'].strftime('%Y-%m-%d')
                
                if 'amount' in row_to_write and isinstance(row_to_write['amount'], (float, int)):
                    row_to_write['amount'] = str(row_to_write['amount'])

                writer.writerow(row_to_write)
        print(f"\nTransactions successfully saved to '{filename}'.")
    except IOError as e:
        print(f"Error saving transactions to '{filename}': {e}")
        _log_error(f"Error saving transactions: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during saving: {e}")
        _log_error(f"Unexpected error during saving: {e}")


# --- Main Application Logic (Example Usage) ---
if __name__ == "__main__":

    load_transactions()

    while True:
        print("\n--- Financial Transaction Manager Menu ---")
        print("1. Load Transactions")
        print("2. Add Transactions")
        print("3. View Transactions")
        print("4. Update Transaction")
        print("5. Delete Transaction")
        print("6. Analyze Finances")
        print("7. Save Transactions")
        print("8. Generate Report")
        print("9. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            load_transactions()
        elif choice == '2':
            add_transactions()
        elif choice == '3':
            view_transactions()
        elif choice == '4':
            update_transactions()
        elif choice == '5':
            transactions = delete_transactions(transactions)
        elif choice == '6':
            print("Feature under construction.")
        elif choice == '7':
            save_transactions()
        elif choice == '8':
            print("Feature under contruction.")
        elif choice == '9':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")