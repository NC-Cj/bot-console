import os
import sys
from imp import load_source

import ntchat
from ruamel import yaml

file = list(filter(lambda n: n.endswith('.yml'), os.listdir('./')))
if file is not None:
    with open(file[0], 'r', encoding='utf-8') as ym:
        data = yaml.load(ym, Loader=yaml.Loader)

    MainModel = ''
    model = load_source(MainModel, data['script']['fileName'])
    script = getattr(model, data['script']['bySet']).By

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
    self_wxid = wechat_instance.get_login_info()["wxid"]
    sender = wechat_instance.get_contact_detail(from_wxid)['nickname']
    remark = wechat_instance.get_contact_detail(from_wxid)['remark']

    if data['msg'].startswith('/') and data['room_wxid'] == room_wxid and from_wxid != self_wxid:
        methods_name = data['msg'].strip('/').split('-')[0]
        params = data['msg'].strip('/').split('-')[1:]

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


try:
    while True:
        pass
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()
