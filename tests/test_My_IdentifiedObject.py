import unittest
from model.identified_object import IdentifiedObject

class TestIdentifiedObject(unittest.TestCase):
    def test_initialization(self):
        obj = IdentifiedObject(123)
        self.assertEqual(obj.oid, 123)

    def test_equality(self):
        obj1 = IdentifiedObject(123)
        obj2 = IdentifiedObject(123)
        self.assertEqual(obj1, obj2)

    def test_inequality(self):
        obj1 = IdentifiedObject(123)
        obj2 = IdentifiedObject(456)
        self.assertNotEqual(obj1, obj2)

    def test_type_check(self):
        obj = IdentifiedObject(123)
        self.assertNotEqual(obj, "not an IdentifiedObject")

    def test_hash_uniqueness(self):
        obj1 = IdentifiedObject(123)
        obj2 = IdentifiedObject(123)
        self.assertEqual(hash(obj1), hash(obj2))

    def test_hash_collision(self):
        obj1 = IdentifiedObject(123)
        obj2 = IdentifiedObject(456)
        self.assertNotEqual(hash(obj1), hash(obj2))


if __name__ == '__main__':
    unittest.main()