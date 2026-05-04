"""Management command to seed the database with fake employee data."""
from __future__ import annotations

import logging
import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

logger = logging.getLogger(__name__)

DEPARTMENTS = [
    ("Engineering", "Software development and infrastructure"),
    ("Marketing", "Brand, growth, and customer acquisition"),
    ("Sales", "Revenue generation and client management"),
    ("Human Resources", "Talent acquisition, culture, and compliance"),
    ("Finance", "Accounting, budgeting, and financial planning"),
    ("Product", "Product strategy and roadmap"),
    ("Operations", "Process optimization and supply chain"),
    ("Legal", "Contracts, compliance, and risk management"),
]

RATINGS = ["exceptional", "exceeds_expectations", "meets_expectations", "needs_improvement"]
STATUSES = ["present", "absent", "late", "remote", "on_leave"]
EMP_STATUSES = ["active", "active", "active", "inactive", "on_leave"]


class Command(BaseCommand):
    """Seed the database with 50 fake employees, departments, attendance, and reviews."""

    help = "Seed the database with fake employee data using Faker"

    def add_arguments(self, parser) -> None:
        """Add --count argument to control number of employees created."""
        parser.add_argument(
            "--count",
            type=int,
            default=50,
            help="Number of employees to create (default: 50)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before seeding",
        )

    def handle(self, *args, **options) -> None:
        """Execute the seed_data command."""
        try:
            from faker import Faker
        except ImportError:
            self.stderr.write("Faker is not installed. Run: pip install Faker")
            return

        try:
            from attendance.models import AttendanceRecord
            from employees.models import Department, Employee, PerformanceReview
        except ImportError as exc:
            logger.error("Failed to import models: %s", exc)
            self.stderr.write(str(exc))
            return

        if options["clear"]:
            AttendanceRecord.objects.all().delete()
            PerformanceReview.objects.all().delete()
            Employee.objects.all().delete()
            Department.objects.all().delete()
            self.stdout.write("Cleared existing data.")

        fake = Faker()
        Faker.seed(42)

        departments = []
        for name, desc in DEPARTMENTS:
            dept, _ = Department.objects.get_or_create(name=name, defaults={"description": desc})
            departments.append(dept)
        self.stdout.write(f"Departments: {len(departments)}")

        count = options["count"]
        employees = []
        for _ in range(count):
            try:
                emp = Employee.objects.create(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.unique.email(),
                    phone=fake.phone_number()[:20],
                    department=random.choice(departments),
                    job_title=fake.job()[:150],
                    salary=round(random.uniform(40000, 180000), 2),
                    hire_date=fake.date_between(start_date="-5y", end_date="today"),
                    status=random.choice(EMP_STATUSES),
                )
                employees.append(emp)
            except Exception as exc:
                logger.warning("Could not create employee: %s", exc)

        self.stdout.write(f"Employees created: {len(employees)}")

        today = timezone.now().date()
        attendance_count = 0
        for emp in employees:
            for days_back in range(30):
                record_date = today - timedelta(days=days_back)
                try:
                    AttendanceRecord.objects.get_or_create(
                        employee=emp,
                        date=record_date,
                        defaults={
                            "status": random.choice(STATUSES),
                            "check_in": fake.time_object() if random.random() > 0.2 else None,
                        },
                    )
                    attendance_count += 1
                except Exception as exc:
                    logger.warning("Attendance record error: %s", exc)

        self.stdout.write(f"Attendance records created: {attendance_count}")

        review_count = 0
        for emp in employees:
            for _ in range(random.randint(1, 3)):
                try:
                    PerformanceReview.objects.create(
                        employee=emp,
                        reviewer=fake.name(),
                        review_date=fake.date_between(start_date="-2y", end_date="today"),
                        rating=random.choice(RATINGS),
                        comments=fake.paragraph(),
                        goals=fake.sentence(),
                    )
                    review_count += 1
                except Exception as exc:
                    logger.warning("Review creation error: %s", exc)

        self.stdout.write(f"Performance reviews created: {review_count}")
        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))
