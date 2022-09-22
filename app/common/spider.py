from requests import request


class Spider:
    token = "EOk6j38PELxUwJy8"
    virus_url = "https://v2.alapi.cn/api/springTravel/risk"
    healthy_travel_url = "https://v2.alapi.cn/api/springTravel/query"
    params = {"token": token}

    def __init__(self):
        pass

    def get_virus(self, province=None, city=None, county=None):
        payload = {
            'token': self.token,
            'province': province,
            'city': city,
            "country": county
        }
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        result = request('POST', self.virus_url, params=payload, headers=headers).json()

        if 10 > len(result['data']['high_list']) > 0:
            high_list = result['data']['high_list']
            msg = ''.join(f"{row['area_name']} - 高风险社区：{len(row['communitys'])}个\n" for row in high_list)
        elif city is None:
            msg = f"{province} 存在高风险地区：{result['data']['high_count']}个\n"
        else:
            msg = f"{city} 存在高风险地区：{result['data']['high_count']}个\n"

        msg = f"{msg}存在中风险地区：{result['data']['middle_count']}个\n最新发布时间：{result['data']['end_update_time']}"

        return msg

    def get_healthy_travel(self):
        result = request('get', self.virus_url, params=self.params).json()
        result = request('get', 'https://v2.alapi.cn/api/springTravel/city', params=self.params).json()
        print(result)


# print(Spider().get_virus('江西省'))
