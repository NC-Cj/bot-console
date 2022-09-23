from requests import request

from app.models.city import City


class Spider:
    token = "EOk6j38PELxUwJy8"

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

    def help_(self):
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

    def get_healthy_travel(self, from_, to):
        """
        出行防疫政策指南
        :docs: https://alapi.cn/api/view/87
        """
        table = City()
        from_id = table.get_city_id(from_)
        to_id = table.get_city_id(to)

        url = "https://v2.alapi.cn/api/springTravel/query"
        payload = {
            'token': self.token,
            'from': from_id,
            'to': to_id
        }
        result = request('POST', url, params=payload, headers=self.headers).json()
        if result['code'] == 200:
            out_desc = result['data']['from_info']['out_desc']
            out_code_name = result['data']['from_info']['health_code_name']
            in_desc = result['data']['to_info']['low_in_desc']
            in_code_name = result['data']['to_info']['health_code_name']
            return f"🌏 {from_}出站：\n📕 健康码：{out_code_name}\n🚆 {out_desc}\n🌏 {to}进站：\n📕 健康码：{in_code_name}\n🚆 {in_desc}\n"

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
            print(result)
            new_state = result['data']['info'][-1]
            msg = f"⏰ 最新更新时间：{new_state['time']}\n📦 {new_state['content']}"

            return msg

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


script = Spider()
