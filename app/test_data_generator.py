import random
from typing import List
from database_manager import DatabaseManager


def generate_phone_number() -> str:
    """Generate a random Russian phone number in the format +7 (XXX) XXX-XX-XX."""
    area_code: str = f"{random.randint(900, 999)}"
    first_part: str = f"{random.randint(100, 999)}"
    second_part: str = f"{random.randint(10, 99)}"
    third_part: str = f"{random.randint(10, 99)}"
    return f"+7 ({area_code}) {first_part}-{second_part}-{third_part}"


def generate_test_data(db: DatabaseManager, employee_count: int = 40, document_count: int = 40) -> None:
    """Generate test data for Employees and Documents tables."""
    departments: List[str] = ["HR", "IT", "Finance", "Marketing", "Sales"]

    # Insert employees
    for i in range(1, employee_count + 1):
        employee_name: str = f"Employee {i:03}"
        document_instance_number: int = random.randint(1, 10)
        department: str = random.choice(departments)
        contact_phone: str = generate_phone_number()
        db.insert_employee(employee_name, document_instance_number, department, contact_phone)

    # Insert documents
    for i in range(1, document_count + 1):
        document_designation: str = f"DOC-{i:03}"
        document_name: str = f"Document {i}"
        document_quantity: int = random.randint(1, 20)
        db.insert_document(document_designation, document_name, document_quantity)

    # Link employees to random documents (many-to-many relationship)
    for i in range(1, employee_count + 1):
        employee_name: str = f"Employee {i}"
        for _ in range(random.randint(1, 5)):  # Each employee can be linked to 1-5 documents
            document_designation: str = f"DOC-{random.randint(1, document_count):03}"
            db.link_employee_to_document(employee_name, document_designation)
