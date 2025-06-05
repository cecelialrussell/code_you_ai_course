import csv
from datetime import datetime

transactions = []
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

def add_transactions(transactions):

    processed_transaction = transaction_data.copy()

    date_str = processed_transaction.get('date', '').strip()
    parsed_date = None
    date_formats = ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%Y/%m/%d"]

    if date_str:
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                break
            except ValueError:
                continue
        if parsed_date: 
            processed_transaction['date'] = parsed_date
        else:
            _log_error(f"Error: Could not add transaction. Invalid date format '{date_str}' for transactions {processed_transaction.get('transaction_id', 'N/A')}.")
            print(f"Error: Could not add transaction. Invalid date format '{date_str}'.")
    else:
        _log_error(f"Error: Could not add transaction. 'date' field is missing or empty for transaction {processed_transaction.get('transaction_id', 'N/A')}.")
        print(f"Error: Could not add transaction. 'date' field is missing or empty.")
        return False
    
    try:
        amount_str = str(processed_transaction.get('amount', '')).strip()
        new_amount = 0.0
        if not amount_str:
            _log_error(f"Warning: Empty amount provided for new transaction {processed_transaction.get('transaction_id', 'N/A')}. Setting to 0.0.")
            print(f"Warning: Empty amount provided. Setting to 0.0.")
        else:
            new_amount = float(amount_str)
        
        transaction_type = str(processed_transaction.get('type', '')).strip().lower()
        if transaction_type == 'debit':
            processed_transaction['amount'] = new_amount * -1
        elif transaction_type == 'credit':
            processed_transaction['amount'] = new_amount
        else:
            processed_transaction['amount'] = new_amount
            if transaction_type:
                _log_error(f"Warning: Unrecognizable type '{transaction_type}' for new transaction {processed_transaction.get('transactions_id', 'N/A')}. Amount stored as is.")
                print(f"Warning: Unrecognizable type '{transaction_type}'. Amount stored as is.")
    except (ValueError, TypeError):
        _log_error(f"Error: Could not add transaction. Invalid amount '{processed_transaction.get('amount', '')} for transaction {processed_transaction.get('transaction_id', 'N/A')}.'")
        print(f"Error: Could not add transaction. Invalid amount '{processed_transaction.get('amount', '')}'.")
        return False
    
    if 'transaction_id' not in processed_transaction or not processed_transaction['transaction_id']:
        processed_transaction['transaction_id'] = f"MANUAL_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        print(f"Note: No 'transaction_id' provided. Generated one: {processed_transaction['transaction_id']}")
    
    transactions.append(processed_transaction)
    print(f"Transaction successfully added. Current total transactions: {len(transactions)}")
    return True

