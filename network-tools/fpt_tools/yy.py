import time
import requests

# HTTP Debugger 抓包获取
t = input('>> 请输入HTTP Debugger抓包获取的t值：').strip()
loop = input('>> 请输入刷多少轮(默认99)：').strip() or '99'
loop = int(loop)

rank_time = 12
url = "https://cat-match.easygame2021.com/sheep/v1/game/game_over?rank_score=1&rank_state=1&rank_time={}&rank_role=1&skin=1".format(
    str(rank_time))
headers = {
    'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.28(0x18001c25) NetType/WIFI Language/en",
    "t": t,
    'Host': 'cat-match.easygame2021.com',
    'Accept': 'gzip,compress,br,deflate',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://servicewechat.com/wx141bfb9b73c970a9/15/page-frame.html',
}

if __name__ == '__main__':
    while loop > 0:
        try:
            r = requests.get(url=url, headers=headers, verify=False, timeout=10).json()
            print(r)
        except Exception as e:
            print('>> 出现异常: ' + str(e))
        loop -= 1
        time.sleep(2)
    print('>> 运行结束')
    input('>> 输入任意键退出...')