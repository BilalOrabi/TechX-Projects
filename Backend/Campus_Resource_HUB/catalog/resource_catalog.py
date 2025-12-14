"""ResourceCatalog collection for managing resources."""
from typing import Iterator, Optional, List, Protocol


class Allocatable(Protocol):
    """Protocol for objects that can receive resource allocations (duck typing)."""
    
    id: str
    
    def needs_resource(self) -> bool:
        """Check if this object needs a resource."""
        ...


class ResourceCatalog:
    """Collection of resources with allocation capabilities."""

    def __init__(self):
        """Initialize an empty resource catalog."""
        self._resources: List = []

    def add_resource(self, resource) -> None:
        """Add a resource to the catalog.
        
        Args:
            resource: A Resource object to add.
        """
        if resource not in self._resources:
            self._resources.append(resource)

    def remove_resource(self, resource_id: str) -> bool:
        """Remove a resource from the catalog.
        
        Args:
            resource_id: ID of the resource to remove.
            
        Returns:
            True if removed, False if not found.
        """
        for i, resource in enumerate(self._resources):
            if resource.resource_id == resource_id:
                self._resources.pop(i)
                return True
        return False

    def get_resource(self, resource_id: str):
        """Get a resource by ID.
        
        Args:
            resource_id: ID of the resource.
            
        Returns:
            The resource or None if not found.
        """
        for resource in self._resources:
            if resource.resource_id == resource_id:
                return resource
        return None

    def get_available_resources(self) -> List:
        """Get all available resources.
        
        Returns:
            List of available resources.
        """
        return [r for r in self._resources if r.is_available()]

    def allocate(self, requestor) -> bool:
        """Allocate a resource to an object using duck typing.
        
        The requestor must have 'id' and 'needs_resource()' attributes.
        
        Args:
            requestor: An object needing a resource.
            
        Returns:
            True if allocation successful, False otherwise.
        """
        # Duck typing: check for required attributes
        if not hasattr(requestor, 'id') or not hasattr(requestor, 'needs_resource'):
            raise TypeError("Requestor must have 'id' and 'needs_resource()' attributes.")
        
        if not requestor.needs_resource():
            return False
        
        # Find first available resource
        available = self.get_available_resources()
        if available:
            resource = available[0]
            return resource.borrow(requestor.id)
        
        return False

    def __len__(self) -> int:
        """Return the number of resources in the catalog."""
        return len(self._resources)

    def __iter__(self) -> Iterator:
        """Iterate over all resources in the catalog."""
        return iter(self._resources)

    def __repr__(self) -> str:
        """Return catalog representation."""
        return f"ResourceCatalog({len(self._resources)} items)"

    def __str__(self) -> str:
        """Return human-readable catalog description."""
        if not self._resources:
            return "Catalog (empty)"
        items_str = ", ".join(str(r) for r in self._resources)
        return f"Catalog ({len(self._resources)} items): {items_str}"
