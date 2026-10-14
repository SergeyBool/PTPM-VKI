import unittest
from unittest.mock import patch

from src.user_interface import UserInterface, ConsoleUserInterface


class TestUserInterface(unittest.TestCase):

    def test_abstract_class_cannot_be_instantiated(self):
        # Абстрактный класс нельзя создать напрямую
        with self.assertRaises(TypeError):
            UserInterface()

    def test_console_ui_returns_user_input(self):
        # Подменяем input() так, чтобы он возвращал три заранее заданные строки
        with patch('builtins.input', side_effect=["my_login", "Passw0rd!", "Passw0rd!"]):
            ui = ConsoleUserInterface()
            login, password, confirm_password = ui.get_user_data()

        self.assertEqual(login, "my_login")
        self.assertEqual(password, "Passw0rd!")
        self.assertEqual(confirm_password, "Passw0rd!")

    def test_console_ui_calls_input_three_times(self):
        with patch('builtins.input', side_effect=["a", "b", "c"]) as mock_input:
            ui = ConsoleUserInterface()
            ui.get_user_data()

        self.assertEqual(mock_input.call_count, 3)


if __name__ == '__main__':
    unittest.main()