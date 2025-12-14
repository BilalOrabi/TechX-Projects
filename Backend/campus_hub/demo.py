from .People import Student, PremiumStudent, Mentor
from .education import Course
from .resources import Resource, ResourceCatalog
from .report import Report


def run_demo():
    mentor = Mentor("Omar")

    s1 = Student("Malik")
    s2 = PremiumStudent("Zahra")

    s1.wallet.deposit(500)
    s2.wallet.deposit(500)

    course = Course("Async Python", mentor)
    print(s2.enroll(course))

    s2.wallet.transfer(s1.wallet, 150)
    print(
        f"Wallet Transfer: Zahra -> Malik | "
        f"-150.00 credits (balance: {s2.wallet.balance:.2f} / {s1.wallet.balance:.2f})"
    )

    catalog = ResourceCatalog()
    r1 = Resource("R-001", "Lab")
    r2 = Resource("R-002", "Book")
    r3 = Resource("R-003", "Device")

    for r in (r1, r2, r3):
        catalog.add(r)

    mentor.approve(r1, s2)
    print(f"Resource Approved: {r1.type} for {s2.name} by Mentor {mentor.name}")

    print(f"Catalog ({len(catalog)} items):")
    for r in catalog:
        print(" ", r)

    report = Report.from_students([s1, s2], mentor, catalog)
    print(report)
