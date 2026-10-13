import unittest
from src.delivery_service import calculate_delivery_cost


class TestDeliveryCost(unittest.TestCase):

    # --- Проверка входных данных ---

    def test_weight_below_minimum(self):
        cost, date = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_weight_above_maximum(self):
        cost, date = calculate_delivery_cost(50.1, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_distance_below_minimum(self):
        cost, date = calculate_delivery_cost(1.0, 0, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_distance_above_maximum(self):
        cost, date = calculate_delivery_cost(1.0, 5001, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_invalid_package_type(self):
        cost, date = calculate_delivery_cost(1.0, 100, "неизвестный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    # --- Базовый расчёт стоимости ---

    def test_basic_cost_no_coefficients(self):
        # weight=1, distance=100, обычный: 200 + 100*5 = 700
        cost, _ = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_fragile_package_adds_300(self):
        # 200 + 500 + 300 = 1000
        cost, _ = calculate_delivery_cost(1.0, 100, "хрупкий")
        self.assertEqual(cost, 1000)

    def test_dangerous_package_adds_1000(self):
        # 200 + 500 + 1000 = 1700
        cost, _ = calculate_delivery_cost(1.0, 100, "опасный")
        self.assertEqual(cost, 1700)

    # --- Весовые коэффициенты ---

    def test_weight_just_over_5_uses_1_2(self):
        # weight=5.1: (200+500)*1.2 = 840
        cost, _ = calculate_delivery_cost(5.1, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_weight_exactly_5_uses_1_2(self):
        # weight=5.0 (граница): ОЖИДАЕТСЯ (200+500)*1.2 = 840
        # БАГ: коэффициент не применяется, получаем 700
        cost, _ = calculate_delivery_cost(5.0, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_weight_just_below_20_uses_1_2(self):
        # weight=19.9: (200+500)*1.2 = 840
        cost, _ = calculate_delivery_cost(19.9, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_weight_exactly_20_uses_1_5(self):
        # weight=20: (200+500)*1.5 = 1050
        cost, _ = calculate_delivery_cost(20.0, 100, "обычный")
        self.assertEqual(cost, 1050)

    # --- Экспресс-доставка ---

    def test_express_costs_more_than_regular(self):
        # ОЖИДАЕТСЯ: экспресс дороже обычной доставки
        # БАГ: экспресс умножается на 0.5, то есть становится дешевле
        regular_cost, _ = calculate_delivery_cost(1.0, 100, "обычный", is_express=False)
        express_cost, _ = calculate_delivery_cost(1.0, 100, "обычный", is_express=True)
        self.assertGreater(express_cost, regular_cost)

    # --- Даты доставки ---

    def test_regular_delivery_days_1000km(self):
        # distance=1000: days = 1000//500 = 2, дата = 2026-09-03 + 2 = 2026-09-05
        _, date = calculate_delivery_cost(1.0, 1000, "обычный")
        self.assertEqual(date, "2026-09-05")

    def test_express_delivery_days_1000km(self):
        # distance=1000: days = 2, express: 2//2 = 1, дата = 2026-09-04
        _, date = calculate_delivery_cost(1.0, 1000, "обычный", is_express=True)
        self.assertEqual(date, "2026-09-04")

    def test_date_format(self):
        # Дата должна быть в формате YYYY-MM-DD
        _, date = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertRegex(date, r"^\d{4}-\d{2}-\d{2}$")


if __name__ == '__main__':
    unittest.main()