from requests import request


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

    @staticmethod
    def other(key):
        url = f'https://cn.bing.com/search?q="{key}"&FORM=BESBTB'
        return f'😢没有该指令，已自动根据你的指令搜索到如下内容，请点击查看\n{url}'

    @staticmethod
    def what_to_eat_today(*args):
        """
        今天吃什么
        :docs: https://www.apispace.com/eolink/api/eat222/apiDocument
        """
        url = "https://eolink.o.apispace.com/eat222/api/v1/forward/chishenme"
        payload = {"size": "3"}
        headers = {
            "X-APISpace-Token": "zbxmug9fyd25pvq7b37urfl2yqm46f0g",
            "Authorization-Type": "apikey"
        }

        result = request('GET', url, params=payload, headers=headers).json()
        if result['code'] == 200:
            return f'亲~，今日推荐的食谱，三选一吧🥙:\n【{result["data"]}】'

        return 'api 错误或者失效了'

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

            if 10 > len(result['config']['high_list']) > 0:
                high_list = result['config']['high_list']
                msg = ''.join(f"{row['area_name']} - ⛔ 高风险社区：{len(row['communitys'])}个\n" for row in high_list)
            elif city is None:
                msg = f"{province} ⛔ 存在高风险地区：{result['config']['high_count']}个\n"
            else:
                msg = f"{city} ⛔ 存在高风险地区：{result['config']['high_count']}个\n"
            msg = f"{msg}⚠ 存在中风险地区：{result['config']['middle_count']}个\n最新发布时间：{result['config']['end_update_time']}"

            return msg

        return 'api 错误或者失效了'

    def get_healthy_travel(self, from_, to):
        """
        出行防疫政策指南
        :docs: https://alapi.cn/api/view/87
        """
        return '该接口已取消'
        # table = City()
        # from_id = table.get_city_id(from_)
        # to_id = table.get_city_id(to)
        #
        # url = "https://v2.alapi.cn/api/springTravel/query"
        # payload = {
        #     'token': self.token,
        #     'from': from_id,
        #     'to': to_id
        # }
        #
        # result = request('POST', url, params=payload, headers=self.headers).json()
        # if result['code'] == 200:
        #     out_desc = result['config']['from_info']['out_desc']
        #     out_code_name = result['config']['from_info']['health_code_name']
        #     in_desc = result['config']['to_info']['low_in_desc']
        #     in_code_name = result['config']['to_info']['health_code_name']
        #
        #     return f"🌏 {from_}出站：\n📕 健康码：{out_code_name}\n🚆 {out_desc}\n🌏 {to}进站：\n📕 健康码：{in_code_name}\n🚆 {in_desc}\n"

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
            hour_list = result['config']['hour']
            msg = ''.join(f"⏰ {row['time'].split()[-1]} - {row['wea']} - {row['temp']}°\n" for row in hour_list)
            msg = f'今日早晨-明日早晨\n{msg}'

            return msg

        return 'api 错误或者失效了'

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
            new_state = result['config']['info'][-1]
            return f"⏰ 最新更新时间：{new_state['time']}\n📦 {new_state['content']}"

        return 'api 错误或者失效了'

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
            image_url = result['config']['image']
            c = request('GET', image_url).content
            filename = r'D:\GI\network-tools\images\zaobao.png'

            with open(filename, 'wb') as f:
                f.write(c)

            return filename

        return 'api 错误或者失效了'

    def oneiromancy(self, key):
        """
        周公解梦
        :docs: https://www.apispace.com/eolink/api/zgjm/guidence/
        """
        url = "https://eolink.o.apispace.com/zgjm/common/dream/searchDreamDetail"
        payload = {"keyword": key}
        headers = {
            "X-APISpace-Token": "zbxmug9fyd25pvq7b37urfl2yqm46f0g",
            "Authorization-Type": "apikey",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        result = request('POST', url, data=payload, headers=headers).json()
        if result['statusCode'] == '000000':
            contents = result["result"]
            msg = ''.join(f'关键字：{key}\n内容：{c["content"]}' for c in contents)

            return msg

        return 'api 错误或者失效了'


class BySpiderCommand:
    script = Spider()
    By = {
        'help': script.help_,
        'other': script.other,
        '疫情查询': script.query_virus_cities,
        '出行防疫': script.get_healthy_travel,
        '天气': script.get_weather,
        '快递': script.query_logistics,
        '早报': script.get_news_to_day,
        '吃东西': script.what_to_eat_today,
        '解梦': script.oneiromancy,
    }


script = Spider()
print(script.oneiromancy('分手'))
