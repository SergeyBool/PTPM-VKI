import unittest
from unittest.mock import Mock

from src.validator import Validator
from src.database import Database
from src.user_interface import UserInterface
from src.external_service import FakeExternalService
from src.controller import Controller


class FakeUserInterface(UserInterface):
    """Заглушка для пользовательского ввода."""

    def __init__(self, login, password, confirm_password):
        self.login = login
        self.password = password
        self.confirm_password = confirm_password

    def get_user_data(self):
        return self.login, self.password, self.confirm_password


class TestController(unittest.TestCase):

    def setUp(self):
        self.db = Database(":memory:")
        self.validator = Validator()
        self.external_service = FakeExternalService()

    def tearDown(self):
        self.db.close()

    def test_successful_registration(self):
        ui = FakeUserInterface("new_user", "Passw0rd!", "Passw0rd!")
        controller = Controller(ui, self.db, self.validator, self.external_service)

        result, message = controller.process_registration()

        self.assertTrue(result)
        self.assertEqual(message, "")
        # Проверяем, что запись появилась в БД
        record = self.db.get_record("new_user", "Passw0rd!", "Passw0rd!")
        self.assertIsNotNone(record)
        # Проверяем отправку
        self.assertEqual(self.external_service.call_count, 1)
        self.assertIn("Регистрация успешна", self.external_service.last_sent)

    def test_failed_registration(self):
        ui = FakeUserInterface("new_user", "Passw0rd!", "Different1!")
        controller = Controller(ui, self.db, self.validator, self.external_service)

        result, message = controller.process_registration()

        self.assertFalse(result)
        self.assertEqual(message, "Пароли не совпадают.")
        # Запись всё равно сохраняется
        record = self.db.get_record("new_user", "Passw0rd!", "Different1!")
        self.assertIsNotNone(record)
        # Отправка с ошибкой
        self.assertEqual(self.external_service.call_count, 1)
        self.assertIn("Ошибка регистрации", self.external_service.last_sent)

    def test_existing_record_skips_validator(self):
        # Вручную кладём запись в БД
        self.db.add_record("existing", "Passw0rd!", "Passw0rd!", True, "")

        # Mock-валидатор — если его вызовут, тест упадёт
        mock_validator = Mock()

        ui = FakeUserInterface("existing", "Passw0rd!", "Passw0rd!")
        controller = Controller(ui, self.db, mock_validator, self.external_service)

        result, message = controller.process_registration()

        self.assertTrue(result)
        self.assertEqual(message, "")
        # Валидатор не должен вызываться
        mock_validator.validate.assert_not_called()
        # Отправка всё равно произошла
        self.assertEqual(self.external_service.call_count, 1)

    def test_new_record_calls_validator(self):
        # Mock-валидатор, который вернёт успех
        mock_validator = Mock()
        mock_validator.validate.return_value = (True, "")

        ui = FakeUserInterface("new_user", "Passw0rd!", "Passw0rd!")
        controller = Controller(ui, self.db, mock_validator, self.external_service)

        result, message = controller.process_registration()

        self.assertTrue(result)
        self.assertEqual(message, "")
        # Валидатор должен быть вызван один раз
        mock_validator.validate.assert_called_once_with("new_user", "Passw0rd!", "Passw0rd!")

    def test_external_service_receives_correct_success_string(self):
        ui = FakeUserInterface("test_user", "Passw0rd!", "Passw0rd!")
        controller = Controller(ui, self.db, self.validator, self.external_service)

        controller.process_registration()

        expected = "Регистрация успешна для логина: test_user"
        self.assertEqual(self.external_service.last_sent, expected)

    def test_external_service_receives_correct_error_string(self):
        ui = FakeUserInterface("test_user", "Passw0rd!", "Different1!")
        controller = Controller(ui, self.db, self.validator, self.external_service)

        controller.process_registration()

        expected = "Ошибка регистрации для логина test_user: Пароли не совпадают."
        self.assertEqual(self.external_service.last_sent, expected)


if __name__ == '__main__':
    unittest.main()