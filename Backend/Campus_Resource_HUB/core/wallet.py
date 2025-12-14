"""Wallet module for managing personal finances."""
from typing import Optional


class Wallet:
    """Manages financial transactions for a person."""

    def __init__(self, initial_balance: float):
        """Initialize a wallet with an initial balance.
        
        Args:
            initial_balance: Starting balance in credits (must be non-negative).
            
        Raises:
            ValueError: If balance is negative.
        """
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        self._balance = initial_balance

    @property
    def balance(self) -> float:
        """Get the current wallet balance."""
        return self._balance

    def deposit(self, amount: float) -> None:
        """Add credits to the wallet.
        
        Args:
            amount: Amount to deposit (must be positive).
            
        Raises:
            ValueError: If amount is not positive.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        """Remove credits from the wallet.
        
        Args:
            amount: Amount to withdraw (must be positive and <= balance).
            
        Raises:
            ValueError: If amount is invalid or exceeds balance.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise ValueError(f"Insufficient funds. Balance: {self._balance}, Requested: {amount}")
        self._balance -= amount

    def transfer(self, recipient_wallet: 'Wallet', amount: float) -> None:
        """Transfer credits to another wallet.
        
        Args:
            recipient_wallet: The destination wallet.
            amount: Amount to transfer (must be positive and <= balance).
            
        Raises:
            ValueError: If amount is invalid or exceeds balance.
        """
        self.withdraw(amount)
        recipient_wallet.deposit(amount)

    def __repr__(self) -> str:
        """Return wallet representation."""
        return f"Wallet(balance={self._balance:.2f})"
