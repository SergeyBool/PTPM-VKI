import unittest
from src.my_project import validate_registration

class TestValidateRegistration(unittest.TestCase):

    def test_password_and_confirm_mismatch(self):
        # Пароль и подтверждение не совпадают
        result, message = validate_registration("my_login", "Passw0rd!", "Different1!")
        self.assertFalse(result)
        self.assertEqual(message, "Пароли не совпадают.")

    def test_password_too_short(self):
        # Пароль короче 7 символов
        result, message = validate_registration("my_login", "Sh0rt!", "Sh0rt!")
        self.assertFalse(result)
        self.assertEqual(message, "Пароль должен содержать минимум 7 символов.")

    def test_password_no_uppercase(self):
        # Нет заглавной буквы
        result, message = validate_registration("my_login", "passw0rd!", "passw0rd!")
        self.assertFalse(result)
        self.assertEqual(message, "Пароль должен содержать хотя бы одну заглавную букву.")

    def test_password_no_lowercase(self):
        # Нет строчной буквы
        result, message = validate_registration("my_login", "PASSW0RD!", "PASSW0RD!")
        self.assertFalse(result)
        self.assertEqual(message, "Пароль должен содержать хотя бы одну строчную букву.")

    def test_password_no_digit(self):
        # Нет цифры
        result, message = validate_registration("my_login", "Password!", "Password!")
        self.assertFalse(result)
        self.assertEqual(message, "Пароль должен содержать хотя бы одну цифру.")

    def test_password_no_special(self):
        # Нет спецсимвола
        result, message = validate_registration("my_login", "Passw0rd", "Passw0rd")
        self.assertFalse(result)
        self.assertEqual(message, "Пароль должен содержать хотя бы один спецсимвол.")

    def test_login_in_blacklist(self):
        # Логин в чёрном списке
        result, message = validate_registration("admin", "Passw0rd!", "Passw0rd!")
        self.assertFalse(result)
        self.assertEqual(message, "Этот логин запрещён (находится в чёрном списке).")

    def test_login_too_short(self):
        # Логин (строка) короче 5 символов
        result, message = validate_registration("ab", "Passw0rd!", "Passw0rd!")
        self.assertFalse(result)
        self.assertEqual(message, "Логин (строка) должен содержать минимум 5 символов.")

    def test_login_invalid_chars(self):
        # Логин содержит русские буквы (длина 5, но есть недопустимый символ)
        result, message = validate_registration("abc_в", "Passw0rd!", "Passw0rd!")
        self.assertFalse(result)
        self.assertEqual(message, "Логин (строка) может содержать только латиницу, цифры и знак подчёркивания.")

    def test_login_phone_invalid(self):
        # Неверный формат телефона
        result, message = validate_registration("+7-99-123-4567", "Passw0rd!", "Passw0rd!")
        self.assertFalse(result)
        self.assertEqual(message, "Неверный формат телефона. Ожидается +x-xxx-xxx-xxxx.")

    def test_login_email_invalid(self):
        # Неверный формат email
        result, message = validate_registration("user@example", "Passw0rd!", "Passw0rd!")
        self.assertFalse(result)
        self.assertEqual(message, "Неверный формат email.")

    def test_login_exactly_five_chars(self):
        # Логин ровно 5 символов — граница (должен пройти)
        result, message = validate_registration("abcde", "Passw0rd!", "Passw0rd!")
        self.assertTrue(result)
        self.assertEqual(message, "")

    def test_login_four_chars(self):
        # Логин 4 символа — на 1 меньше границы (должен упасть)
        result, message = validate_registration("abcd", "Passw0rd!", "Passw0rd!")
        self.assertFalse(result)
        self.assertEqual(message, "Логин (строка) должен содержать минимум 5 символов.")

    def test_password_exactly_seven_chars(self):
        # Пароль ровно 7 символов — граница (должен пройти)
        result, message = validate_registration("my_login", "Passw0!", "Passw0!")
        self.assertTrue(result)
        self.assertEqual(message, "")

    def test_login_phone_valid(self):
        # Правильный формат телефона
        result, message = validate_registration("+7-999-123-4567", "Passw0rd!", "Passw0rd!")
        self.assertTrue(result)
        self.assertEqual(message, "")

    def test_login_email_valid(self):
        # Правильный формат email
        result, message = validate_registration("user@example.com", "Passw0rd!", "Passw0rd!")
        self.assertTrue(result)
        self.assertEqual(message, "")

    def test_login_blacklist_uppercase(self):
        # Логин из чёрного списка в верхнем регистре
        result, message = validate_registration("ADMIN", "Passw0rd!", "Passw0rd!")
        self.assertFalse(result)
        self.assertEqual(message, "Этот логин запрещён (находится в чёрном списке).")

    def test_login_with_digits_and_underscore(self):
        # Логин с цифрами и подчёркиванием (должен пройти)
        result, message = validate_registration("user_123", "Passw0rd!", "Passw0rd!")
        self.assertTrue(result)
        self.assertEqual(message, "")

    def test_login_empty(self):
        # Пустой логин
        result, message = validate_registration("", "Passw0rd!", "Passw0rd!")
        self.assertFalse(result)
        self.assertEqual(message, "Логин (строка) должен содержать минимум 5 символов.")

    def test_password_empty(self):
        # Пустой пароль
        result, message = validate_registration("my_login", "", "")
        self.assertFalse(result)
        self.assertEqual(message, "Пароль должен содержать минимум 7 символов.")

    def test_login_with_space(self):
        # Логин с пробелом (недопустимый символ)
        result, message = validate_registration("my login", "Passw0rd!", "Passw0rd!")
        self.assertFalse(result)
        self.assertEqual(message, "Логин (строка) может содержать только латиницу, цифры и знак подчёркивания.")

    def test_successful_registration(self):
        # Все данные корректны
        result, message = validate_registration("my_login", "Passw0rd!", "Passw0rd!")
        self.assertTrue(result)
        self.assertEqual(message, "")

if __name__ == '__main__':
    unittest.main()