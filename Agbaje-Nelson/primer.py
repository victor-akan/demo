from sqlalchemy import create_engine


class ValidateSampleData():
    def __init__(self):
        self.sales_table = 'CREATE TABLE sales ( "index" BIGINT, user TEXT, product TEXT, cost BIGINT )'
        self.ix_sales_index = 'CREATE INDEX ix_sales_index ON sales ( "index")'

        self.engine = create_engine('sqlite://')

        # execute the sql queries
        self.engine.execute(self.sales_table)
        self.engine.execute(self.ix_sales_index)

        # this is the sample sample data provided
        data = ({"index": 0, "user": "user1", "product": "productA", "cost": 585},
                {"index": 1, "user": "user2", "product": "productC", "cost": 2262},
                {"index": 2, "user": "user2", "product": "productC", "cost": 4485},
                {"index": 3, "user": "user3", "product": "productD", "cost": 7947},
                {"index": 4, "user": "user2", "product": "productC", "cost": 4180}
                )

        sql = 'INSERT INTO sales ("index", user, product, cost) VALUES (:index, :user, :product, :cost)'
        for line in data:
            self.engine.execute(sql, **line)

    def caller(self):
        sql = "SELECT MAX(cost) FROM sales"
        return self.engine.execute(sql).fetchone()


if __name__ == '__main__':
    vs = ValidateSampleData()
    print(vs.caller())
