import csv
from datetime import datetime

transactions = []
ERROR_LOG_FILE = 'errors.txt' # Define this if not already defined

def _log_error(message):
    with open(ERROR_LOG_FILE, 'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def load_transactions(filename='financial_transactions_short.csv'):
    global transactions # Indicate that we're modifying the global variable

    try:
        with open(filename, 'r', newline='') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                processed_row = row.copy()

                # --- Date Parsing ---
                date_str = processed_row.get('date', '').strip()
                parsed_date = None
                date_formats = ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y"] # Add more formats as needed

                if date_str:
                    for fmt in date_formats:
                        try:
                            parsed_date = datetime.strptime(date_str, fmt)
                            break
                        except ValueError:
                            continue
                    if parsed_date:
                        processed_row['date'] = parsed_date.strftime("%Y-%m-%d") # Store as string
                        # Or, to store as datetime object: processed_row['date'] = parsed_date
                    else:
                        _log_error(f"Error: Skipping transaction {processed_row.get('transaction_id', 'N/A')}. Invalid date format '{date_str}'.")
                        processed_row['date'] = None # Indicate invalid date
                else:
                    processed_row['date'] = None # No date provided

                # --- Amount Parsing ---
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
                    elif transaction_type == "credit":
                        processed_row['amount'] = new_amount
                    else:
                        processed_row['amount'] = new_amount
                        if transaction_type: # Only log if there was a type string that wasn't debit/credit
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

# To test the function (if you have a CSV file named 'financial_transactions_short.csv' in the same directory)
# load_transactions()
# print(transactions[:5]) # Print first 5 transactions to see the result