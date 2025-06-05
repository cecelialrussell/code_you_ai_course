import csv
from datetime import datetime

transactions = []
max_id = 0
ERROR_LOG_FILE = 'errors.txt'

def _log_error(message):
    with open(ERROR_LOG_FILE, 'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def load_transactions(filename='financial_transactions_short.csv'):
    global transactions
    
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
                        _log_error(f"Error: Skipping transaction {processed_row.get('transaction_id', 'N/A')}. Invalid date format '{date_str}.")
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
                            processed_row['amount'] - new_amount
                            if transaction_type:
                                _log_error(f"Warning: Unrecognizable type '{transaction_type} for transaction {processed_row.get('transaction_id', 'N/A')}. Amount stored as is.")
                    except (ValueError, TypeError):
                        _log_error(f"Error: Could not convert amount to float in transaction {processed_row.get('transaction_id', 'N/A')}. Invalid amount '{processed_row.get('amount', '')}'.")
                        processed_row['amount'] = 0.0

                    transactions.append(processed_row)

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        _log_error(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred during file loading: {e}")
        _log_error(f"An unexpected error occurred during file loading: {e}")
    
    print(f"There are {len(transactions)} transactions.")
    print(f"Transaction processing complete. Check {ERROR_LOG_FILE} for any logged issues.")

    import csv
from datetime import datetime

def add_transactions(transactions):
    load_transactions()
    global max_id
    for transaction in transactions:
        if 'transaction_id' in transaction:
            try:
                current_id = int(transaction['transaction_id'])
                if current_id > max_id:
                    max_id = current_id
            except (ValueError, TypeError):
                print(f"Warning: transaction_id '{transaction['transaction_id']}' is not a valid number. Skipping.")
        else:
            print("Warning: 'transaction_id' key not found in transaction.")
   
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
        print(transactions[-1])
    except IOError as e:
        print(f"Unable to add transaction.")

def view_transactions(transactions):
    if not transactions:
        print(f"No transactions to display. Load or add some transactions.")
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


def delete_transactions(transactions):
    print("\n--- Delete Transaction ---")
    if not transactions:
        print("No transactions to delete. The list is empty.")
        return
    view_transactions()
    try:
        id_to_delete = int(input("Enter the ID of the transaction to delete: "))
    except ValueError:
        print("Invalid input. Please enter a numerical transaction ID.")
        return
    
    found = False

    new_transactions = []
    deleted_count = 0

    for transaction in transactions:
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
        print(f"Transactions with ID {id_to_delete} not found.")
        return transactions