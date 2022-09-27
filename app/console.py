import os
import sys

from ruamel import yaml

CONFIG_YML = {
    'monitorUserInfoList': ['wxid_rfmdl29r87jh22'],
    'script': None,
    'mysqlConnStr': None
}


def _init_robot(*args):
    os.makedirs('./images/', exist_ok=True)

    if not os.path.exists('./robot1.yml'):
        with open('robot1.yml', 'w', encoding='utf-8') as ym:
            yaml.dump(CONFIG_YML, ym, allow_unicode=True, Dumper=yaml.RoundTripDumper)


def _start_robot(*args):
    with open('./robot1.yml', 'r', encoding='utf-8') as ym:
        data = yaml.load(ym, Loader=yaml.Loader)

    print('机器人启动...')


def console(command, param):
    by.get(f'{command}')(*param)


by = {
    'init': _init_robot,
    'start': _start_robot,
}

if __name__ == '__main__':
    console(sys.argv[1], sys.argv[2:])
# pyinstaller -F -w -i robot.ico  gift.py

