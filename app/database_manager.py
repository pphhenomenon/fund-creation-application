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
                department TEXT NOT NULL,
                contact_phone TEXT NOT NULL
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
                employee_name TEXT NOT NULL,
                document_designation TEXT NOT NULL,
                document_instance_number INTEGER NOT NULL,
                FOREIGN KEY (employee_name) REFERENCES Employees(employee_name),
                FOREIGN KEY (document_designation) REFERENCES Documents(document_designation),
                PRIMARY KEY (employee_name, document_designation)
            )
        """)

        self.connection.commit()

    def insert_employee(self, employee_name: str, department: str, contact_phone: str) -> None:
        """Insert a new employee or skip if the employee already exists."""
        # Check if employee already exists in the Employees table
        self.cursor.execute("SELECT 1 FROM Employees WHERE employee_name = ?", (employee_name,))
        result: Optional[Tuple[int]] = self.cursor.fetchone()

        if result is not None:
            print(f"Employee {employee_name} already exists in the database. Skipping insertion.")
        else:
            # Insert new employee into Employees table
            self.cursor.execute("""
                INSERT INTO Employees (employee_name, department, contact_phone)
                VALUES (?, ?, ?)
            """, (employee_name, department, contact_phone))
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

    def link_employee_to_document(self, employee_name: str, document_designation: str, document_instance_number: int) -> None:
        """Link an employee to a document in the Employees_Documents table."""
        # Check if the link between employee and document already exists
        self.cursor.execute("SELECT 1 FROM Employees_Documents WHERE employee_name = ? AND document_designation = ?", (employee_name, document_designation))
        result: Optional[Tuple[int]] = self.cursor.fetchone()

        if result is None:
            # Link employee to document in Employees_Documents table
            query = """
                INSERT INTO Employees_Documents (employee_name, document_designation, document_instance_number)
                VALUES (?, ?, ?)
            """
            self.cursor.execute(query, (employee_name, document_designation, document_instance_number))
            self.connection.commit()

    def get_all_documents(self) -> List[str]:
        """Retrieve all document designations from the Documents table."""
        self.cursor.execute("SELECT document_designation FROM Documents")
        documents = [row[0] for row in self.cursor.fetchall()]
        return documents

    def get_all_employees(self) -> List[str]:
        """Retrieve all employee names from the Employees table."""
        self.cursor.execute("SELECT employee_name FROM Employees")
        employees = [row[0] for row in self.cursor.fetchall()]
        return employees

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
