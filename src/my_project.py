# Подключаем встроенную библиотеку Python для ведения логов (нашего «дневника»).
import logging
# Подключаем библиотеку для работы с системой. Она нам нужна, чтобы логгер мог писать в консоль (sys.stdout).
import sys
# Подключаем модуль регулярных выражений.
import re
# Подключаем модуль для хеширования.
import hashlib

import os


def setup_logging():
    """Настраивает логирование в консоль и файл."""
    # Создаём папку logs, если её нет
    os.makedirs("logs", exist_ok=True)

    # Шаблон строки лога
    log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Базовая настройка корневого логгера
    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/file_txt.log", encoding="utf-8")
        ]
    )

    logging.info("Логгер успешно сконфигурирован")

def mask_password(password):
    """
    Возвращает хеш пароля для логирования.
    Одинаковые пароли дают одинаковый хеш,
    разные — разный. Восстановить пароль по хешу нельзя.
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()[:8]

def validate_registration(login, password, confirm_password):
    """
    Проверяет данные для регистрации.
    Возвращает: (bool, str) — Успех и Сообщение.
    """
    # Буква f перед кавычками позволяет вставлять переменные прямо в текст внутри {}. Сюда подставится значение переменной login.
    # logging.info(f"Начало валидации. Логин: {login}")
    logging.info(f"Начало валидации. Логин: {login}, Пароль (маска): {mask_password(password)}")

    # Правило 0: Проверка чёрного списка логинов
    blacklist = ["admin", "root", "user", "test", "guest", "qwerty", "12345"]
    if login.lower() in blacklist:
        error_msg = "Этот логин запрещён (находится в чёрном списке)."
        logging.error(f"Ошибка валидации: {error_msg}")
        return False, error_msg

    # Правило 0.5: Проверка формата телефона или email
    if login.startswith("+"):
        # Это телефон. Проверяем формат: +x-xxx-xxx-xxxx
        phone_pattern = r'^\+\d-\d{3}-\d{3}-\d{4}$'
        if not re.match(phone_pattern, login):
            error_msg = "Неверный формат телефона. Ожидается +x-xxx-xxx-xxxx."
            logging.error(f"Ошибка валидации: {error_msg}")
            return False, error_msg
    elif "@" in login:
        # Это email. Проверяем стандартную маску
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, login):
            error_msg = "Неверный формат email."
            logging.error(f"Ошибка валидации: {error_msg}")
            return False, error_msg

    # Правило 1: Пароль и подтверждение должны совпадать
    if password != confirm_password:
        error_msg = "Пароли не совпадают."
        logging.error(f"Ошибка валидации: {error_msg}")
        return False, error_msg

    # Правило 2: Пароль должен быть не менее 7 символов
    if len(password) < 7:
        error_msg = "Пароль должен содержать минимум 7 символов."
        logging.error(f"Ошибка валидации: {error_msg}")
        return False, error_msg

    # Правило 3: Пароль должен содержать хотя бы одну заглавную букву
    has_upper = False
    for char in password:
        if char.isupper():
            has_upper = True
            break
    if not has_upper:
        error_msg = "Пароль должен содержать хотя бы одну заглавную букву."
        logging.error(f"Ошибка валидации: {error_msg}")
        return False, error_msg

    # Правило 4: Пароль должен содержать хотя бы одну строчную букву
    has_lower = False
    for char in password:
        if char.islower():
            has_lower = True
            break

    if not has_lower:
        error_msg = "Пароль должен содержать хотя бы одну строчную букву."
        logging.error(f"Ошибка валидации: {error_msg}")
        return False, error_msg

    # Правило 5: Пароль должен содержать хотя бы одну цифру
    has_digit = False
    for char in password:
        if char.isdigit():
            has_digit = True
            break

    if not has_digit:
        error_msg = "Пароль должен содержать хотя бы одну цифру."
        logging.error(f"Ошибка валидации: {error_msg}")
        return False, error_msg

    # Правило 6: Пароль должен содержать хотя бы один спецсимвол
    # Спецсимволы — это всё, что не буква и не цифра
    has_special = False
    for char in password:
        if not char.isalnum():  # isalnum() = True для букв и цифр
            has_special = True
            break

    if not has_special:
        error_msg = "Пароль должен содержать хотя бы один спецсимвол."
        logging.error(f"Ошибка валидации: {error_msg}")
        return False, error_msg

    # Правило 7: Проверка логина
    # Логин может быть телефоном, email или обычной строкой.
    # Пока реализуем только проверку обычной строки.

    # Сначала проверим, не телефон ли это и не email ли.
    # Если логин начинается с "+" — считаем, что это телефон.
    # Если содержит "@" — считаем, что это email.
    # Иначе — обычная строка.

    is_phone = login.startswith("+")
    is_email = "@" in login

    if not is_phone and not is_email:
        # Это обычная строка. Проверяем её по правилам:
        # 1. Минимум 5 символов.
        # 2. Только латиница, цифры и подчёркивание.

        if len(login) < 5:
            error_msg = "Логин (строка) должен содержать минимум 5 символов."
            logging.error(f"Ошибка валидации: {error_msg}")
            return False, error_msg

        # Проверяем каждый символ
        for char in login:
            if not (char.isascii() and (char.isalnum() or char == "_")):
                error_msg = "Логин (строка) может содержать только латиницу, цифры и знак подчёркивания."
                logging.error(f"Ошибка валидации: {error_msg}")
                return False, error_msg

    # Если все проверки пройдены (пока только одна)
    logging.info("Валидация пройдена успешно.")
    return True, ""



# --- ТОЧКА ВХОДА ---
# Это специальная конструкция Python. Она означает: «Выполни код ниже, только если этот файл запущен напрямую (а не импортирован в другой файл)». Это стандартная «точка входа» для программ.
if __name__ == '__main__':
    logging.info("Приложение запущено")

    # Тестовый вызов функции
    result, message = validate_registration("user@example.com", "Password0!", "Password0!")

    logging.info(f"Результат: {result}, Сообщение: '{message}'")