class Controller:
    """Класс-контроллер, реализующий сквозной сценарий регистрации."""

    def __init__(self, user_interface, database, validator, external_service):
        """
        user_interface: объект класса UserInterface
        database: объект класса Database
        validator: объект класса Validator
        external_service: объект класса ExternalService
        """
        self.user_interface = user_interface
        self.database = database
        self.validator = validator
        self.external_service = external_service

    def process_registration(self):
        """
        Сквозной сценарий:
        1. Запрашивает данные у пользователя.
        2. Проверяет, есть ли запись в БД.
           - Если нет: вычисляет результат и сохраняет в БД.
           - Если есть: берёт результат из БД.
        3. Отправляет результат во внешний сервис.
        4. Возвращает результат.
        """
        # Шаг 1: получаем данные от пользователя
        login, password, confirm_password = self.user_interface.get_user_data()

        # Шаг 2: проверяем, есть ли запись в БД
        record = self.database.get_record(login, password, confirm_password)

        if record is None:
            # Записи нет — вычисляем результат через валидатор
            result, message = self.validator.validate(login, password, confirm_password)
            # Сохраняем в БД
            self.database.add_record(login, password, confirm_password, result, message)
        else:
            # Запись есть — берём результат из БД
            result, message = record

        # Шаг 3: отправляем результат во внешний сервис
        # Формируем строку-результат для отправки
        if result:
            send_string = f"Регистрация успешна для логина: {login}"
        else:
            send_string = f"Ошибка регистрации для логина {login}: {message}"

        self.external_service.send_result(send_string)

        # Шаг 4: возвращаем результат
        return result, message