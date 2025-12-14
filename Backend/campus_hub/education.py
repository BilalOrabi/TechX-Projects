class Course:
    max_students = 2  # class attribute

    def __init__(self, name: str, mentor):
        if not name.strip():
            raise ValueError("Course name required")
        self.name = name
        self.mentor = mentor
        self.current_students = []

    def add_student(self, student):
        if len(self.current_students) >= Course.max_students:
            raise RuntimeError("Course is full")
        self.current_students.append(student)

    def assign_mentor(self):
        return self.mentor
