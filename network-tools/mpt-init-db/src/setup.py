from src.db import Init
from src.models import *


def setup():
    url = 'mysql+pymysql://root:admin@localhost/new_schema'
    Init(url).create_tables([
        BurnRecord().table,
        SerialFactory().table
    ])


if __name__ == '__main__':
    setup()
