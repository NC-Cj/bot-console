from sqlalchemy import Table, MetaData, Integer, String, Column

from app.models.base import DataBase


class City(DataBase):

    def __init__(self):
        super().__init__()
        # self.conn_str = 'sqlite:///city.db'
        self.conn_str = "mysql+pymysql://root:admin@localhost:3306/new_schema"
        self.table = Table(
            'city', MetaData(),
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('city_name', String(30)),
            Column('city_id', String(10))
        )

    def get_city_id(self, c):
        return self.engine_execute(
            self.table.select().with_only_columns(self.table.c.city_id).where(self.table.c.city_name == c)
        )
