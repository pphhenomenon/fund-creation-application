from database_manager import DatabaseManager


def test_database_manager():
    # Create an instance of the database manager
    db_manager = DatabaseManager(":memory:")  # Use in-memory database for testing
    db_manager.create_tables()

    # Insert employees
    db_manager.insert_employee("John Doe", "HR", "123-456-7890")
    db_manager.insert_employee("Jane Smith", "IT", "987-654-3210")

    # Insert documents
    db_manager.insert_document("DOC001", "Employee Handbook", 10)
    db_manager.insert_document("DOC002", "IT Security Policy", 5)

    # Link employees to documents
    db_manager.link_employee_to_document("John Doe", "DOC001", 1)
    db_manager.link_employee_to_document("Jane Smith", "DOC002", 2)

    # Test getting all employees
    employees = db_manager.get_all_employees()
    assert sorted(employees) == sorted(["John Doe", "Jane Smith"])

    # Test getting all documents
    documents = db_manager.get_all_documents()
    assert sorted(documents) == sorted(["DOC001", "DOC002"])

    # Test getting employees linked to a document
    employees_by_document = db_manager.get_employees_by_document("DOC001")
    assert sorted(employees_by_document) == sorted(["John Doe"])

    # Test getting documents linked to an employee
    documents_by_employee = db_manager.get_documents_by_employee("John Doe")
    assert sorted(documents_by_employee) == sorted(["DOC001"])

    # Close the database
    db_manager.close()

    print("All tests passed successfully!")


if __name__ == "__main__":
    # Run tests
    test_database_manager()
