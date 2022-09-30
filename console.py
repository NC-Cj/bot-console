import os
import pydoc
import sys
from traceback import print_exc

from ruamel import yaml

from src import CONFIG_YML


def _init_robot(*args):
    """
    Command: bot init [Configuration parameters] [Robot configuration file name]
    :param args:
        --debug: 允许查看机器人日志的debug版本
    """
    if len(args) >= 2:
        if args[0] == '--debug':
            CONFIG_YML.update({'debug': True})
        else:
            return pydoc.help(_init_robot)

    with open(f'./{args[-1]}.yml', 'w', encoding='utf-8') as ym:
        yaml.dump(CONFIG_YML, ym, allow_unicode=True, Dumper=yaml.RoundTripDumper)

    os.makedirs('./images/', exist_ok=True)
    print('Please wait, the package is downloading...')
    os.system('pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r ./requirements.txt')
    print('done...')


def _start_robot(*args):
    """
    Command: bot start [Robot name]
    :param args: Only one parameter is required
        - The robot name corresponds to the created robot configuration file name
    """
    if len(args) >= 2:
        return pydoc.help(_start_robot)

    file = list(filter(lambda n: n.endswith('.yml'), os.listdir('./')))
    if file is not None:
        with open(file[0], 'r', encoding='utf-8') as ym:
            data = yaml.load(ym, Loader=yaml.Loader)

        print('机器人启动...')
        if data['debug']:
            os.system(f'python {data.get("root")}')
        else:
            os.system(f'start pythonw {data.get("root")}')


def _close_robot(*args):
    """
    Command: bot close
    """
    if len(args) >= 2:
        return pydoc.help(_close_robot)

    os.system('taskill /f /im pythonw')
    print('机器人终止...')


def root(command, param):
    """
    Command: bot [command] [param]
    :param command:
        - `init`
        - `start`
        - `close`
    :param param: parameters passed to each command
    """
    try:
        by.get(f'{command}')(*param)
    except TypeError as e:
        if str(e).endswith('not callable'):
            pydoc.help(root)
        else:
            print_exc()


by = {
    'init': _init_robot,
    'start': _start_robot,
    'close': _close_robot,
}

if __name__ == '__main__':
    root(sys.argv[1], sys.argv[2:])
