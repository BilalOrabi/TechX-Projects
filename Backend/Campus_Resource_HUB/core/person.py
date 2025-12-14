"""Person module containing abstract Person class and subclasses."""
from abc import ABC, abstractmethod
from typing import Optional, List
from .wallet import Wallet


class Person(ABC):
    """Abstract base class for all people in the campus hub."""

    _total_people = 0

    def __init__(self, person_id: str, name: str, email: str, initial_balance: float):
        """Initialize a person.
        
        Args:
            person_id: Unique identifier (non-empty string).
            name: Person's name (non-empty string).
            email: Person's email (non-empty string).
            initial_balance: Starting wallet balance (non-negative).
            
        Raises:
            ValueError: If any parameter is invalid.
        """
        if not person_id or not isinstance(person_id, str):
            raise ValueError("Person ID must be a non-empty string.")
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string.")
        if not email or not isinstance(email, str):
            raise ValueError("Email must be a non-empty string.")

        self.person_id = person_id
        self.name = name
        self.email = email
        self.wallet = Wallet(initial_balance)
        Person._total_people += 1

    def __eq__(self, other: object) -> bool:
        """Compare persons by ID."""
        if not isinstance(other, Person):
            return False
        return self.person_id == other.person_id

    def __repr__(self) -> str:
        """Return person representation."""
        return f"{self.__class__.__name__}(id={self.person_id}, name={self.name})"

    @abstractmethod
    def get_role(self) -> str:
        """Get the role of this person."""
        pass

    @classmethod
    def get_total_people(cls) -> int:
        """Get total number of people created."""
        return cls._total_people


class Student(Person):
    """Represents a student enrolled in courses."""

    def __init__(self, person_id: str, name: str, email: str, initial_balance: float):
        """Initialize a student.
        
        Args:
            person_id: Unique identifier.
            name: Student's name.
            email: Student's email.
            initial_balance: Starting wallet balance.
        """
        super().__init__(person_id, name, email, initial_balance)
        self.enrolled_courses: List[str] = []  # Course IDs
        self._progress = 0.0  # Progress percentage

    @property
    def progress(self) -> float:
        """Get student's progress percentage (read-only derived property)."""
        return self._progress

    def set_progress(self, value: float) -> None:
        """Set progress percentage.
        
        Args:
            value: Progress percentage (0-100).
            
        Raises:
            ValueError: If value is not between 0 and 100.
        """
        if not (0 <= value <= 100):
            raise ValueError("Progress must be between 0 and 100.")
        self._progress = value

    def enroll(self, course_id: str) -> bool:
        """Enroll in a course.
        
        Args:
            course_id: ID of the course.
            
        Returns:
            True if enrollment successful, False otherwise.
        """
        if course_id not in self.enrolled_courses:
            self.enrolled_courses.append(course_id)
            return True
        return False

    def get_role(self) -> str:
        """Get the role of this person."""
        return "Student"


class PremiumStudent(Student):
    """Premium student with enhanced features and mentor matching."""

    def __init__(self, person_id: str, name: str, email: str, initial_balance: float):
        """Initialize a premium student.
        
        Args:
            person_id: Unique identifier.
            name: Student's name.
            email: Student's email.
            initial_balance: Starting wallet balance.
        """
        super().__init__(person_id, name, email, initial_balance)
        self.assigned_mentor: Optional[str] = None  # Mentor ID

    def enroll(self, course_id: str) -> bool:
        """Override enroll to include mentor matching.
        
        Args:
            course_id: ID of the course.
            
        Returns:
            True if enrollment successful, False otherwise.
        """
        # Premium students get priority and faster access
        result = super().enroll(course_id)
        if result:
            # Could perform mentor matching here
            pass
        return result

    def assign_mentor(self, mentor_id: str) -> None:
        """Assign a mentor to this premium student.
        
        Args:
            mentor_id: ID of the mentor.
        """
        if not mentor_id:
            raise ValueError("Mentor ID cannot be empty.")
        self.assigned_mentor = mentor_id

    def get_role(self) -> str:
        """Get the role of this person."""
        return "PremiumStudent"


class Mentor(Person):
    """Represents a mentor who can approve resource requests."""

    def __init__(self, person_id: str, name: str, email: str, initial_balance: float):
        """Initialize a mentor.
        
        Args:
            person_id: Unique identifier.
            name: Mentor's name.
            email: Mentor's email.
            initial_balance: Starting wallet balance.
        """
        super().__init__(person_id, name, email, initial_balance)
        self.approvals_count = 0
        self.denials_count = 0

    def approve_request(self) -> None:
        """Increment approval count."""
        self.approvals_count += 1

    def deny_request(self) -> None:
        """Increment denial count."""
        self.denials_count += 1

    def get_role(self) -> str:
        """Get the role of this person."""
        return "Mentor"
