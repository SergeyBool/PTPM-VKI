import unittest
from unittest.mock import Mock

from src.validator import Validator
from src.database import Database
from src.user_interface import UserInterface
from src.external_service import FakeExternalService
from src.controller import Controller


class FakeUserInterface(UserInterface):
    """Заглушка для пользовательского ввода: возвращает заранее заданные данные."""

    def __init__(self, login, password, confirm_password):
        self.login = login
        self.password = password
        self.confirm_password = confirm_password

    def get_user_data(self):
        return self.login, self.password, self.confirm_password


class TestIntegration(unittest.TestCase):

    def setUp(self):
        # Для каждого теста — своя БД в памяти, чтобы тесты были независимы
        self.db = Database(":memory:")
        self.validator = Validator()
        self.external_service = FakeExternalService()

    def tearDown(self):
        self.db.close()

    # --- Интеграционный тест 1: успешная регистрация новых данных ---
    def test_successful_registration_new_data(self):
        ui = FakeUserInterface("new_user", "Passw0rd!", "Passw0rd!")
        controller = Controller(ui, self.db, self.validator, self.external_service)

        result, message = controller.process_registration()

        self.assertTrue(result)
        self.assertEqual(message, "")

        # Проверяем, что запись появилась в БД
        record = self.db.get_record("new_user", "Passw0rd!", "Passw0rd!")
        self.assertIsNotNone(record)
        self.assertTrue(record[0])

        # Проверяем, что отправка во внешний сервис произошла
        self.assertEqual(self.external_service.call_count, 1)
        self.assertIn("Регистрация успешна", self.external_service.last_sent)

    # --- Интеграционный тест 2: неуспешная регистрация (пароли не совпадают) ---
    def test_failed_registration_password_mismatch(self):
        ui = FakeUserInterface("new_user", "Passw0rd!", "Different1!")
        controller = Controller(ui, self.db, self.validator, self.external_service)

        result, message = controller.process_registration()

        self.assertFalse(result)
        self.assertEqual(message, "Пароли не совпадают.")

        # Запись всё равно сохраняется в БД (с ошибкой)
        record = self.db.get_record("new_user", "Passw0rd!", "Different1!")
        self.assertIsNotNone(record)
        self.assertFalse(record[0])

        # Отправка произошла
        self.assertEqual(self.external_service.call_count, 1)
        self.assertIn("Ошибка регистрации", self.external_service.last_sent)

    # --- Интеграционный тест 3: запись уже есть в БД, валидатор не вызывается ---
    def test_existing_record_uses_db_and_skips_validator(self):
        # Вручную добавляем запись в БД
        self.db.add_record("existing", "Passw0rd!", "Passw0rd!", True, "")

        # Создаём Mock-валидатор, чтобы проверить, что он не вызывается
        mock_validator = Mock()

        ui = FakeUserInterface("existing", "Passw0rd!", "Passw0rd!")
        controller = Controller(ui, self.db, mock_validator, self.external_service)

        result, message = controller.process_registration()

        self.assertTrue(result)
        self.assertEqual(message, "")

        # Валидатор не должен вызываться, потому что запись уже есть в БД
        mock_validator.validate.assert_not_called()

        # Отправка произошла
        self.assertEqual(self.external_service.call_count, 1)

    # --- Интеграционный тест 4: проверка строки, отправленной во внешний сервис ---
    def test_external_service_receives_correct_string(self):
        ui = FakeUserInterface("test_user", "Passw0rd!", "Passw0rd!")
        controller = Controller(ui, self.db, self.validator, self.external_service)

        controller.process_registration()

        expected = "Регистрация успешна для логина: test_user"
        self.assertEqual(self.external_service.last_sent, expected)

    # --- Тест 5: класс Database — добавление и получение ---
    def test_database_add_and_get(self):
        self.db.add_record("user1", "pass1", "pass1", True, "")
        record = self.db.get_record("user1", "pass1", "pass1")

        self.assertIsNotNone(record)
        self.assertTrue(record[0])
        self.assertEqual(record[1], "")

    # --- Тест 6: класс Database — удаление ---
    def test_database_delete(self):
        self.db.add_record("user2", "pass2", "pass2", False, "error")

        deleted = self.db.delete_record("user2", "pass2", "pass2")
        self.assertTrue(deleted)

        record = self.db.get_record("user2", "pass2", "pass2")
        self.assertIsNone(record)

    # --- Тест 7: класс Database — повторное добавление возвращает False ---
    def test_database_duplicate_add_returns_false(self):
        self.db.add_record("user3", "pass3", "pass3", True, "")

        added = self.db.add_record("user3", "pass3", "pass3", True, "")
        self.assertFalse(added)

    # --- Тест 8: Validator — не дублирует ЛР2, проверяет специфичный случай ---
    def test_validator_returns_error_for_short_login(self):
        result, message = self.validator.validate("ab", "Passw0rd!", "Passw0rd!")

        self.assertFalse(result)
        self.assertEqual(message, "Логин (строка) должен содержать минимум 5 символов.")


if __name__ == '__main__':
    unittest.main()