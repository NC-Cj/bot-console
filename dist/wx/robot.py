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

    listen_room_wxid = set(config['listenRoomList'])
    listen_user_wxid = set(config['listenWeChatIdList'])

    self_wxid = wechat_instance.get_login_info()["wxid"]
    sender = wechat_instance.get_contact_detail(from_wxid)['nickname']
    remark = wechat_instance.get_contact_detail(from_wxid)['remark']

    if data['msg'].startswith('/'):
        zh_methods_name = data['msg'].strip('/').split('-')[0]
        params = data['msg'].strip('/').split('-')[1:]

        if room_wxid != '' and from_wxid != self_wxid and room_wxid in listen_room_wxid:
            _execute_send_engine(
                wechat_instance,
                'send_room_at_msg',
                zh_methods_name,
                params,
                room_wxid,
                sender,
                [from_wxid]
            )

        if room_wxid == '' and from_wxid != self_wxid and from_wxid in listen_user_wxid:
            _execute_send_engine(
                wechat_instance,
                'send_text',
                zh_methods_name,
                params,
                from_wxid
            )


def _execute_send_engine(
        wechat_instance: ntchat.WeChat,
        by_method: str,
        callable_methods_key: str,
        callable_methods_params: str,
        to_wxid: str,
        at: str = '',
        *args,
        **kwargs
):
    try:
        if callable_methods_key in {'早报'}:
            imag = script[callable_methods_key]()
            wechat_instance.send_image(to_wxid, imag)
        else:
            msg = script[callable_methods_key](callable_methods_params)
            if at != '':
                msg = f'@{at}\n{msg}'
            getattr(wechat_instance, by_method)(to_wxid, msg, *args, **kwargs)
    except KeyError:
        msg = script['other'](callable_methods_key)
        getattr(wechat_instance, by_method)(to_wxid, msg, *args, **kwargs)


try:
    while True:
        pass
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()
