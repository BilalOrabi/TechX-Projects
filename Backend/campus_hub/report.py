class Report:
    def __init__(self, students, premium, approvals, catalog_size):
        self.students = students
        self.premium = premium
        self.approvals = approvals
        self.catalog_size = catalog_size

    @classmethod
    def from_students(cls, students, mentor, catalog):
        premium_count = sum(1 for s in students if s.role() == "PremiumStudent")
        return cls(len(students), premium_count, mentor.approvals, len(catalog))

    @staticmethod
    def format_currency(amount: float) -> str:
        return f"{amount:.2f} credits"

    def __add__(self, other):
        return Report(
            self.students + other.students,
            self.premium + other.premium,
            self.approvals + other.approvals,
            self.catalog_size + other.catalog_size,
        )

    def __str__(self):
        return (
            f"REPORT: students={self.students} | "
            f"premium={self.premium} | "
            f"mentor_approvals={self.approvals} | "
            f"catalog_size={self.catalog_size}"
        )
