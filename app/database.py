import random
import sqlite3
from typing import List, Optional, Tuple


class DatabaseManager:
    def __init__(self, db_name: str) -> None:
        """Initialize the SQLite database connection."""
        self.connection: sqlite3.Connection = sqlite3.connect(db_name)
        self.cursor: sqlite3.Cursor = self.connection.cursor()

    def create_tables(self) -> None:
        """Create the Employees, Documents, and Employees_Documents tables."""
        # Create Employees table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Employees (
                employee_name TEXT PRIMARY KEY NOT NULL,
                document_instance_number INTEGER,
                department TEXT,
                contact_phone TEXT
            )
        """)

        # Create Documents table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Documents (
                document_designation TEXT PRIMARY KEY NOT NULL,
                document_name TEXT NOT NULL,
                document_quantity INTEGER NOT NULL
            )
        """)

        # Create Employees_Documents table for many-to-many relationship
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Employees_Documents (
                employee_name TEXT,
                document_designation TEXT,
                FOREIGN KEY (employee_name) REFERENCES Employees(employee_name),
                FOREIGN KEY (document_designation) REFERENCES Documents(document_designation),
                PRIMARY KEY (employee_name, document_designation)
            )
        """)

        self.connection.commit()

    def insert_employee(self, employee_name: str, document_instance_number: int, department: str, contact_phone: str) -> None:
        """Insert a new employee or skip if the employee already exists."""
        # Check if employee already exists in the Employees table
        self.cursor.execute("SELECT 1 FROM Employees WHERE employee_name = ?", (employee_name,))
        result: Optional[Tuple[int]] = self.cursor.fetchone()

        if result is not None:
            print(f"Employee {employee_name} already exists in the database. Skipping insertion.")
        else:
            # Insert new employee into Employees table
            self.cursor.execute("""
                INSERT INTO Employees (employee_name, document_instance_number, department, contact_phone)
                VALUES (?, ?, ?, ?)
            """, (employee_name, document_instance_number, department, contact_phone))
            self.connection.commit()

    def insert_document(self, document_designation: str, document_name: str, document_quantity: int) -> None:
        """Insert a new document into the Documents table or skip if it exists."""
        # Check if document already exists in the Documents table
        self.cursor.execute("SELECT 1 FROM Documents WHERE document_designation = ?", (document_designation,))
        result: Optional[Tuple[int]] = self.cursor.fetchone()

        if result is None:
            # Insert new document into Documents table
            self.cursor.execute("""
                INSERT INTO Documents (document_designation, document_name, document_quantity)
                VALUES (?, ?, ?)
            """, (document_designation, document_name, document_quantity))
            self.connection.commit()
        else:
            print(f"Document with designation {document_designation} already exists. Skipping insertion.")

    def link_employee_to_document(self, employee_name: str, document_designation: str) -> None:
        """Link an employee to a document in the Employees_Documents table."""
        # Check if the link between employee and document already exists
        self.cursor.execute("SELECT 1 FROM Employees_Documents WHERE employee_name = ? AND document_designation = ?", (employee_name, document_designation))
        result: Optional[Tuple[int]] = self.cursor.fetchone()

        if result is None:
            # Link employee to document in Employees_Documents table
            self.cursor.execute("INSERT INTO Employees_Documents (employee_name, document_designation) VALUES (?, ?)", (employee_name, document_designation))
            self.connection.commit()

    def generate_test_data(self, employee_count: int = 40, document_count: int = 40) -> None:
        """Generate test data for Employees and Documents tables."""
        departments: List[str] = ["HR", "IT", "Finance", "Marketing", "Sales"]

        def generate_phone_number() -> str:
            """Generate a random Russian phone number in the format +7 (XXX) XXX-XX-XX."""
            area_code: str = f"{random.randint(900, 999)}"
            first_part: str = f"{random.randint(100, 999)}"
            second_part: str = f"{random.randint(10, 99)}"
            third_part: str = f"{random.randint(10, 99)}"
            return f"+7 ({area_code}) {first_part}-{second_part}-{third_part}"

        # Insert employees
        for i in range(1, employee_count + 1):
            employee_name: str = f"Employee {i}"
            document_instance_number: int = random.randint(1, 10)
            department: str = random.choice(departments)
            contact_phone: str = generate_phone_number()
            self.insert_employee(employee_name, document_instance_number, department, contact_phone)

        # Insert documents
        for i in range(1, document_count + 1):
            document_designation: str = f"DOC-{i:03}"
            document_name: str = f"Document {i}"
            document_quantity: int = random.randint(1, 20)
            self.insert_document(document_designation, document_name, document_quantity)

        # Link employees to random documents (many-to-many relationship)
        for i in range(1, employee_count + 1):
            employee_name: str = f"Employee {i}"
            for _ in range(random.randint(1, 5)):  # Each employee can be linked to 1-5 documents
                document_designation: str = f"DOC-{random.randint(1, document_count):03}"
                self.link_employee_to_document(employee_name, document_designation)

    def get_employees_by_document(self, document_designation: str) -> List[str]:
        """Get all employees linked to the specified document."""
        self.cursor.execute("SELECT employee_name FROM Employees_Documents WHERE document_designation = ?", (document_designation,))
        employees: List[str] = [row[0] for row in self.cursor.fetchall()]
        return employees

    def get_documents_by_employee(self, employee_name: str) -> List[str]:
        """Get all documents linked to the specified employee."""
        self.cursor.execute("SELECT document_designation FROM Employees_Documents WHERE employee_name = ?", (employee_name,))
        documents: List[str] = [row[0] for row in self.cursor.fetchall()]
        return documents

    def close(self) -> None:
        """Close the database connection."""
        self.connection.close()


# Example usage
if __name__ == "__main__":
    db: DatabaseManager = DatabaseManager("test_company.db")

    # Create tables
    db.create_tables()

    # Generate test data with 40 employees and 40 documents
    employee_count: int = 40
    document_count: int = 40
    db.generate_test_data(employee_count=employee_count, document_count=document_count)

    # Get employees linked to a specific document
    document_designation: str = "DOC-001"
    employees: List[str] = db.get_employees_by_document(document_designation)
    print(f"Employees linked to {document_designation}: {employees}")

    # Get documents linked to a specific employee
    employee_name: str = "Employee 1"
    documents: List[str] = db.get_documents_by_employee(employee_name)
    print(f"Documents linked to {employee_name}: {documents}")

    # Close the database connection
    db.close()
