from datetime import datetime

class AuditMixin:
    def log(self, message: str) -> None:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[AUDIT {time}] {message}")


class Wallet(AuditMixin):
    def __init__(self, owner):
        self.owner = owner
        self._balance = 0.0

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount
        self.log(f"{self.owner.name} deposited {amount:.2f}")

    def withdraw(self, amount: float) -> None:
        if amount <= 0 or amount > self._balance:
            raise ValueError("Invalid withdrawal")
        self._balance -= amount
        self.log(f"{self.owner.name} withdrew {amount:.2f}")

    def transfer(self, other, amount: float) -> None:
        self.withdraw(amount)
        other.deposit(amount)
        self.log(f"Transfer {amount:.2f} to {other.owner.name}")
