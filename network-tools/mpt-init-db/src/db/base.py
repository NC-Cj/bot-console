import time
import traceback

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError, ResourceClosedError, OperationalError

from src.depend import load_excel_dict


class Base:

    def __init__(self):
        self.sleep = time.sleep
        self.db_engine = None

    def _init_db(self, conn=False):
        if self.db_engine is None:
            self.db_engine = create_engine(self.conn_str, pool_size=1, max_overflow=0, pool_recycle=3600,
                                           pool_pre_ping=True)
            if getattr(self, 'table', None) is not None:
                self.table.create(self.db_engine, checkfirst=True)

        return self.db_engine.connect() if conn else self.db_engine

    def _conn_execute(self, sql, ignore_errors=False, data=None, convert_to_list=True):
        conn = self._init_db(True)

        retries = 0
        while True:
            try:

                res = conn.execute(sql, **data) if data else conn.execute(sql)
                if convert_to_list:
                    res = list(res)
            except ResourceClosedError:
                return
            except OperationalError as e:
                if ignore_errors:
                    return

                retries += 1
                if retries >= 5:
                    raise e

                self.sleep(1)
                continue
            except SQLAlchemyError as e:
                if ignore_errors:
                    return
                else:
                    raise e
            else:
                return res
            finally:
                if conn:
                    conn.close()

    def _engine_execute(self, stmt, ignore_errors=False, data=None, convert_to_list=True):
        engine = self._init_db()
        retries = 0
        while True:
            try:
                res = engine.execute(stmt, data) if data else engine.execute(stmt)
                if convert_to_list:
                    res = list(res)
            except ResourceClosedError:
                return
            except OperationalError as e:
                if ignore_errors:
                    return

                retries += 1
                if retries >= 5:
                    raise e

                self.sleep(1)
                continue
            except SQLAlchemyError as e:
                if ignore_errors:
                    return
                else:
                    raise e
            else:
                return res

    @property
    def from_engine(self):
        return self._init_db(True)


class Init(Base):

    def __init__(self, url=None):
        super().__init__()
        self.conn_str = url

    def create_tables(self, models: list):
        for table in models:
            try:
                table.create(self.from_engine)
            except Exception as e:
                logger.error(f'Error: {e}\nfrom table: {table.name}')
                traceback.print_exc()
            else:
                logger.success(f'Created: {table.name}')

    def migrate_data(self, path):
        # TODO: 有问题
        try:
            values = load_excel_dict(path)
            self._engine_execute(self.table.insert(), data=values)
        except Exception as e:
            logger.error(f'Error: {e}\nfrom table: {self.table.name}')
            traceback.print_exc()
        else:
            logger.success(f'Write complete: {self.table.name}')
