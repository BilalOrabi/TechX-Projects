"""Course module for managing courses."""
from typing import List


class Course:
    """Represents a course in the bootcamp."""

    max_students = 30  # Class attribute

    def __init__(self, course_id: str, name: str, mentor_id: str, capacity: Optional[int] = None):
        """Initialize a course.
        
        Args:
            course_id: Unique course identifier (non-empty).
            name: Course name (non-empty).
            mentor_id: ID of the mentor teaching this course.
            capacity: Maximum students (defaults to class max_students).
            
        Raises:
            ValueError: If any parameter is invalid.
        """
        if not course_id or not isinstance(course_id, str):
            raise ValueError("Course ID must be a non-empty string.")
        if not name or not isinstance(name, str):
            raise ValueError("Course name must be a non-empty string.")
        if not mentor_id or not isinstance(mentor_id, str):
            raise ValueError("Mentor ID must be a non-empty string.")

        self.course_id = course_id
        self.name = name
        self.mentor_id = mentor_id
        self.capacity = capacity or self.max_students
        self.current_students: List[str] = []  # Student IDs

    def add_student(self, student_id: str) -> bool:
        """Add a student to the course.
        
        Args:
            student_id: ID of the student.
            
        Returns:
            True if added, False if course is full or student already enrolled.
        """
        if student_id in self.current_students:
            return False
        if len(self.current_students) >= self.capacity:
            return False
        self.current_students.append(student_id)
        return True

    def is_full(self) -> bool:
        """Check if course has reached capacity."""
        return len(self.current_students) >= self.capacity

    def get_enrollment_count(self) -> int:
        """Get number of enrolled students."""
        return len(self.current_students)

    def __repr__(self) -> str:
        """Return course representation."""
        return f"Course(id={self.course_id}, name={self.name}, mentor={self.mentor_id})"

    def __str__(self) -> str:
        """Return human-readable course description."""
        return f"{self.name} (instructor: Mentor {self.mentor_id}, {self.get_enrollment_count()}/{self.capacity} students)"


from typing import Optional
