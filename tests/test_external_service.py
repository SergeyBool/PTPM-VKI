import unittest

from src.external_service import ExternalService, FakeExternalService


class TestExternalService(unittest.TestCase):

    def test_abstract_class_cannot_be_instantiated(self):
        # Абстрактный класс нельзя создать напрямую
        with self.assertRaises(TypeError):
            ExternalService()

    def test_fake_service_send_returns_true(self):
        service = FakeExternalService()
        result = service.send_result("тестовое сообщение")
        self.assertTrue(result)

    def test_fake_service_saves_last_sent(self):
        service = FakeExternalService()
        service.send_result("первое сообщение")
        service.send_result("второе сообщение")

        self.assertEqual(service.last_sent, "второе сообщение")

    def test_fake_service_counts_calls(self):
        service = FakeExternalService()
        service.send_result("раз")
        service.send_result("два")
        service.send_result("три")

        self.assertEqual(service.call_count, 3)

    def test_fake_service_initial_state(self):
        service = FakeExternalService()
        self.assertIsNone(service.last_sent)
        self.assertEqual(service.call_count, 0)


if __name__ == '__main__':
    unittest.main()