import re


class Validator:
    """Класс для валидации данных регистрации."""

    def __init__(self):
        # Чёрный список логинов
        self.blacklist = ["admin", "root", "user", "test", "guest", "qwerty", "12345"]

    def validate(self, login, password, confirm_password):
        """
        Проверяет данные для регистрации.
        Возвращает: (bool, str) — Успех и Сообщение.
        """
        # Правило 0: Проверка чёрного списка логинов
        if login.lower() in self.blacklist:
            return False, "Этот логин запрещён (находится в чёрном списке)."

        # Правило 0.5: Проверка формата телефона или email
        if login.startswith("+"):
            phone_pattern = r'^\+\d-\d{3}-\d{3}-\d{4}$'
            if not re.match(phone_pattern, login):
                return False, "Неверный формат телефона. Ожидается +x-xxx-xxx-xxxx."
        elif "@" in login:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, login):
                return False, "Неверный формат email."

        # Правило 1: Пароль и подтверждение должны совпадать
        if password != confirm_password:
            return False, "Пароли не совпадают."

        # Правило 2: Пароль должен быть не менее 7 символов
        if len(password) < 7:
            return False, "Пароль должен содержать минимум 7 символов."

        # Правило 3: Заглавная буква
        if not any(c.isupper() for c in password):
            return False, "Пароль должен содержать хотя бы одну заглавную букву."

        # Правило 4: Строчная буква
        if not any(c.islower() for c in password):
            return False, "Пароль должен содержать хотя бы одну строчную букву."

        # Правило 5: Цифра
        if not any(c.isdigit() for c in password):
            return False, "Пароль должен содержать хотя бы одну цифру."

        # Правило 6: Спецсимвол
        if not any(not c.isalnum() for c in password):
            return False, "Пароль должен содержать хотя бы один спецсимвол."

        # Правило 7: Проверка логина (если это не телефон и не email)
        if not login.startswith("+") and "@" not in login:
            if len(login) < 5:
                return False, "Логин (строка) должен содержать минимум 5 символов."
            for char in login:
                if not (char.isascii() and (char.isalnum() or char == "_")):
                    return False, "Логин (строка) может содержать только латиницу, цифры и знак подчёркивания."

        # Если все проверки пройдены
        return True, ""