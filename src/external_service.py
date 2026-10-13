from abc import ABC, abstractmethod


class ExternalService(ABC):
    """Абстрактный класс для взаимодействия со сторонней зависимостью."""

    @abstractmethod
    def send_result(self, result: str) -> bool:
        """
        Отправляет строку-результат во внешнюю систему (например, email-сервер).
        Возвращает: True, если отправка успешна.
        """
        pass


class FakeExternalService(ExternalService):
    """Заглушка для тестов: сохраняет последний результат, никуда не отправляя."""

    def __init__(self):
        self.last_sent = None
        self.call_count = 0

    def send_result(self, result: str) -> bool:
        self.last_sent = result
        self.call_count += 1
        return True