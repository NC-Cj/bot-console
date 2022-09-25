from sqlalchemy import Table, MetaData, Integer, String, Column

from app.models.base import DataBase


class User(DataBase):

    def __init__(self):
        super().__init__()
        self.conn_str = "mysql+pymysql://root:admin@localhost:3306/bot_schema"
        self.table = Table(
            'user', MetaData(),
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('from_wxid', String(255), primary_key=True),
            Column('account', String(255)),
            Column('user_remark', String(50))
        )

    def _operate_user_info(self, action, from_wxid, account, user_remark):
        if action == 'insert':
            self.engine_execute(getattr(self.table, action)().values(**{
                'from_wxid': from_wxid,
                'account': account,
                'user_remark': user_remark
            }))

    def push(self, from_wxid, account, user_remark):
        if res := self.conn_execute("SELECT 1 FROM `user` WHERE from_wxid = '%s'  LIMIT 1" % from_wxid):
            self._operate_user_info('update', from_wxid, account, user_remark)
        else:
            self._operate_user_info('insert', from_wxid, account, user_remark)

    def get_user_id(self, from_wxid):
        if res := self.engine_execute(
                self.table.select().with_only_columns(self.table.c.id).where(self.table.c.from_wxid == from_wxid)
        ):
            return res[0][0]

        return False

    def get_user_wxid(self, user_id):
        if res := self.engine_execute(
                self.table.select().with_only_columns(self.table.c.from_wxid).where(self.table.c.id == user_id)
        ):
            return res[0][0]

        return False


print(User().get_user_id('wxid_rfmdl29r87jh22'))
