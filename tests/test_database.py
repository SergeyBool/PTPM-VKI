import unittest
from src.database import Database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        # Для каждого теста — своя БД в памяти
        self.db = Database(":memory:")

    def tearDown(self):
        self.db.close()

    def test_add_record_returns_true(self):
        added = self.db.add_record("user1", "pass1", "pass1", True, "")
        self.assertTrue(added)

    def test_get_record_returns_data(self):
        self.db.add_record("user1", "pass1", "pass1", True, "")
        record = self.db.get_record("user1", "pass1", "pass1")

        self.assertIsNotNone(record)
        self.assertTrue(record[0])
        self.assertEqual(record[1], "")

    def test_get_record_returns_none_if_not_found(self):
        record = self.db.get_record("nobody", "nopass", "nopass")
        self.assertIsNone(record)

    def test_delete_record_returns_true(self):
        self.db.add_record("user2", "pass2", "pass2", False, "error")

        deleted = self.db.delete_record("user2", "pass2", "pass2")
        self.assertTrue(deleted)

        record = self.db.get_record("user2", "pass2", "pass2")
        self.assertIsNone(record)

    def test_delete_record_returns_false_if_not_found(self):
        deleted = self.db.delete_record("nobody", "nopass", "nopass")
        self.assertFalse(deleted)

    def test_duplicate_add_returns_false(self):
        self.db.add_record("user3", "pass3", "pass3", True, "")

        added = self.db.add_record("user3", "pass3", "pass3", True, "")
        self.assertFalse(added)

    def test_add_two_different_records(self):
        self.db.add_record("user4", "pass4", "pass4", True, "")
        self.db.add_record("user5", "pass5", "pass5", False, "error")

        record1 = self.db.get_record("user4", "pass4", "pass4")
        record2 = self.db.get_record("user5", "pass5", "pass5")

        self.assertIsNotNone(record1)
        self.assertIsNotNone(record2)
        self.assertTrue(record1[0])
        self.assertFalse(record2[0])


if __name__ == '__main__':
    unittest.main()