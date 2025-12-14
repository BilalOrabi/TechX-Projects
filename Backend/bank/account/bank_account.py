from account.exceptions import InvalidPinError
from account.validators import validate_amount

class BankAccount:
	def __init__(self, account_holder, balance, pin_code):
		self.account_holder = account_holder

		validate_amount(balance)
		self._balance = balance

		self.__transaction_history = []
		self.__pin_code = pin_code

	def deposit(self, amount):
		validate_amount(amount)
		self._balance += amount
		self.__transaction_history.append(f"Deposited: {amount}")

	def withdraw(self, amount, pin):
		if pin != self.__pin_code:
			raise InvalidPinError("Invalid PIN.")
		
		validate_amount(amount)

		if amount > self._balance:
			raise ValueError("Insufficient funds.")
		
		self._balance -= amount
		self.__transaction_history.append(f"Withdrew: {amount}")

		def show_balance(self, pin):
			if pin != self.__pin_code:
				raise InvalidPinError("Invalid PIN.")
		return self._balance

	def show_transactions(self):
		return self.__transaction_history.copy()
	
	@classmethod
	def from_string(cls, data_str):
		name, balance, pin = data_str.split(",")
		return cls(name.strip(), float(balance.strip()), pin.strip())

	@staticmethod
	def validate_amount(amount):
		validate_amount(amount)