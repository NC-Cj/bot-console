import os
import sys
from imp import load_source

import ntchat
from ruamel import yaml

file = list(filter(lambda n: n.endswith('.yml'), os.listdir('./')))
config = None
if file is not None:
    with open(file[0], 'r', encoding='utf-8') as ym:
        config = yaml.load(ym, Loader=yaml.Loader)

    MainModel = ''
    model = load_source(MainModel, config['script']['fileName'])
    script = getattr(model, config['script']['bySet'])().By

    ntchat.set_wechat_exe_path(wechat_version='3.6.0.18')
    wechat = ntchat.WeChat()
    wechat.open(smart=True)
else:
    raise KeyboardInterrupt('Missing configuration file')


@wechat.msg_register(ntchat.MT_RECV_TEXT_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]
    from_wxid = data["from_wxid"]
    room_wxid = data["room_wxid"]

    listen_room_wxid = config['listenRoomList'] or [room_wxid]
    listen_user_wxid = config['listenWeChatIdList'] or [from_wxid]

    self_wxid = wechat_instance.get_login_info()["wxid"]
    sender = wechat_instance.get_contact_detail(from_wxid)['nickname']
    remark = wechat_instance.get_contact_detail(from_wxid)['remark']

    if data['msg'].startswith('/'):
        methods_name = data['msg'].strip('/').split('-')[0]
        params = data['msg'].strip('/').split('-')[1:]

        if room_wxid in listen_room_wxid and from_wxid != self_wxid:
            # 监听群消息
            try:
                if methods_name in ['早报']:
                    imag = script[methods_name]()
                    wechat_instance.send_image(room_wxid, imag)
                else:
                    msg = script[methods_name](params)
                    wechat_instance.send_room_at_msg(room_wxid, f'@{sender}\n{msg}', [from_wxid])
            except KeyError:
                msg = script['other'](methods_name)
                wechat_instance.send_room_at_msg(room_wxid, f'@{sender}\n{msg}', [from_wxid])

        elif from_wxid in listen_user_wxid and data['room_wxid'] != '' and from_wxid != self_wxid:
            # 监听个人消息
            try:
                if methods_name in ['早报']:
                    imag = script[methods_name]()
                    wechat_instance.send_image(from_wxid, imag)
                else:
                    msg = script[methods_name](params)
                    wechat_instance.send_text(from_wxid, f'@{sender}\n{msg}')
            except KeyError:
                msg = script['other'](methods_name)
                wechat_instance.send_text(from_wxid, f'@{sender}\n{msg}')


def _execute_send(
        wechat_instance: ntchat.WeChat,
        by_method,
        to_wxid: str,
        content: str,
        *args,
        **kwargs
):
    getattr(wechat_instance, by_method)(to_wxid, content, *args, **kwargs)


try:
    while True:
        pass
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()
