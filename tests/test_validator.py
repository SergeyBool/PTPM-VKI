import unittest
from src.validator import Validator


class TestValidator(unittest.TestCase):

    def setUp(self):
        self.validator = Validator()

    def test_validate_success(self):
        result, message = self.validator.validate("my_login", "Passw0rd!", "Passw0rd!")
        self.assertTrue(result)
        self.assertEqual(message, "")

    def test_validate_blacklist_login(self):
        result, message = self.validator.validate("admin", "Passw0rd!", "Passw0rd!")
        self.assertFalse(result)
        self.assertEqual(message, "Этот логин запрещён (находится в чёрном списке).")

    def test_validate_password_mismatch(self):
        result, message = self.validator.validate("my_login", "Passw0rd!", "Different1!")
        self.assertFalse(result)
        self.assertEqual(message, "Пароли не совпадают.")

    def test_validate_short_password(self):
        result, message = self.validator.validate("my_login", "Sh0rt!", "Sh0rt!")
        self.assertFalse(result)
        self.assertEqual(message, "Пароль должен содержать минимум 7 символов.")

    def test_validate_short_login(self):
        result, message = self.validator.validate("ab", "Passw0rd!", "Passw0rd!")
        self.assertFalse(result)
        self.assertEqual(message, "Логин (строка) должен содержать минимум 5 символов.")


if __name__ == '__main__':
    unittest.main()