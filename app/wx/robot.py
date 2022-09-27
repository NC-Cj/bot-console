import ntchat

from app.main import wechat,


# 文本注册消息回调
@wechat.msg_register(ntchat.MT_RECV_TEXT_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]
    from_wxid = data["from_wxid"]
    room_wxid = data["room_wxid"]
    self_wxid = wechat_instance.get_login_info()["wxid"]
    sender = wechat_instance.get_contact_detail(from_wxid)['nickname']
    remark = wechat_instance.get_contact_detail(from_wxid)['remark']

    wechat_instance.send_text(to_wxid='a', content='1')
