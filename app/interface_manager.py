import sys
import shutil

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QMessageBox,
    QComboBox,
    QFileDialog,
)
from PyQt6.QtGui import QAction

from database_manager import DatabaseManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.db_manager = None  # Инициализация переменной базы данных
        self.current_db_path = None  # Для хранения пути к текущей базе данных
        self.setWindowTitle("Управление сотрудниками и документами")
        
        # Создание меню
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Файл")
        
        # Добавление действий в меню
        new_db_action = QAction("Создать новую базу данных", self)
        new_db_action.triggered.connect(self.create_new_database)
        file_menu.addAction(new_db_action)
        
        open_db_action = QAction("Открыть существующую базу данных", self)
        open_db_action.triggered.connect(self.open_existing_database)
        file_menu.addAction(open_db_action)
        
        close_db_action = QAction("Закрыть базу данных", self)
        close_db_action.triggered.connect(self.close_database)
        file_menu.addAction(close_db_action)

        backup_db_action = QAction("Создать резервную копию", self)
        backup_db_action.triggered.connect(self.backup_database)
        file_menu.addAction(backup_db_action)
        
        # Основной виджет и макет
        layout = QVBoxLayout()

        # Поля для добавления сотрудника
        self.employee_name_input = QLineEdit(self)
        self.employee_name_input.setPlaceholderText("Имя сотрудника")
        self.department_input = QLineEdit(self)
        self.department_input.setPlaceholderText("Отдел")
        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("Контактный телефон")
        self.add_employee_button = QPushButton("Добавить сотрудника", self)
        self.add_employee_button.clicked.connect(self.add_employee)

        layout.addWidget(QLabel("Добавить сотрудника"))
        layout.addWidget(self.employee_name_input)
        layout.addWidget(self.department_input)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.add_employee_button)

        # Поля для добавления документа
        self.document_designation_input = QLineEdit(self)
        self.document_designation_input.setPlaceholderText("Обозначение документа")
        self.document_name_input = QLineEdit(self)
        self.document_name_input.setPlaceholderText("Название документа")
        self.quantity_input = QLineEdit(self)
        self.quantity_input.setPlaceholderText("Количество")
        self.add_document_button = QPushButton("Добавить документ", self)
        self.add_document_button.clicked.connect(self.add_document)

        layout.addWidget(QLabel("Добавить документ"))
        layout.addWidget(self.document_designation_input)
        layout.addWidget(self.document_name_input)
        layout.addWidget(self.quantity_input)
        layout.addWidget(self.add_document_button)

        # Выпадающие списки для выбора сотрудника и документа
        self.employee_combo = QComboBox(self)
        self.document_combo = QComboBox(self)

        # Поле для ввода номера экземпляра документа
        self.document_instance_input = QLineEdit(self)
        self.document_instance_input.setPlaceholderText("Номер экземпляра документа")

        self.link_button = QPushButton("Связать сотрудника с документом", self)
        self.link_button.clicked.connect(self.link_employee_document)

        layout.addWidget(QLabel("Связать сотрудника и документ"))
        layout.addWidget(self.employee_combo)
        layout.addWidget(self.document_combo)
        layout.addWidget(self.document_instance_input)
        layout.addWidget(self.link_button)

        # Настройка центрального виджета
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Первоначальное обновление списков сотрудников и документов
        self.refresh_employee_and_document_lists()

    def create_new_database(self):
        """Создание новой базы данных"""
        file_path, _ = QFileDialog.getSaveFileName(self, "Создать новую базу данных", "", "SQLite Files (*.db);;All Files (*)")
        if file_path:
            if self.db_manager:
                self.db_manager.close()
            self.db_manager = DatabaseManager(file_path)
            self.db_manager.create_tables()
            self.current_db_path = file_path
            QMessageBox.information(self, "Успех", "Новая база данных создана!")
            self.refresh_employee_and_document_lists()

    def open_existing_database(self):
        """Открытие существующей базы данных"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть базу данных", "", "SQLite Files (*.db);;All Files (*)")
        if file_path:
            if self.db_manager:
                self.db_manager.close()
            self.db_manager = DatabaseManager(file_path)
            self.current_db_path = file_path
            QMessageBox.information(self, "Успех", "База данных открыта!")
            self.refresh_employee_and_document_lists()

    def close_database(self):
        """Закрытие текущей базы данных"""
        if self.db_manager:
            self.db_manager.close()
            self.db_manager = None
            self.current_db_path = None
            QMessageBox.information(self, "Успех", "База данных закрыта!")
            self.clear_lists_and_fields()

    def backup_database(self):
        """Создание резервной копии текущей базы данных"""
        if not self.current_db_path:
            QMessageBox.warning(self, "Ошибка", "Нет открытой базы данных для создания резервной копии.")
            return

        backup_path, _ = QFileDialog.getSaveFileName(self, "Создать резервную копию", "", "SQLite Files (*.db);;All Files (*)")
        if backup_path:
            try:
                shutil.copyfile(self.current_db_path, backup_path)
                QMessageBox.information(self, "Успех", f"Резервная копия базы данных создана по пути: {backup_path}")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось создать резервную копию: {e}")

    def clear_lists_and_fields(self):
        """Очистка всех полей ввода и выпадающих списков"""
        self.employee_combo.clear()
        self.document_combo.clear()
        
        # Очистка всех полей ввода
        self.employee_name_input.clear()
        self.department_input.clear()
        self.phone_input.clear()
        self.document_designation_input.clear()
        self.document_name_input.clear()
        self.quantity_input.clear()
        self.document_instance_input.clear()

    def add_employee(self):
        if not self.db_manager:
            QMessageBox.warning(self, "Ошибка", "Сначала создайте или откройте базу данных.")
            return

        name = self.employee_name_input.text()
        department = self.department_input.text()
        phone = self.phone_input.text()

        if name and department and phone:
            try:
                self.db_manager.insert_employee(name, department, phone)
                QMessageBox.information(self, "Успех", "Сотрудник добавлен!")
                self.refresh_employee_and_document_lists()
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось добавить сотрудника: {e}")
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля корректно.")

    def add_document(self):
        if not self.db_manager:
            QMessageBox.warning(self, "Ошибка", "Сначала создайте или откройте базу данных.")
            return

        designation = self.document_designation_input.text()
        name = self.document_name_input.text()
        quantity = self.quantity_input.text()

        if designation and name and quantity.isdigit():
            try:
                self.db_manager.insert_document(designation, name, int(quantity))
                QMessageBox.information(self, "Успех", "Документ добавлен!")
                self.refresh_employee_and_document_lists()
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось добавить документ: {e}")
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля корректно.")

    def link_employee_document(self):
        """Связывание сотрудника и документа"""
        if not self.db_manager:
            QMessageBox.warning(self, "Ошибка", "Сначала создайте или откройте базу данных.")
            return

        employee = self.employee_combo.currentText()
        document = self.document_combo.currentText()
        instance_number = self.document_instance_input.text()

        if employee and document and instance_number.isdigit():
            try:
                self.db_manager.link_employee_to_document(employee, document, int(instance_number))
                QMessageBox.information(self, "Успех", "Сотрудник и документ связаны!")
                self.refresh_employee_and_document_lists()
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось связать сотрудника и документ: {e}")
        else:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля корректно и выберите сотрудника и документ.")

    def refresh_employee_and_document_lists(self):
        """Обновление выпадающих списков сотрудников и документов"""
        if not self.db_manager:
            self.clear_lists_and_fields()
            return

        self.employee_combo.clear()
        self.document_combo.clear()

        employees = self.db_manager.get_all_employees()
        documents = self.db_manager.get_all_documents()

        self.employee_combo.addItems(employees)
        self.document_combo.addItems(documents)

    def closeEvent(self, event):
        if self.db_manager:
            self.db_manager.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
