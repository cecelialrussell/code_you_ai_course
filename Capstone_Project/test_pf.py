# test_pf.py
import personal_finance

print(dir(personal_finance)) # This will show all attributes of the module

try:
    personal_finance.add_transaction()
    print("add_transaction called successfully!")
except AttributeError:
    print("Still getting AttributeError in test_pf.py :(")