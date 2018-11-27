import json
import os
import unittest

import pandas as pd
from sqlalchemy import create_engine


class ValidateSampleData(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite://')

        df = pd.DataFrame(columns=['user', 'product', 'cost'])
        df['user'] = ['user1', 'user2', 'user2', 'user3', 'user2']
        df['product'] = ['productA', 'productC', 'productC', 'productD', 'productC']
        df['cost'] = [585, 2262, 4485, 7947, 4180]
        df.to_sql('sales', self.engine, if_exists='replace')

    def test_exists(self):
        self.assertTrue(self.engine.execute("SELECT * FROM sales;"))

    def test_all_data(self):
        pull_data = self.engine.execute("SELECT * FROM sales;").fetchall()
        self.assertEqual(len(pull_data), 5)

    def test_top_price(self):
        sql = "SELECT MAX(cost) FROM sales"

        pull_data = self.engine.execute(sql).fetchone()
        self.assertEqual(pull_data, (7947,))

    def test_first_and_second_buyers(self):
        sql = """\
        SELECT user, costing
        FROM (SELECT user, SUM(cost) AS costing FROM sales GROUP BY user) inner_query
        ORDER BY costing DESC
        LIMIT 2
        """

        pull_data = self.engine.execute(sql).fetchall()
        self.assertEqual(pull_data, [('user2', 10927), ('user3', 7947)])

    def test_top_buyer(self):
        sql = """\
        SELECT user FROM (SELECT user, costing
        FROM (SELECT user, SUM(cost) AS costing FROM sales GROUP BY user) inner_query
        ORDER BY costing DESC
        LIMIT 2) LIMIT 1
        """

        pull_data = self.engine.execute(sql).fetchone()
        self.assertEqual(pull_data, ('user2',))

    def test_second_top_buyer(self):
        sql = """\
        SELECT user FROM (SELECT user, costing
        FROM (SELECT user, SUM(cost) AS costing FROM sales GROUP BY user) inner_query
        ORDER BY costing DESC
        LIMIT 2) ORDER BY costing LIMIT 1
        """

        pull_data = self.engine.execute(sql).fetchone()
        self.assertEqual(pull_data, ('user3',))

    def test_mean_price_productC(self):
        sql = "SELECT avg(cost) FROM sales WHERE product = 'productC'"

        pull_data = self.engine.execute(sql).fetchone()
        self.assertEqual(pull_data, (3642.3333333333335,))

    def test_mean_price_productC_rounded(self):
        sql = "SELECT round(avg(cost), 3) FROM sales WHERE product = 'productC'"

        pull_data = self.engine.execute(sql).fetchone()
        self.assertEqual(pull_data, (3642.333,))

    def test_number_of_products_user2(self):
        sql = "SELECT COUNT(DISTINCT product) FROM sales WHERE user = 'user2'"

        pull_data = self.engine.execute(sql).fetchone()
        self.assertEqual(pull_data, (1,))

    def test_all_query(self):
        sql = """\
        WITH first_and_second_buyers AS (SELECT user, costing
                                     FROM (SELECT user, SUM(cost) AS costing FROM sales GROUP BY user) inner_query
                                     ORDER BY costing DESC
                                     LIMIT 2),
         top_buyer AS (SELECT user FROM first_and_second_buyers LIMIT 1),
         second_top_buyer AS (SELECT user FROM first_and_second_buyers ORDER BY costing LIMIT 1),
         top_price AS (SELECT MAX(cost) FROM sales),
         mean_price_productC AS (SELECT avg(cost) FROM sales WHERE product = 'productC'),
         number_of_products_user2 AS (SELECT COUNT(DISTINCT product) FROM sales WHERE user = 'user2')


        SELECT *
        FROM top_buyer,
             second_top_buyer,
             top_price,
             mean_price_productC,
             number_of_products_user2
        """

        pull_data = self.engine.execute(sql).fetchone()
        self.assertEqual(pull_data, ('user2', 'user3', 7947, 3642.3333333333335, 1))

    def test_json_write(self):
        sql = """\
        WITH first_and_second_buyers AS (SELECT user, costing
                                     FROM (SELECT user, SUM(cost) AS costing FROM sales GROUP BY user) inner_query
                                     ORDER BY costing DESC
                                     LIMIT 2),
         top_buyer AS (SELECT user FROM first_and_second_buyers LIMIT 1),
         second_top_buyer AS (SELECT user FROM first_and_second_buyers ORDER BY costing LIMIT 1),
         top_price AS (SELECT MAX(cost) FROM sales),
         mean_price_productC AS (SELECT avg(cost) FROM sales WHERE product = 'productC'),
         number_of_products_user2 AS (SELECT COUNT(DISTINCT product) FROM sales WHERE user = 'user2')


        SELECT *
        FROM top_buyer,
             second_top_buyer,
             top_price,
             mean_price_productC,
             number_of_products_user2
        """

        query = self.engine.execute(sql).fetchone()

        top_buyer, second_top_buyer, top_price, mean_price_productC, number_of_products_user2 = query
        results = {
            'top_price': top_price,
            'top_buyer': top_buyer,
            'second_top_buyer': second_top_buyer,
            'mean_price_productC': mean_price_productC,
            'number_of_products_user2': number_of_products_user2
        }

        scriptdir = os.path.dirname(os.path.abspath(__file__))
        location = os.path.join(scriptdir, 'test_results.json')

        with open(location, 'w', encoding='utf8') as the_file:
            json.dump(results, the_file, indent=2)

        with open(location, 'r') as the_file:
            self.assertTrue(the_file)


if __name__ == '__main__':
    unittest.main()
