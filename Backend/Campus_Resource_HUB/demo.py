"""Demo module showcasing Campus Resource Hub functionality."""
from core import Student, PremiumStudent, Mentor, Course, Resource, ResourceStatus
from catalog import ResourceCatalog
from reports import Report
from mixins import AuditMixin


class AuditedStudent(Student, AuditMixin):
    """Student class with audit logging capabilities."""
    
    def __init__(self, person_id: str, name: str, email: str, initial_balance: float):
        """Initialize an audited student."""
        Student.__init__(self, person_id, name, email, initial_balance)
        AuditMixin.__init__(self)
    
    def enroll(self, course_id: str) -> bool:
        """Enroll in a course with audit logging."""
        result = super().enroll(course_id)
        if result:
            self.log_action("enrollment", f"Enrolled in course {course_id}")
        return result
    
    def needs_resource(self) -> bool:
        """Check if student needs a resource (for duck typing)."""
        return True


class AuditedMentor(Mentor, AuditMixin):
    """Mentor class with audit logging capabilities."""
    
    def __init__(self, person_id: str, name: str, email: str, initial_balance: float):
        """Initialize an audited mentor."""
        Mentor.__init__(self, person_id, name, email, initial_balance)
        AuditMixin.__init__(self)
    
    def approve_request(self) -> None:
        """Approve a request with audit logging."""
        super().approve_request()
        self.log_action("approval", "Approved a resource request")
    
    def deny_request(self) -> None:
        """Deny a request with audit logging."""
        super().deny_request()
        self.log_action("denial", "Denied a resource request")


