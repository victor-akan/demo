import json
import unittest


class ExpectedResult(unittest.TestCase):
    def setUp(self):
        self.results = json.dumps({
            'top_price': 7947,
            'top_buyer': 'user2',
            'second_top_buyer': 'user3',
            'mean_price_productC': 3642.333,
            'number_of_products_user2': 1
        })

    def test_results(self):
        self.assertIsNotNone(self.results)

    def test_top_price(self):
        self.assertEqual(json.loads(self.results).get('top_price'), 7947)

    def test_top_buyer(self):
        self.assertEqual(json.loads(self.results).get('top_buyer'), 'user2')

    def test_second_top_buyer(self):
        self.assertEqual(json.loads(self.results).get('second_top_buyer'), 'user3')

    def test_mean_price_productC(self):
        self.assertEqual(json.loads(self.results).get('mean_price_productC'), 3642.333)

    def test_number_of_products_user2(self):
        self.assertEqual(json.loads(self.results).get('number_of_products_user2'), 1)


if __name__ == '__main__':
    unittest.main()
