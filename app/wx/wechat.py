# -*- coding: utf-8 -*-
import sys

import ntchat

from app.models.user import User

sys.path.append("../..")
from app.common import script

wechat = ntchat.WeChat()

# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)
by = {
    'help': script.help_,
    'other': script.other,
    'send': script.send,
    '疫情查询': script.query_virus_cities,
    '出行防疫': script.get_healthy_travel,
    '天气': script.get_weather,
    '快递': script.query_logistics,
    '早报': script.get_news_to_day,
}

message_reception_group = "48024453345@chatroom"  # test群
admin_wxid = 'wxid_auv3381tqzbz22'
bot_admin_nickname = 'Admin'


# room_wxid = "17733202318@chatroom"  # 家族企业

def get_msg(methods_name, params):
    try:
        msg = by[methods_name](*params)
    except KeyError:
        msg = by['other'](methods_name)

    return msg


# 注册消息回调
@wechat.msg_register(ntchat.MT_RECV_TEXT_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]
    from_wxid = data["from_wxid"]
    room_wxid = data["room_wxid"]
    self_wxid = wechat_instance.get_login_info()["wxid"]
    sender = wechat_instance.get_contact_detail(from_wxid)['nickname']
    remark = wechat_instance.get_contact_detail(from_wxid)['remark']

    if room_wxid == '' and from_wxid != '':
        res = wechat_instance.get_contact_detail(from_wxid)
        User().push(from_wxid, res['account'], res['remark'])

    # if from_wxid == 'wxid_auv3381tqzbz22' and room_wxid == '':
    if from_wxid == 'wxid_rfmdl29r87jh22' and room_wxid == '':
        msg = data['msg']
        user_id = User().get_user_id(from_wxid)

        if user_id is False:
            user_id = '数据库中没有该账号id, 不可转发消息'

        msg = f'@{bot_admin_nickname}\nFrom：{remark}\nuserID：{user_id}\nmsg：{msg}'
        wechat_instance.send_room_at_msg(
            message_reception_group,
            msg,
            [admin_wxid]
        )

    if data['msg'].startswith('/') and data['room_wxid'] == room_wxid and from_wxid != self_wxid:
        methods_name = data['msg'].strip('/').split('-')[0]
        params = data['msg'].strip('/').split('-')[1:]

        if methods_name in ['早报']:
            file = by[methods_name]()
            wechat_instance.send_image(room_wxid, file)
        elif methods_name == 'send':
            msg = get_msg(methods_name, params)
            wechat_instance.send_text(msg[0], f'{msg[1]}')
        else:
            msg = get_msg(methods_name, params)
            wechat_instance.send_room_at_msg(room_wxid, f'@{sender}\n{msg}', [from_wxid])


try:
    while True:
        pass
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()
