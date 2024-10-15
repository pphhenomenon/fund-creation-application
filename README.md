# Database Functionality

This project implements a SQLite-based database system for managing employees and documents, with a many-to-many relationship between them. The database includes functionality for adding, updating, and retrieving information about employees, documents, and their relationships.

## Features

- **Employees table**: Stores information about employees, including their name, department, document instance number, and contact phone number.
- **Documents table**: Stores documents with a unique designation, name, and quantity.
- **Many-to-many relationship**: Employees can be linked to multiple documents, and documents can be associated with multiple employees.
- **Test data generation**: A utility to generate sample employees, documents, and relationships between them.
- **Retrieval methods**: Retrieve all employees linked to a specific document or all documents linked to a specific employee.

## Database Schema

### `Employees` Table
- `employee_name`: `TEXT` (Primary Key) – The full name of the employee.
- `document_instance_number`: `INTEGER` – The instance number of the document the employee is responsible for.
- `department`: `TEXT` – The department where the employee works.
- `contact_phone`: `TEXT` – The employee's contact phone number.

### `Documents` Table
- `document_designation`: `TEXT` (Primary Key) – The unique designation of the document.
- `document_name`: `TEXT` – The name of the document.
- `document_quantity`: `INTEGER` – The quantity of the document available.

### `Employees_Documents` Table (Many-to-many relationship)
- `employee_name`: `TEXT` (Foreign Key) – References the `employee_name` in the `Employees` table.
- `document_designation`: `TEXT` (Foreign Key) – References the `document_designation` in the `Documents` table.

## Getting Started

### Prerequisites

- Python 3.x
- SQLite

### Installation

1. Clone this repository to your local machine.
   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
   ```

2. Run the script:
   ```bash
   python main.py
   ```

### Usage

1. **Creating Tables**:
   The `create_tables()` method creates the `Employees`, `Documents`, and `Employees_Documents` tables if they do not exist.

2. **Inserting Employees**:
   Use `insert_employee()` to insert a new employee into the database. The function checks if the employee already exists based on the employee name. If the employee exists, the insertion is skipped.

   ```python
   db.insert_employee("John Doe", 1, "Finance", "+7 (900) 123-45-67")
   ```

3. **Inserting Documents**:
   Use `insert_document()` to insert a new document. It checks for document uniqueness by designation.

   ```python
   db.insert_document("DOC-001", "Document 1", 5)
   ```

4. **Linking Employees to Documents**:
   The `link_employee_to_document()` method creates a many-to-many relationship between employees and documents.

   ```python
   db.link_employee_to_document("John Doe", "DOC-001")
   ```

5. **Generating Test Data**:
   You can generate test data (40 employees and 40 documents by default) using the `generate_test_data()` function.

   ```python
   db.generate_test_data(employee_count=40, document_count=40)
   ```

6. **Retrieving Data**:
   - Get all employees linked to a specific document:
     ```python
     employees = db.get_employees_by_document("DOC-001")
     ```
   - Get all documents linked to a specific employee:
     ```python
     documents = db.get_documents_by_employee("John Doe")
     ```

7. **Closing the Connection**:
   Always remember to close the database connection after use:
   ```python
   db.close()
   ```

### Example

Here is a full example that demonstrates how to use the database functionality:

```python
from database_manager import DatabaseManager

db = DatabaseManager("test_company.db")

# Create tables
db.create_tables()

# Insert an employee
db.insert_employee("John Doe", 1, "Finance", "+7 (900) 123-45-67")

# Insert a document
db.insert_document("DOC-001", "Document 1", 5)

# Link employee to document
db.link_employee_to_document("John Doe", "DOC-001")

# Generate test data (40 employees and 40 documents)
db.generate_test_data(employee_count=40, document_count=40)

# Get all employees linked to a specific document
employees = db.get_employees_by_document("DOC-001")
print(f"Employees linked to DOC-001: {employees}")

# Get all documents linked to a specific employee
documents = db.get_documents_by_employee("John Doe")
print(f"Documents linked to John Doe: {documents}")

# Close the database connection
db.close()
```

## Contributing

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