def run_demo() -> None:
    """
    Demonstrate all features of Campus Resource Hub.
    
    This function demonstrates:
    - Student and PremiumStudent enrollment
    - Course management
    - Wallet operations and transfers
    - Resource borrowing with mentor approval
    - Resource catalog iteration
    - Audit logging through mixin
    - Report generation
    """
    print("=" * 70)
    print("CAMPUS RESOURCE HUB - DEMO")
    print("=" * 70)
    print()

    # ==================== SEED DATA ====================
    print("--- SEEDING DATA ---")
    
    # Create Students
    zahra = AuditedStudent("S001", "Zahra", "zahra@bootcamp.edu", 500.0)
    malik = AuditedStudent("S002", "Malik", "malik@bootcamp.edu", 300.0)
    
    # Create Premium Student
    premium_student = PremiumStudent("S003", "Ali", "ali@bootcamp.edu", 600.0)
    premium_student.assign_mentor("M001")
    print(f"Created Premium Student: {premium_student.name} (Mentor: {premium_student.assigned_mentor})")
    
    # Create Mentor
    omar = AuditedMentor("M001", "Omar", "omar@mentor.edu", 1000.0)
    
    # Create Courses
    course1 = Course("C001", "Async Python", "M001", capacity=5)
    course2 = Course("C002", "Web Frameworks", "M001", capacity=5)
    course3 = Course("C003", "Database Design", "M001", capacity=5)
    
    # Create Resources
    printer = Resource("R001", "3D Printer", "Lab", ResourceStatus.AVAILABLE)
    laptop = Resource("R002", "Laptop", "Equipment", ResourceStatus.AVAILABLE)
    whiteboard = Resource("R003", "Smart Whiteboard", "Lab", ResourceStatus.AVAILABLE)
    
    students_list = [zahra, malik, premium_student]
    courses_list = [course1, course2, course3]
    resources_list = [printer, laptop, whiteboard]
    
    print(f"Created {len(students_list)} students (including {1} premium)")
    print(f"Created {len(courses_list)} courses")
    print(f"Created {len(resources_list)} resources")
    print()

    # ==================== ENROLLMENTS ====================
    print("--- ENROLLMENTS ---")
    
    # Regular student enrolls
    if zahra.enroll("C001"):
        course1.add_student(zahra.person_id)
        print(f"✓ Enrolled: {zahra.name} -> {course1.name} (mentor: {course1.mentor_id.split(':')[0] if ':' in course1.mentor_id else 'Omar'})")
    
    if malik.enroll("C002"):
        course2.add_student(malik.person_id)
        print(f"✓ Enrolled: {malik.name} -> {course2.name}")
    
    # Premium student enrolls with mentor matching
    if premium_student.enroll("C003"):
        course3.add_student(premium_student.person_id)
        print(f"✓ Enrolled: {premium_student.name} -> {course3.name} (Premium: mentor matched)")
    print()

    # ==================== WALLET OPERATIONS ====================
    print("--- WALLET OPERATIONS ---")
    
    # Initial balances
    print(f"Initial Balance - {zahra.name}: {zahra.wallet.balance:.2f} credits")
    print(f"Initial Balance - {malik.name}: {malik.wallet.balance:.2f} credits")
    print()
    
    # Transfer
    print(f"Transferring 150.00 credits from {zahra.name} to {malik.name}...")
    zahra.wallet.transfer(malik.wallet, 150.0)
    zahra.log_action("transfer", f"Transferred 150.00 to {malik.name}")
    
    print(f"✓ Wallet Transfer: {zahra.name} -> {malik.name} | -150.00 credits")
    print(f"  After transfer - {zahra.name}: {zahra.wallet.balance:.2f} / 500.00")
    print(f"  After transfer - {malik.name}: {malik.wallet.balance:.2f} / 300.00")
    print()

    # ==================== RESOURCE CATALOG ====================
    print("--- RESOURCE CATALOG ---")
    
    catalog = ResourceCatalog()
    for resource in resources_list:
        catalog.add_resource(resource)
    
    print(f"Catalog Size: {len(catalog)} items")
    print("Resources in catalog:")
    for idx, resource in enumerate(catalog, 1):
        print(f"  {idx}. {resource}")
    print()

    # ==================== RESOURCE BORROWING & MENTOR APPROVAL ====================
    print("--- RESOURCE BORROWING & MENTOR APPROVAL ---")
    
    # First allocation - approve
    if zahra.needs_resource():
        if catalog.allocate(zahra):
            resource_borrowed = catalog.get_resource("R001")
            omar.approve_request()
            zahra.log_action("borrow", f"Borrowed {resource_borrowed.name}")
            print(f"✓ Resource Approved: {resource_borrowed.name} for {zahra.name} by Mentor {omar.name}")
    
    # Second allocation - approve
    if malik.needs_resource():
        if catalog.allocate(malik):
            resource_borrowed = catalog.get_resource("R002")
            omar.approve_request()
            malik.log_action("borrow", f"Borrowed {resource_borrowed.name}")
            print(f"✓ Resource Approved: {resource_borrowed.name} for {malik.name} by Mentor {omar.name}")
    print()

    # ==================== GENERATE REPORT ====================
    print("--- REPORT GENERATION ---")
    
    # Count mentor approvals
    total_approvals = omar.approvals_count
    
    # Create report using factory method
    report = Report.from_students(
        student_list=students_list,
        mentor_approval_count=total_approvals,
        catalog_size=len(catalog)
    )
    
    print(report)
    print()

    # ==================== AUDIT LOGS ====================
    print("--- AUDIT LOGS ---")
    
    print(f"\nAudit Log for {zahra.name}:")
    zahra.print_audit_log()
    
    print(f"Audit Log for {omar.name}:")
    omar.print_audit_log()

    # ==================== ADDITIONAL FEATURES ====================
    print("--- ADDITIONAL FEATURES ---")
    
    # Magic method: __eq__ for Person comparison
    another_zahra = AuditedStudent("S001", "Zahra", "zahra2@bootcamp.edu", 100.0)
    print(f"Person equality (by ID): zahra == another_zahra with same ID? {zahra == another_zahra}")
    print()
    
    # Magic method: __add__ for combining reports
    report2 = Report(students=1, premium_students=0, mentor_approvals=1, catalog_size=2)
    combined_report = report + report2
    print(f"Original Report: {report}")
    print(f"Report 2:        {report2}")
    print(f"Combined Report: {combined_report}")
    print()

    # Demonstrate class vs instance attributes
    print("--- CLASS VS INSTANCE ATTRIBUTES ---")
    print(f"Course.max_students (class attribute): {Course.max_students}")
    print(f"course1.capacity (instance attribute): {course1.capacity}")
    print(f"course1.current_students (instance list): {course1.current_students}")
    print()

    # Property demonstration
    print("--- PROPERTY DEMONSTRATION ---")
    zahra.set_progress(75.5)
    print(f"Student progress (read-only property): {zahra.progress}%")
    print(f"Wallet balance (guarded property): {zahra.wallet.balance}")
    print()

    print("=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    run_demo()
