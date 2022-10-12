import os

from fire import Fire
from ruamel import yaml

from src import ROBOT_CONFIGURATION
from src.tpl import tpl


class Cmd(object):

    @staticmethod
    def init(name, debug=True, template='01'):
        """This is where we will create the robot configuration item.

        Examples:
            1、bot init --name=test1 --debug=False --template=01\n
            2、bot init --name=test2 --template=03\n
            3、bot init --name=test3

        Args:
            name: Robot name.
            debug: Robot with debugging information display. for example: `True` | `False`
            template: Generated bot template files. for example:\n
                `01` -> listen group\n
                `02` -> listen individual\n
                `03` -> listen individual & group
        """
        ROBOT_CONFIGURATION.update({
            'name': name,
            'debug': debug if isinstance(debug, bool) else True,
            'template': tpl.get(template).get('name')
        })
        with open(f'./{name}.yml', 'w', encoding='utf-8') as ym:
            yaml.dump(ROBOT_CONFIGURATION, ym, allow_unicode=True, Dumper=yaml.RoundTripDumper)

        tpl_path = tpl.get(template).get('path')
        with open(tpl_path, 'r', encoding='utf-8') as content:
            with open(f'./{name}.py', 'w', encoding="utf-8") as f:
                f.write(content.read())

        print('Please wait, the package is downloading...')
        os.makedirs('./images/', exist_ok=True)
        os.system('pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r ./requirements.txt')
        print('done...')

    @staticmethod
    def close():
        """
        Terminate the background bot process
        """
        os.system('taskill /f /im pythonw')
        print('机器人终止...')

    @staticmethod
    def start():
        """
        Starting the robot process
        """
        file = list(filter(lambda n: n.endswith('.yml'), os.listdir('./')))
        if file is not None:
            with open(file[0], 'r', encoding='utf-8') as ym:
                data = yaml.load(ym, Loader=yaml.Loader)

            print('机器人启动...')
            if data['debug']:
                os.system(f'python {data.get("root")}')
            else:
                os.system(f'start pythonw {data.get("root")}')


def main():
    Fire(Cmd)


if __name__ == '__main__':
    main()
