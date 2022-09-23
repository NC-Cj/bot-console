# -*- coding: utf-8 -*-
import sys

import ntchat

sys.path.append("../..")
from app.common import script

wechat = ntchat.WeChat()

# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)
by = {
    'help': script.help_,
    '疫情查询': script.query_virus_cities,
    '出行防疫': script.get_healthy_travel,
    '天气': script.get_weather,
    '快递': script.query_logistics,
    '早报': script.get_news_to_day,
}
# room_wxid = "48024453345@chatroom"  # test群


room_wxid = "17733202318@chatroom"  # 家族企业


# 注册消息回调
@wechat.msg_register(ntchat.MT_RECV_TEXT_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]
    from_wxid = data["from_wxid"]
    self_wxid = wechat_instance.get_login_info()["wxid"]
    sender = wechat_instance.get_contact_detail(from_wxid)['nickname']

    if data['msg'].startswith('/') and data['room_wxid'] != '' and from_wxid != self_wxid:
        methods_name = data['msg'].strip('/').split('-')[0]

        if methods_name in ['早报']:
            file = by[methods_name]()
            wechat_instance.send_image(room_wxid, file)
        else:
            params = data['msg'].strip('/').split('-')[1:]
            msg = by[methods_name](*params)
            wechat_instance.send_room_at_msg(room_wxid, f'@{sender}\n{msg}', [from_wxid])


try:
    while True:
        pass
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()
