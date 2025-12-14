# bank/demo.py

from account.bank_account import BankAccount

# Create account using constructor
acc1 = BankAccount("bilal", 500, "1234")

# Create account using class method
acc2 = BankAccount.from_string("ahmad,1000,4321")

# Deposits and withdrawals
acc1.deposit(200)
acc1.withdraw(100, "1234")

acc2.deposit(500)
acc2.withdraw(300, "4321")

# Show balances
print(acc1.show_balance("1234"))
print(acc2.show_balance("4321"))

# Show transactions
print(acc1.show_transactions())
print(acc2.show_transactions())

# Demonstrate encapsulation (these should fail)
try:
    print(acc1.__transaction_history)
except AttributeError:
    print("transaction_history is private")

try:
    print(acc1.__pin_code)
except AttributeError:
    print("pin_code is private")

# Use static method
BankAccount.validate_amount(100)
print("Amount validation passed")
