from app.common.spider import Spider


class Cmd:

    def __init__(self):
        self.spider = Spider()

    def help_(self):
        return f'🚩 命令格式：/命令名称\n🚩 注意：命令带有下划线请忽略填写\n🚩 命令列表：{dir(self)[26:]}'

    # @staticmethod
    def epidemic(self, city):
        return self.spider.get_virus(city)

    def weather(self):
        pass


cmd = Cmd()
