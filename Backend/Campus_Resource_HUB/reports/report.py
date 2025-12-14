"""Report utility for generating campus hub summaries."""
from typing import List, Optional


class Report:
    """Utility class for generating campus hub reports."""

    def __init__(self, students: int = 0, premium_students: int = 0, 
                 mentor_approvals: int = 0, catalog_size: int = 0):
        """Initialize a report.
        
        Args:
            students: Total number of students.
            premium_students: Total number of premium students.
            mentor_approvals: Total mentor approvals.
            catalog_size: Total resources in catalog.
        """
        self.students = students
        self.premium_students = premium_students
        self.mentor_approvals = mentor_approvals
        self.catalog_size = catalog_size

    @classmethod
    def from_students(cls, student_list: List, mentor_approval_count: int = 0, 
                      catalog_size: int = 0) -> 'Report':
        """Factory method to create a report from a list of students.
        
        Args:
            student_list: List of student objects.
            mentor_approval_count: Total approvals by mentors.
            catalog_size: Size of resource catalog.
            
        Returns:
            A Report instance.
        """
        from .core import PremiumStudent
        
        total_students = len(student_list)
        premium_count = sum(1 for s in student_list if isinstance(s, PremiumStudent))
        
        return cls(
            students=total_students,
            premium_students=premium_count,
            mentor_approvals=mentor_approval_count,
            catalog_size=catalog_size
        )

    @staticmethod
    def format_currency(amount: float) -> str:
        """Format a currency amount.
        
        Args:
            amount: Amount in credits.
            
        Returns:
            Formatted currency string.
        """
        return f"{amount:.2f}"

    @staticmethod
    def format_list(items: List[str]) -> str:
        """Format a list of items.
        
        Args:
            items: List of item strings.
            
        Returns:
            Comma-separated formatted string.
        """
        return ", ".join(items) if items else "None"

    def __str__(self) -> str:
        """Return human-readable report summary."""
        return (f"REPORT: students={self.students} | premium={self.premium_students} | "
                f"mentor_approvals={self.mentor_approvals} | catalog_size={self.catalog_size}")

    def __repr__(self) -> str:
        """Return report representation."""
        return (f"Report(students={self.students}, premium={self.premium_students}, "
                f"approvals={self.mentor_approvals}, catalog_size={self.catalog_size})")

    def __add__(self, other: 'Report') -> 'Report':
        """Combine two reports by summing their values.
        
        Args:
            other: Another Report instance.
            
        Returns:
            A new Report with combined values.
        """
        if not isinstance(other, Report):
            raise TypeError("Can only add Report instances together.")
        
        return Report(
            students=self.students + other.students,
            premium_students=self.premium_students + other.premium_students,
            mentor_approvals=self.mentor_approvals + other.mentor_approvals,
            catalog_size=self.catalog_size + other.catalog_size
        )

    def __eq__(self, other: object) -> bool:
        """Check if two reports have the same values."""
        if not isinstance(other, Report):
            return False
        return (self.students == other.students and 
                self.premium_students == other.premium_students and
                self.mentor_approvals == other.mentor_approvals and
                self.catalog_size == other.catalog_size)
