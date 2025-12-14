from abc import ABC, abstractmethod
from typing import List
from .finance import Wallet


class Person(ABC):
    _id_counter = 1

    def __init__(self, name: str):
        if not name.strip():
            raise ValueError("Name cannot be empty")
        self.id = f"P-{Person._id_counter}"
        Person._id_counter += 1
        self.name = name
        self.wallet = Wallet(self)

    def __eq__(self, other):
        return isinstance(other, Person) and self.id == other.id

    @abstractmethod
    def role(self) -> str:
        pass


class Student(Person):
    def __init__(self, name: str):
        super().__init__(name)
        self.courses: List[str] = []
        self._progress = 0.0

    @property
    def progress(self) -> float:
        return self._progress

    @progress.setter
    def progress(self, value: float):
        if not 0 <= value <= 100:
            raise ValueError("Progress must be 0–100")
        self._progress = value

    def enroll(self, course):
        course.add_student(self)
        self.courses.append(course.name)
        return f"Enrolled: {self.name} -> {course.name}"

    def needs_resource(self) -> bool:
        return True

    def role(self) -> str:
        return "Student"


class PremiumStudent(Student):
    def enroll(self, course):
        mentor = course.assign_mentor()
        course.add_student(self)
        self.courses.append(course.name)
        return f"Enrolled: {self.name} -> {course.name} (mentor: {mentor.name})"

    def role(self) -> str:
        return "PremiumStudent"


class Mentor(Person):
    def __init__(self, name: str):
        super().__init__(name)
        self.approvals = 0

    def approve(self, resource, student):
        self.approvals += 1
        resource.allocate_to(student)

    def role(self) -> str:
        return "Mentor"
