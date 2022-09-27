import os
import sys

import ntchat
from ruamel import yaml

from app.config import CONFIG_YML


def _main():
    try:
        while True:
            pass
    except KeyboardInterrupt:
        ntchat.exit_()
        sys.exit()


if __name__ == '__main__':
    wechat = ntchat.WeChat()
    wechat.open(smart=True)

    os.makedirs('./images/', exist_ok=True)

    if not os.path.exists('./robot1.yml'):
        with open('robot1.yml', 'w', encoding='utf-8') as ym:
            yaml.dump(CONFIG_YML, ym, allow_unicode=True, Dumper=yaml.RoundTripDumper)

    _main()

# # 读取配置文件
# with open('./robot1.yml', 'r', encoding='utf-8') as ym:
#     data = yaml.load(ym, Loader=yaml.Loader)
