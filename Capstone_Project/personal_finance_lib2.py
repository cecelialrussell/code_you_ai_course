import csv
from datetime import datetime

transactions = [] # Global variable, defined once at the module level
ERROR_LOG_FILE = 'errors.txt' # Global for error logging


def _initialize_error_log():
    """Helper to initialize/clear the error log."""
    try:
        with open(ERROR_LOG_FILE, 'w') as f:
            f.write(f"[{datetime.now()}] --- Transaction Processing Log Started ---\n")
        print(f"Log file '{ERROR_LOG_FILE}' has been created/cleared.")
    except IOError as e:
        print(f"Failed to initialize error log file '{ERROR_LOG_FILE}': {e}")

def _log_error(message):
    """Helper to log an error message."""
    try:
        with open(ERROR_LOG_FILE, 'a') as f:
            f.write(f"[{datetime.now()}] {message}\n")
    except IOError as e:
        print(f"Failed to write to error log file '{ERROR_LOG_FILE}': {e}")

def load_transactions(filename='financial_transactions_short.csv'):
    global transactions # Declare intent to modify the global list
    _initialize_error_log()

    transactions.clear() # <--- CRITICAL: Clear the list before loading new data [cite: 1]

    try:
        with open(filename, 'r', newline='') as file: 
            csv_reader = csv.DictReader(file) 
            for row in csv_reader:
                processed_row = row.copy()

                # --- Date Parsing (your existing logic) ---
                date_str = processed_row.get('date', '').strip() 
                parsed_date = None
                if date_str:
                    try:
                        parsed_date = datetime.strptime(date_str, "%Y-%m-%d") 
                    except ValueError:
                        try:
                            parsed_date = datetime.strptime(date_str, "%d-%m-%Y") 
                        except ValueError:
                            try:
                                parsed_date = datetime.strptime(date_str, "%m/%d/%Y") 
                            except ValueError:
                                _log_error(f"Error: Skipping transaction {processed_row.get('transaction_id', 'N/A')}. Invalid date format '{date_str}'.") 

                if parsed_date:
                    # Store as YYYY-MM-DD string for consistency, or keep as datetime object
                    processed_row['date'] = parsed_date.strftime("%Y-%m-%d")
                else:
                    processed_row['date'] = None # Or a default invalid string

                # --- Amount Parsing (your existing logic) ---
                try:
                    amount_str = processed_row['amount']
                    if not amount_str:
                        new_amount = 0.0 
                        print(f"Warning: Empty amount found for transaction {processed_row.get('transaction_id', 'N/A')}. Setting to 0.0")
                        _log_error(f"Warning: Empty amount found for transaction {processed_row.get('transaction_id', 'N/A')}. Set to 0.0.")
                    else:
                        new_amount = float(amount_str)

                    transaction_type = processed_row.get('type', '').strip().lower()
                    if transaction_type == "debit": 
                        processed_row['amount'] = new_amount * -1 
                    elif transaction_type == "credit": 
                        processed_row['amount'] = new_amount
                    else:
                        processed_row['amount'] = new_amount
                        if transaction_type:
                             _log_error(f"Warning: Unrecognized type '{transaction_type}' for transaction {processed_row.get('transaction_id', 'N/A')}. Amount stored as is.")
                except (ValueError, TypeError): 
                    _log_error(f"Error: Could not convert amount to float in transaction {processed_row.get('transaction_id', 'N/A')}. Invalid amount '{processed_row.get('amount', '')}'.")
                    processed_row['amount'] = 0.0 # Default if conversion fails

                transactions.append(processed_row)

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        _log_error(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred during file loading: {e}")
        _log_error(f"An unexpected error occurred during file loading: {e}")

    print(f"There are {len(transactions)} transactions.") 
    print(f"Transaction processing complete. Check {ERROR_LOG_FILE} for any logged issues.")

    # No return needed as it modifies the global 'transactions'

# Helper function to save current state of transactions to CSV
def save_transactions(filename='financial_transactions_short.csv'):
    global transactions # Access the global list

    if not transactions:
        print("No transactions to save.")
        return

    # Determine fieldnames from the first transaction's keys
    # This assumes all transactions have the same keys, which is generally a good practice
    fieldnames = []
    if transactions:
        fieldnames = list(transactions[0].keys())
    else:
        # Fallback fieldnames if transactions list is empty (shouldn't happen if this is called when not empty)
        fieldnames = ['transaction_id', 'date', 'customer_id', 'amount', 'type', 'description']

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()
            for t in transactions:
                # Prepare data for CSV writing
                # Create a copy to avoid modifying the original dict during iteration
                write_t = t.copy()
                # Ensure date is string format for CSV
                if isinstance(write_t.get('date'), datetime.date):
                    write_t['date'] = write_t['date'].strftime('%Y-%m-%d')
                # Ensure amount is string or formatted float for CSV
                if isinstance(write_t.get('amount'), (float, int)):
                    write_t['amount'] = f"{write_t['amount']:.2f}"
                csv_writer.writerow(write_t)
        print(f"Transactions saved to {filename}.")
    except IOError as e:
        _log_error(f"Error writing to file '{filename}': {e}")
        print(f"Error writing to file '{filename}': {e}")
    except Exception as e:
        _log_error(f"An unexpected error occurred during file write: {e}")
        print(f"An unexpected error occurred during file write: {e}")


def add_transactions(transactions): # Removed filename param if not used for loading
    
    # Find max ID from current in-memory transactions
    max_id = 0
    if transactions:
        try:
            # Ensure 'transaction_id' is present and can be converted to int
            max_id = max(int(t.get('transaction_id', 0)) for t in transactions if t.get('transaction_id') is not None)
        except ValueError:
            _log_error("Warning: Could not determine max transaction ID due to non-integer IDs. Starting new IDs from 1000.")
            max_id = 999 # Fallback if IDs are not clean numbers

    print("--- Add New Transaction ---")

    transaction_id = max_id + 1

    while True:
        date_str = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    customer_id = input("Enter customer ID: ").strip()

    while True:
        amount_str = input("Enter amount: ").strip()
        try:
            amount = float(amount_str)
            break
        except ValueError:
            print("Invalid amount. Please enter numerical value.")

    transaction_type = input("Enter type (credit/debit/transfer): ").strip().lower()
    if not transaction_type: 
        print("Transaction type cannot be empty. Aborting...")
        _log_error(f"Transaction add aborted: type was empty for ID {transaction_id}.")
        return

    description = input("Enter description for transaction: ").strip()

    new_transaction = {
        'transaction_id': str(transaction_id), # Store as string to match CSV behavior
        'date': date_str,
        'customer_id': customer_id,
        'amount': amount,
        'type': transaction_type,
        'description': description
    }
    transactions.append(new_transaction)

    print("Transaction added!")
    print(f"ID: {new_transaction['transaction_id']}")
    print(f"Date: {new_transaction['date']}")
    print(f"Customer ID: {new_transaction['customer_id']}")
    print(f"Amount: {new_transaction['amount']:.2f}")
    print(f"Type: {new_transaction['type']}")

    save_transactions() # Save changes after adding

# ... (view_transactions, update_transactions, delete_transactions)
# Make sure view_transactions DOES NOT load from file again, just displays global 'transactions'
# Make sure update_transactions DOES NOT load from file again, just modifies global 'transactions' and then calls save_transactions()
# Make sure delete_transactions DOES NOT load from file again, just modifies global 'transactions' and then calls save_transactions()

def view_transactions(transactions):
    # No global transactions needed as it only reads
    # REMOVE ALL FILE READING LOGIC FROM HERE
    if not transactions:
        print("No transactions to display.")
        return

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
    
    if not transactions: 
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

    selected_transaction_index = -1
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
            _log_error(f"Update failed for ID {selected_transaction.get('transaction_id', 'N/A')}: Invalid amount '{new_value}'.")
            return 

    selected_transaction[field_to_change] = new_value
    print("Transaction updated!")

    save_transactions() # <--- Call save_transactions after modification


def delete_transactions(transactions): # Removed filename param if not used for loading
    
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

    selected_transaction_index = -1
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
        print("Transaction deleted successfully!")
        save_transactions() # <--- Call save_transactions after modification
    else:
        print("Transaction deletion cancelled.")

# Placeholder for other functions you might add
def analyze_finances():
    print("Financial analysis feature coming soon!")

def generate_report():
    print("Report generation feature coming soon!")