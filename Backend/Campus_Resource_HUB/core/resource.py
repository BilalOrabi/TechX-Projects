"""Resource module for managing borrowable resources."""
from enum import Enum
from typing import Optional


class ResourceStatus(Enum):
    """Enum for resource status."""
    AVAILABLE = "available"
    BORROWED = "borrowed"
    MAINTENANCE = "maintenance"


class Resource:
    """Represents a borrowable resource in the campus."""

    def __init__(self, resource_id: str, name: str, resource_type: str, status: ResourceStatus = ResourceStatus.AVAILABLE):
        """Initialize a resource.
        
        Args:
            resource_id: Unique resource identifier (non-empty).
            name: Resource name (non-empty).
            resource_type: Type of resource (e.g., 'Lab', 'Equipment').
            status: Current status (defaults to AVAILABLE).
            
        Raises:
            ValueError: If any parameter is invalid.
        """
        if not resource_id or not isinstance(resource_id, str):
            raise ValueError("Resource ID must be a non-empty string.")
        if not name or not isinstance(name, str):
            raise ValueError("Resource name must be a non-empty string.")
        if not resource_type or not isinstance(resource_type, str):
            raise ValueError("Resource type must be a non-empty string.")

        self.resource_id = resource_id
        self.name = name
        self.resource_type = resource_type
        self.status = status
        self.borrowed_by: Optional[str] = None  # Student ID

    def is_available(self) -> bool:
        """Check if resource is available for borrowing."""
        return self.status == ResourceStatus.AVAILABLE

    def borrow(self, student_id: str) -> bool:
        """Attempt to borrow the resource.
        
        Args:
            student_id: ID of the student borrowing.
            
        Returns:
            True if successful, False if not available.
        """
        if not self.is_available():
            return False
        self.status = ResourceStatus.BORROWED
        self.borrowed_by = student_id
        return True

    def return_resource(self) -> None:
        """Return the borrowed resource."""
        self.status = ResourceStatus.AVAILABLE
        self.borrowed_by = None

    def __repr__(self) -> str:
        """Return resource representation."""
        return f"Resource(id={self.resource_id}, type='{self.resource_type}', status='{self.status.value}')"

    def __str__(self) -> str:
        """Return human-readable resource description."""
        return f"{self.name} ({self.resource_type}, {self.status.value})"

    def __eq__(self, other: object) -> bool:
        """Compare resources by ID."""
        if not isinstance(other, Resource):
            return False
        return self.resource_id == other.resource_id
