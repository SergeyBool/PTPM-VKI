from abc import ABC, abstractmethod


class UserInterface(ABC):
    """Абстрактный класс для взаимодействия с пользователем."""

    @abstractmethod
    def get_user_data(self):
        """
        Запрашивает у пользователя логин, пароль и подтверждение.
        Возвращает: (login, password, confirm_password).
        """
        pass


class ConsoleUserInterface(UserInterface):
    """Конкретная реализация: ввод через консоль."""

    def get_user_data(self):
        login = input("Введите логин: ")
        password = input("Введите пароль: ")
        confirm_password = input("Подтвердите пароль: ")
        return login, password, confirm_password