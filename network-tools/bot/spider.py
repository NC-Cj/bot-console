import requests as requests

TOKEN = "EOk6j38PELxUwJy8"
virus_url = "https://v2.alapi.cn/api/springTravel/risk"
city = '天津市'


# 查询疫情城市

params = {
    "token": TOKEN,
    "province": city,
}
# 显示江西、江苏

result = requests.get(virus_url, params=params).json()
high_fx = result['data']['high_count']
middle_fx = result['data']['middle_count']

msg = f"""
-----疫情风险地区查询-----
{city}高风险数量：{high_fx}
{city}中风险数量：{middle_fx}
"""
