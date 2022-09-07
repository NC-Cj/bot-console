import time

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError, ResourceClosedError, OperationalError


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
