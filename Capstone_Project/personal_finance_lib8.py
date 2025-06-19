import csv 
from datetime import datetime
import os

ERROR_LOG_FILE = 'errors.txt'

def initialize_error_log():
    try:
        with open(ERROR_LOG_FILE, 'w') as f:
            f.write(f"[{datetime.now()}] --- Transaction Processing Log Started ---\n")
        print(f"Log file '{ERROR_LOG_FILE}' has been created/cleared.")
    except IOError as e:
        print(f"Failed to initialize error log file '{ERROR_LOG_FILE}': {e}")

def log_error(message):
    try:
        with open(ERROR_LOG_FILE, 'a') as f:
            f.write(f"[{datetime.now()}] {message}\n")
    except IOError as e:
        print(f"Failed to write to error log file '{ERROR_LOG_FILE}': {e}")

def load_transactions(filename='financial_transactions_short.csv'):
    if not os.path.exists(ERROR_LOG_FILE):
        initialize_error_log()

    loaded_transactions = []
    try:
        with open(filename, 'r', newline='') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                loaded_transactions.append(row)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        log_error(f"Error: The file '{filename}' was not found during loading.")
        return[]
    except Exception as e:
        print(f"An unexpected error occurred while reading '{filename}': {e}")
        log_error(f"An unexpected error occurred while reading '{filename}': {e}")

    processed_transactions = []
    for item in loaded_transactions:
        current_item = item.copy()

        date_str = current_item.get('date', '').strip()
        parsed_date = None
        date_formats = ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y"]
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                break
            except ValueError:
                continue

        if parsed_date:
            current_item['date'] = parsed_date.strftime("%Y-%m-%d")
        else:
            log_error(f"Skipping transaction {current_item.get('transaction_id', 'N/A')}. Invalid date format '{date_str}'.")
            continue

        try:
            amount_str = current_item.get('amount', '').strip()
            if not amount_str:
                new_amount = 0.0
                print(f"Warning: Empty amount found for transaction {current_item.get('transaction_id', 'N/A')}. Setting to 0.0.")
            else:
                new_amount = float(amount_str)

            transaction_type = current_item.get('type', '').lower().strip()
            if transaction_type == "debit":
                current_item['amount'] = new_amount * -1
            elif transaction_type == "credit" or transaction_type == "transfer":
                current_item['amount'] = new_amount
            else:
                log_error(f"Skipping transaction {current_item.get('transaction_id', 'N/A')}. Invalid or empty type '{transaction_type}'.")
                continue

            processed_transactions.append(current_item)
        except ValueError:
            log_error(f"Error: Could not convert amount '{amount_str}' to float in transaction {current_item.get('transaction_id', 'N/A')}.")
            continue
        except Exception as e:
            log_error(f"An unexpected error occurred processing transaction {current_item.get('transaction_id', 'N/A')}: {e}")

    print(f"Successfully loaded and process {len(processed_transactions)} transactions.")
    print(f"Transaction processing complete. Check {ERROR_LOG_FILE} for any logged issues.")
    return processed_transactions

def add_transaction(transactions_list):
    print("\n--- Add new Transaction ---")
    max_id = 0
    if transactions_list:
        max_id = max(int(t.get('transaction_id', 0)) for t in transactions_list if t.get('transaction_id') is not None)

    transaction_id = max_id + 1

    while True:
        date_str = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
    
    customer_id = input("Enter customer ID: ").strip()
    if not customer_id:
        print("Customer ID cannot be empty. Aborting transaction addition.")
        return

    while True:
        amount_str = input("Enter amount: ").strip()
        try:
            amount = float(amount_str)
            break
        except ValueError:
            print("Invalid amount. Please enter a numerical value.")

    while True:
        transaction_type = input("Enter type (credit/debit/transfer): ").strip().lower()
        if transaction_type in ["credit", "debit", "transfer"]:
            break
        else:
            print("Invalid type. Please enter 'credit', 'debit', or 'transfer'.")
    
    if transaction_type == "debit":
        amount = amount * -1

    description = input("Enter description for transaction: ").strip()
    if not description:
        print("Description cannot be empty. Aborting transaction addition.")
        return

    try:
        new_transaction = {
            'transaction_id': str(transaction_id),
            'date': date_str,
            'customer_id': customer_id,
            'amount': amount,
            'type': transaction_type,
            'description': description
        }
        transactions_list.append(new_transaction)
        print(f"\nTransaction added successfully! Details: ")
        for key, value in new_transaction.items():
            print(f"- {key.replace('_', ' ').title()}: {value}")
        print(f"Transaction ID: {new_transaction['transaction_id']}")
    except Exception as e:
        print(f"An unexpected error occurred while adding the transaction: {e}")
        log_error(f"An error occurred while adding a transaction: {e}")

