"""AuditMixin for logging monetary and resource actions."""
from datetime import datetime
from typing import List, Dict


class AuditMixin:
    """Mixin class that logs every monetary or resource action with timestamps."""

    def __init__(self):
        """Initialize audit log."""
        self._audit_log: List[Dict[str, str]] = []

    def log_action(self, action: str, details: str) -> None:
        """Log an action with timestamp.
        
        Args:
            action: Type of action (e.g., 'withdrawal', 'resource_borrow').
            details: Description of the action.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'action': action,
            'details': details
        }
        self._audit_log.append(log_entry)

    def get_audit_log(self) -> List[Dict[str, str]]:
        """Get all logged actions.
        
        Returns:
            List of audit log entries.
        """
        return self._audit_log.copy()

    def print_audit_log(self) -> None:
        """Print all logged actions."""
        if not self._audit_log:
            print("No audit log entries.")
            return
        print("\n=== Audit Log ===")
        for entry in self._audit_log:
            print(f"[{entry['timestamp']}] {entry['action']}: {entry['details']}")
        print("================\n")
