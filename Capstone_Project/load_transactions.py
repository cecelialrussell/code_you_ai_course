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