def view_transactions(transactions_list):
    print("\n--- Viewing Transactions ---")
    if not transactions_list:
        print("No transactions to display.")
        return

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

    for transaction in transactions_list:
        row_values = []
        for key, _, width in columns:
            value = transaction.get(key, '')

            if key == 'amount':
                try: 
                    value = f"{float(value):.2f}"
                except (ValueError, TypeError):
                    value = "N/A"
            elif key == 'transaction_id':
                value = str(value)

            str_value = str(value)

            if len(str_value) > width:
                str_value = str_value[:width - 3] + "..."

            row_values.append(f"{str_value:<{width}}")

        print(" | ".join(row_values))

def update_transaction(transactions_list):
    print("\n--- Update Transaction ---")
    if not transactions_list:
        print("No transactions to update. Please load or add transactions first.")
        return

    view_transactions(transactions_list)

    while True:
        try:
            transaction_to_update = int(input("\nEnter the ID of the transaction to update (or 0 to cancel): "))
            if transaction_to_update == 0:
                print("Update cancelled.")
                return
            break
        except ValueError:
            print("Invalid input. Please enter a numerical transaction ID.")

    found_transaction = None
    for transaction in transactions_list:
        if int(transaction.get('transaction_id', 0)) == transaction_to_update:
            found_transaction = transaction
            break
    
    if not found_transaction:
        print(f"Transaction with ID {transaction_to_update} not found.")
        return

    print(f"\nTransaction found. Current details for ID {transaction_to_update}: ")
    print(f"1. Description: {found_transaction.get('description', 'N/A')}")
    print(f"2. Type: {found_transaction.get('type', 'N/A')}")
    print(f"3. Amount: {found_transaction.get('amount', 0):.2f}")

    while True:
        field_choice = input("Enter the number of the field to update (1-3, or 0 to cancel): ").strip()

        if field_choice == 0:
            print("Update cancelled.")
            return
        elif field_choice == '1':
            new_description = input("Enter new description: ").strip()
            found_transaction['description'] = new_description
            print("Description updated successfully.")
            break
        elif field_choice == '2':
            while True:
                new_type = input("Enter new type (credit/debit/transfer): ").strip().lower()
                if new_type in ["credit", "debit", "transfer"]:
                    current_amount = found_transaction.get('amount', 0)
                    current_type = found_transaction.get('type', '').lower()

                    if current_type != new_type:
                        if new_type == "debit" and current_type != "debit":
                            found_transaction['amount'] = abs(current_amount) * -1
                        elif new_type != "debit" and current_type == "debit":
                            found_transaction['amount'] = abs(current_amount)

                    found_transaction['type'] = new_type
                    print("Type updated successfully.")
                    break
                else:
                    print("Invalid type. Please enter 'credit', 'debit', or 'transfer'.")
            break
        elif field_choice == '3':
            while True:
                try:
                    new_amount = float(input("Enter new amount: ").strip())
                    if found_transaction.get('type') == 'debit':
                        found_transaction['amount'] = new_amount * -1
                    else:
                        found_transaction['amount'] = new_amount
                    print("Amount updated successfully.")
                    break
                except ValueError:
                    print("Invalid amount. Please enter a numerical value.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 0 to cancel.")
    print(f"\nUpdated transaction details for ID {transaction_to_update}: ")
    for key, value in found_transaction.items():
        if key == 'amount':
            print(f"- {key.replace('_', ' ').title()}: {value:.2f}")
        else:
            print(f"- {key.replace('_', ' ').title()}: {value}")


