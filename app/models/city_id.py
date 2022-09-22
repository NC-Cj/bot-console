from sqlalchemy import Table, MetaData, Integer, String, Column

from app.common.db import DataBase


class City(DataBase):

    def __init__(self):
        super().__init__()
        self.conn_str = 'sqlite:///city.db'
        self.table = Table(
            'city', MetaData(),
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('city_name', String(30)),
            Column('city_id', String(10))
        )

# City().test()
