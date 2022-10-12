import os

from fire import Fire
from ruamel import yaml

from src import CONFIG_YML


class Cmd(object):

    @staticmethod
    def init(name, debug=True, template='group'):
        """This is where we will create the robot configuration item.

        Args:
            name: Robot name.
            debug: Robot with debugging information display. for example: `True` | `False`
            template: Generated bot template files. for example:\n
                `01` -> individual\n
                `02` -> group\n
                `03` -> individual & group
        """
        CONFIG_YML.update({
            'name': name,
            'debug': debug if isinstance(debug, bool) else True,
            'template': template
        })
        with open(f'./{name}.yml', 'w', encoding='utf-8') as ym:
            yaml.dump(CONFIG_YML, ym, allow_unicode=True, Dumper=yaml.RoundTripDumper)

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