def delete_transaction(transactions_list):
    print("\n--- Delete Transaction ---")

    if not transactions_list:
        print("No transactions to delete. Please load or add transactions first.")
        return

    view_transactions(transactions_list)

    while True:
        try:
            transaction_to_delete = int(input("\nEnter the ID of the transaction to delete. (or 0 to cancel)"))

            if transaction_to_delete == 0:
                print("Deletion canceled.")
                return

            found_index = -1
            for i, transaction in enumerate(transactions_list):
                if int(transaction.get('transaction_id', 0)) == transaction_to_delete:
                    found_index = i
                    break
            
            if found_index != -1:
                transaction_details = transactions_list[found_index]
                print(f"\nFound transaction with ID {transaction_to_delete}: ")
                print(f"Date: {transaction_details.get('date', 'N/A')}, Customer: {transaction_details.get('customer_id', 'N/A')}, Amount: {transaction_details.get('amount', 0):.2f}, Type: {transaction_details.get('type', 'N/A')}")

                confirm = input("Are you sure you want to delete this transaction? (yes/no)").strip().lower()

                if confirm == 'yes':
                    del transactions_list[found_index]
                    print(f"Transaction with ID {transaction_to_delete} deleted successfully.")

                else:
                    print("Deletion aborted by user.")
                    break
            else:
                print(f"Transaction with ID {transaction_to_delete} not found.")
                continue

        except ValueError:
            print("Invalid input. Please enter a numerical transaction ID.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            log_error(f"An unexpected error occurred during deletion: {e}")
            break

def analyze_transactions(transactions_list):
    print("\n--- Financial Summary ---")
    if not transactions_list:
        print("No transactions to analyze. Please load or add transactions first.")
        return
    
    total_credits = 0.0
    total_debits = 0.0
    total_transfers = 0.0
    net_balance = 0.0
    totals_by_type = {}

    for transaction in transactions_list:
        try:
            amount = float(transaction.get('amount', 0))
            transaction_type = transaction.get('type', 'unknown').lower()

            if transaction_type == 'credit':
                total_credits += amount
            elif transaction_type == 'debit':
                total_debits += amount
            elif transaction_type == 'transfer':
                total_transfers += amount

            net_balance += amount

            if transaction_type in totals_by_type:
                totals_by_type[transaction_type] += amount
            else:
                totals_by_type[transaction_type] = amount
        except (ValueError, TypeError) as e:
            log_error(f"Error processing amount for financial analysis: {transaction.get('transaction_id', 'N/A')}. Error: {e}")
            print(f"Warning: Skipping a transaction due to invalid amount for analysis (ID: {transaction.get('transaction_id', 'N/A')}).")
            continue

    print(f"Total Credits: ${total_credits:.2f}")
    print(f"Total Debits: ${total_debits:.2f}")
    print(f"Total Transfers: ${total_transfers:.2f}")
    print(f"Net Balance: ${net_balance:.2f}")

    print("\nTotals by Type:")
    if totals_by_type:
        for transaction_type, total_amount in totals_by_type.items():
            print(f"- {transaction_type.replace('_', ' ').title()}: ${total_amount:.2f}")
    else:
        print("No categorized transactions.")

def save_transactions(transactions_list, filename='financial_transactions_short.csv'):
    header = ['transaction_id', 'date', 'customer_id', 'amount', 'type', 'description']

    existing_transactions = []
    existing_transaction_identifiers = set()

    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        try:
            with open(filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.Reader(file)
                if not all(field in reader.fieldnames for field in header):
                    log_error(f"Warning: CSV header in '{filename}' does not fully match expected header. Data may not be read correctly.")

                    for row in reader:
                        try:
                            if 'amount' in row:
                                row['amount'] = float(row['amount'])
                        except (ValueError, KeyError) as e:
                            log_error(f"Error converting amount for row{row.get('transaction_id', 'N/A')} from '{filename}': {e}. Amount might be missing or invalid.")

                        existing_transactions.append(row)

                        identifier = row.get('transaction_id')
                        if identifier:
                            existing_transaction_identifiers.add(identifier)

        except FileNotFoundError:
            log_error(f"Error: File '{filename}' not found during read operation in save_transactions.")
            existing_transactions = []
            existing_transaction_identifiers = set()
        except Exception as e:
            log_error(f"An unexpected error occurred while reading existing transactions from '{filename}': {e}.")
            existing_transactions = []
            existing_transaction_identifiers = set()

    new_transactions_to_add = []
    for transaction in transactions_list:
        transaction_id = transaction.get('transaction_id')

        if transaction_id and transaction_id not in existing_transaction_identifiers:
            new_transactions_to_add.append(transaction)
            existing_transaction_identifiers.add(transaction_id)
        elif not transaction_id:
            log_error(f"Warning: Transaction missing 'transaction_id'. Skipping: {transaction}")
    
    all_unique_transactions = []

    for trans in existing_transactions:
        if 'amount' in trans:
            try:
                trans['amount'] = float(trans['amount'])
            except (ValueError, TypeError):
                log_error(f"Error: Amount for transaction ID {trans.get('transaction_id', 'N/A')} is not a valid number before saving. Saving as is.")

        all_unique_transactions.append(trans)

    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            writer.writerows(all_unique_transactions)
        print(f"Transactions successfully saved to '{filename}'. {len(new_transactions_to_add)} new transactions added.")
    except Exception as e:
        log_error(f"Error writing transactions to '{filename}': {e}")
        print(f"Error writing transactions to '{filename}': {e}")
    

def main():
    transactions_data = []
    initialize_error_log()

    while True:
        print("\n--- Smart Personal Finance Analyzer ---")
        print("1. Load Transactions")
        print("2. Add Transactions")
        print("3. View Transactions")
        print("4. Update Transactions")
        print("5. Delete Transactions")
        print("6. Analyze Transactions")
        print("7. Save Transactions")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ").strip()
        if choice == '1':
            transactions_data = load_transactions()
        elif choice == '2':
            if not transactions_data:
                print("Please load transactions first (option 1) before adding new ones.")
            else:
                add_transaction(transactions_data)
        elif choice == '3':
            view_transactions(transactions_data)
        elif choice == '4':
            update_transaction(transactions_data)
        elif choice == '5':
            delete_transaction(transactions_data)
        elif choice == '6':
            analyze_transactions(transactions_data)
        elif choice == '7':
            save_transactions(transactions_data)
            print("Current transactions saved to file.")
        elif choice == '9':
            print("Exiting Smart Personal Finance Analyzer. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 9.")

