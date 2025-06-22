### Smart Personal Finance Analyzer

This Python program is a command-line tool designed to help you manage and analyze financial transactions. It allows you to load transaction data from a CSV file, add new transactions, view, update, and delete existing transactions, analyze financial data, save new transactions, and generate a detailed report in text format.

### Features

Load Transactions - imports data from a CSV file. It also converts debit amounts to negative values. RUN THIS OPTION FIRST!
Add Transactions - Manually add new financial transactions with automation ID generation.
View Transactions - Display all loaded transactions in a formatted, easy-to-read table.
Update Transactions - Modify the description, type, or amount of existing transactions.
Delete Transactions - Remove transactions from the list according to ID.
Analyze Transactions - Generate a summary of financial activity, including total credits, debits, transfers, and net balance.
Save Transactions - Export current list of transactions back to a CSV file.
Generate Report - Create a text file containing the detailed financial summary.
Error Logging - Automatically logs processing errors and warnings to error.txt for easier debugging and data integrity checks.

### How to Run

1. Save the code: Save the provided Python code as a .py file (e.g. financial_analyzer.py)
2. Prepare your CSV file: Headers should include transaction_id, date, customer_id, amount, type, description. You may also save the included sample file "financial_transactions_short.csv"
3. Run the script: Import the Python library in a Jupiter notebook and call the function or open a terminal to run python financial_analyzer.py

### Usage

Upon running the script, you will be presented with a menu including 9 options. Begin with Option 1 to load transactions.

### Credits

This program was created with help from CODE:YOU mentors and Google Gemini.