import pandas as pd
from sqlalchemy import create_engine


class ValidateSampleData():
    def __init__(self):
        self.engine = create_engine('sqlite://')

        df = pd.DataFrame(columns=['user', 'product', 'cost'])
        df['user'] = ['user1', 'user2', 'user2', 'user3', 'user2']
        df['product'] = ['productA', 'productC', 'productC', 'productD', 'productC']
        df['cost'] = [585, 2262, 4485, 7947, 4180]

        df.to_sql('sales', self.engine, if_exists='replace')

    def caller(self):
        sql = "SELECT MAX(cost) FROM sales"
        return self.engine.execute(sql).fetchone()


if __name__ == '__main__':
    vs = ValidateSampleData()
    print(vs.caller())
