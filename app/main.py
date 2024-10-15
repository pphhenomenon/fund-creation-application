from typing import List


from database_manager import DatabaseManager
from test_data_generator import generate_test_data


if __name__ == "__main__":
    db: DatabaseManager = DatabaseManager("test_company.db")

    # Create tables
    db.create_tables()

    # Generate test data with 40 employees and 40 documents
    employee_count: int = 40
    document_count: int = 40
    generate_test_data(db, employee_count=employee_count, document_count=document_count)

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
