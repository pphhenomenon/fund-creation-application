import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QComboBox, QTableWidget, QTableWidgetItem, QHBoxLayout
from database_manager import DatabaseManager
from test_data_generator import generate_test_data
from typing import List

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Employee and Document Management")

        # Create database manager and ensure tables are created
        self.db = DatabaseManager("company.db")
        self.db.create_tables()

        # UI elements
        self.document_label = QLabel("Select Document:")
        self.employee_label = QLabel("Select Employee:")

        self.document_combo_box = QComboBox()
        self.employee_combo_box = QComboBox()

        self.employee_table = QTableWidget()
        self.document_table = QTableWidget()

        # Layout setup
        self.layout = QVBoxLayout()

        # Document selection layout
        document_layout = QHBoxLayout()
        document_layout.addWidget(self.document_label)
        document_layout.addWidget(self.document_combo_box)
        self.layout.addLayout(document_layout)

        # Employee selection layout
        employee_layout = QHBoxLayout()
        employee_layout.addWidget(self.employee_label)
        employee_layout.addWidget(self.employee_combo_box)
        self.layout.addLayout(employee_layout)

        # Table layouts
        self.layout.addWidget(QLabel("Employees related to selected document:"))
        self.layout.addWidget(self.employee_table)

        self.layout.addWidget(QLabel("Documents related to selected employee:"))
        self.layout.addWidget(self.document_table)

        self.setLayout(self.layout)

        # Populate the combo boxes with data from the database
        self.populate_combo_boxes()

        # Connect the combo boxes to the event handlers
        self.document_combo_box.currentIndexChanged.connect(self.on_document_selected)
        self.employee_combo_box.currentIndexChanged.connect(self.on_employee_selected)

        # Initialize tables
        self.init_tables()

    def populate_combo_boxes(self):
        """Populate combo boxes with document designations and employee names."""
        documents = self.db.get_all_documents()
        employees = self.db.get_all_employees()

        self.document_combo_box.clear()
        self.employee_combo_box.clear()

        for document in documents:
            self.document_combo_box.addItem(document)

        for employee in employees:
            self.employee_combo_box.addItem(employee)

    def init_tables(self):
        """Initialize the tables with default values."""
        self.employee_table.setColumnCount(2)
        self.employee_table.setHorizontalHeaderLabels(["Employee Name", "Department"])
        self.employee_table.setRowCount(0)

        self.document_table.setColumnCount(2)
        self.document_table.setHorizontalHeaderLabels(["Document Designation", "Document Name"])
        self.document_table.setRowCount(0)

    def on_document_selected(self):
        """Handler for document selection. Display all employees related to the selected document."""
        document = self.document_combo_box.currentText()
        if document:
            employees = self.db.get_employees_by_document(document)
            self.display_employees(employees)

    def on_employee_selected(self):
        """Handler for employee selection. Display all documents related to the selected employee."""
        employee = self.employee_combo_box.currentText()
        if employee:
            documents = self.db.get_documents_by_employee(employee)
            self.display_documents(documents)

    def display_employees(self, employees: List[str]):
        """Display the employees in the employee table."""
        self.employee_table.setRowCount(0)  # Clear the table before displaying new data
        for row_idx, employee in enumerate(employees):
            self.employee_table.insertRow(row_idx)
            self.employee_table.setItem(row_idx, 0, QTableWidgetItem(employee))  # Assuming employee is just the name
            self.employee_table.setItem(row_idx, 1, QTableWidgetItem("Unknown"))  # Set placeholder for department

    def display_documents(self, documents: List[str]):
        """Display the documents in the document table."""
        self.document_table.setRowCount(0)  # Clear the table before displaying new data
        for row_idx, document in enumerate(documents):
            self.document_table.insertRow(row_idx)
            self.document_table.setItem(row_idx, 0, QTableWidgetItem(document))  # Assuming document is just the designation
            self.document_table.setItem(row_idx, 1, QTableWidgetItem("Unknown"))  # Set placeholder for document name


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Ensure the database has some test data
    db_manager = DatabaseManager("company.db")
    db_manager.create_tables()
    generate_test_data(db_manager)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
