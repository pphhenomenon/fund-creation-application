from database_manager import DatabaseManager


def test_database_manager():
    # Создаем экземпляр менеджера базы данных
    db_manager = DatabaseManager("database.db")  # Используем базу данных в памяти для тестирования
    db_manager.create_tables()

    # Вставляем сотрудников
    db_manager.insert_employee("John Doe", "HR", "123-456-7890")
    db_manager.insert_employee("Jane Smith", "IT", "987-654-3210")

    # Вставляем документы
    db_manager.insert_document("DOC001", "Employee Handbook", 10)
    db_manager.insert_document("DOC002", "IT Security Policy", 5)

    # Связываем сотрудников с документами
    db_manager.link_employee_to_document("John Doe", "DOC001", 1)
    db_manager.link_employee_to_document("Jane Smith", "DOC002", 2)

    # Тестируем получение всех сотрудников
    employees = db_manager.get_all_employees()
    assert sorted(employees) == sorted(["John Doe", "Jane Smith"]), f"Ошибка: {employees}"

    # Тестируем получение всех документов
    documents = db_manager.get_all_documents()
    assert sorted(documents) == sorted(["DOC001", "DOC002"]), f"Ошибка: {documents}"

    # Тестируем получение сотрудников, связанных с документом
    employees_by_doc1 = db_manager.get_employees_by_document("DOC001")
    assert sorted(employees_by_doc1) == sorted(["John Doe"]), f"Ошибка: {employees_by_doc1}"

    # Тестируем получение документов, связанных с сотрудником
    documents_by_emp1 = db_manager.get_documents_by_employee("John Doe")
    assert sorted(documents_by_emp1) == sorted(["DOC001"]), f"Ошибка: {documents_by_emp1}"

    # Закрываем базу данных
    db_manager.close()

    print("Все тесты пройдены успешно!")


# Запускаем тесты
test_database_manager()
