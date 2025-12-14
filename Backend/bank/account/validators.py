from account.exceptions import InvalidAmountError

def validate_amount(amount):
	if not isinstance(amount, (int, float)):
		raise InvalidAmountError("Amount must be numeric.")
	if amount < 0:
		raise InvalidAmountError("Amount must be >= 0")