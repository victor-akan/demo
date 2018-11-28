import json
import os

import numpy as np
import pandas as pd
from sqlalchemy import create_engine


def generate_example_data(example_db):
    """
    This function creates a sqlite database with a single table 'sales'.
    This table contains the data you need to solve the problem.
    """
    n_rows = 100
    engine = create_engine(example_db)
    df = pd.DataFrame(columns=['user', 'product', 'cost'])
    df['user'] = np.random.choice(['user1', 'user2', 'user3'], n_rows, replace=True)
    df['product'] = np.random.choice(['productA', 'productB', 'productC', 'productD'], n_rows, replace=True)
    df['cost'] = np.random.randint(0, 10000, n_rows)
    df.to_sql('sales', engine, if_exists='replace')


def solution(example_db):
    """
    This function contains your solution. 
    You should fill the results dictionary replacing None with the correct value. 
    In brackets the expected type is suggested.

    results = {
        # What is the highest price for a product (Int)
        'top_price': None,
        # Who is the user that spent the largest amount of money? (Str)
        'top_buyer': None,
        # Who is the second user in term of spending? (Str)
        'second_top_buyer': None,
        # What is the mean price for productC? (Float)
        'mean_price_productC': None,
        # How many different products did user2 buy? (Int)
        'number_of_products_userC': None
    }

    --------------------------------------------------
               EXAMPLE : 

    Consider the following table: 
    user   product  cost
    user1  productA   585
    user2  productC  2262
    user2  productC  4485
    user3  productD  7947
    user2  productC  4180

    The correct results is: 

    results = {
        'top_price': 7947,
        'top_buyer': user2,
        'second_top_buyer': user3,
        'mean_price_productC': 3642.333 ,
        'number_of_products_user2': 1
    }

    -------------------------------------------------

    Once you have filled the dictionary save the results to a json file. 

    Please use python 3. You can use pandas or numpy if you need.
    To generate the data you need to install sqlalchemy

    I suggest you to write a small test to validate your code.
    """

    engine = create_engine(example_db)

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

    query = engine.execute(sql).fetchone()

    top_buyer, second_top_buyer, top_price, mean_price_productC, number_of_products_user2 = query
    results = {
        'top_price': top_price,
        'top_buyer': top_buyer,
        'second_top_buyer': second_top_buyer,
        'mean_price_productC': mean_price_productC,
        'number_of_products_user2': number_of_products_user2
    }

    with open('results.json', 'w', encoding='utf8') as the_file:
        json.dump(results, the_file, indent=2)

    return results


def run():
    scriptdir = os.path.dirname(os.path.abspath(__file__))
    example_db = 'sqlite:///' + os.path.join(scriptdir, 'example.db')
    generate_example_data(example_db)

    return solution(example_db)


if __name__ == "__main__":
    from pprint import pprint

    pprint(run())
