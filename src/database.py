import sqlite3


class Database:
    """Класс для работы с базой данных SQLite."""

    def __init__(self, db_path="users.db"):
        """
        Инициализация подключения к БД.
        db_path: путь к файлу БД. Для тестов удобно использовать ":memory:".
        """
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        """Создаёт таблицу, если её ещё нет."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS registrations (
                login TEXT NOT NULL,
                password TEXT NOT NULL,
                confirm_password TEXT NOT NULL,
                result INTEGER NOT NULL,
                message TEXT NOT NULL,
                PRIMARY KEY (login, password, confirm_password)
            )
        """)
        self.connection.commit()

    def add_record(self, login, password, confirm_password, result, message):
        """Добавляет запись в БД."""
        try:
            self.cursor.execute(
                "INSERT INTO registrations (login, password, confirm_password, result, message) VALUES (?, ?, ?, ?, ?)",
                (login, password, confirm_password, int(result), message)
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            # Запись с таким ключом уже существует
            return False

    def get_record(self, login, password, confirm_password):
        """Возвращает запись по логину, паролю и подтверждению. Или None, если не найдено."""
        self.cursor.execute(
            "SELECT result, message FROM registrations WHERE login = ? AND password = ? AND confirm_password = ?",
            (login, password, confirm_password)
        )
        row = self.cursor.fetchone()
        if row is None:
            return None
        return bool(row[0]), row[1]

    def delete_record(self, login, password, confirm_password):
        """Удаляет запись. Возвращает True, если что-то удалилось."""
        self.cursor.execute(
            "DELETE FROM registrations WHERE login = ? AND password = ? AND confirm_password = ?",
            (login, password, confirm_password)
        )
        self.connection.commit()
        return self.cursor.rowcount > 0

    def close(self):
        """Закрывает соединение с БД."""
        self.connection.close()