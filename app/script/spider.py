import sys

from requests import request

sys.path.append('../../')
from app.config import TOKEN


class Spider:
    token = TOKEN

    def __init__(self):
        self.headers = {'Content-Type': "application/x-www-form-urlencoded"}
        self.command_list = [
            'help',
            '疫情查询',
            '出行防疫',
            '天气',
            '快递',
            '早报',
        ]

    @staticmethod
    def other(key):
        url = f'https://cn.bing.com/search?q="{key}"&FORM=BESBTB'
        return f'😢没有该指令，已自动根据你的指令搜索到如下内容，请点击查看\n{url}'

    def help_(self, *args):
        return f'🚩 命令格式：/命令名称\n🚩 注意：命令带有下划线请忽略填写\n🚩 命令列表：{self.command_list}'

    def query_virus_cities(self, province, city=None, county=None):
        """
        疫情风险地区查询
        :docs: https://alapi.cn/api/view/106
        """
        url = "https://v2.alapi.cn/api/springTravel/risk"
        payload = {
            'token': self.token,
            'province': province,
            'city': city,
            "country": county
        }

        result = request('POST', url, params=payload, headers=self.headers).json()
        if result['code'] == 200:

            if 10 > len(result['data']['high_list']) > 0:
                high_list = result['data']['high_list']
                msg = ''.join(f"{row['area_name']} - ⛔ 高风险社区：{len(row['communitys'])}个\n" for row in high_list)
            elif city is None:
                msg = f"{province} ⛔ 存在高风险地区：{result['data']['high_count']}个\n"
            else:
                msg = f"{city} ⛔ 存在高风险地区：{result['data']['high_count']}个\n"
            msg = f"{msg}⚠ 存在中风险地区：{result['data']['middle_count']}个\n最新发布时间：{result['data']['end_update_time']}"

            return msg

    def get_weather(self, city=None):
        """
        国内天气查询
        :docs: https://alapi.cn/api/view/65
        """
        url = 'https://v2.alapi.cn/api/tianqi'
        payload = {
            'token': self.token,
            'city': city
        }

        result = request('POST', url, params=payload, headers=self.headers).json()
        if result['code'] == 200:
            hour_list = result['data']['hour']
            msg = ''.join(f"⏰ {row['time'].split()[-1]} - {row['wea']} - {row['temp']}°\n" for row in hour_list)
            msg = f'今日早晨-明日早晨\n{msg}'

            return msg

    def query_logistics(self, number):
        """
        快递查询
        :docs: https://alapi.cn/api/view/63
        """
        url = 'https://v2.alapi.cn/api/kd'
        payload = {
            'token': self.token,
            'number': number,
            'order': 'asc'
        }

        result = request('POST', url, params=payload, headers=self.headers).json()
        if result['code'] == 200:
            new_state = result['data']['info'][-1]
            return f"⏰ 最新更新时间：{new_state['time']}\n📦 {new_state['content']}"

    def get_news_to_day(self):
        """
        每日60秒早报
        :docs: https://alapi.cn/api/view/93
        """
        url = 'https://v2.alapi.cn/api/zaobao'
        payload = {
            'token': self.token,
            'format': 'json'
        }

        result = request('POST', url, params=payload, headers=self.headers).json()
        if result['code'] == 200:
            image_url = result['data']['image']
            c = request('GET', image_url).content
            filename = r'D:\GI\network-tools\images\zaobao.png'

            with open(filename, 'wb') as f:
                f.write(c)

            return filename


class BySpiderCommand:
    script = Spider()
    By = {
        'help': script.help_,
        'other': script.other,
        '疫情查询': script.query_virus_cities,
        '天气': script.get_weather,
        '快递': script.query_logistics,
        '早报': script.get_news_to_day,
    }
