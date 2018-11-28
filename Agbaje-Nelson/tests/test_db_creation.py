import unittest

from sqlalchemy import create_engine


class DBCreation(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite://')

    def test_select(self):
        self.assertEqual(self.engine.execute("SELECT 1").fetchone(), (1,))


if __name__ == '__main__':
    unittest.main()
