import requests
from lxml import etree


class neteaseMusicBot():
    """部分使用cloud-music.pl-fe.cn这个api"""

    def __init__(self) -> None:
        pass

    def top(self):
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}

        html = requests.get(
            "https://music.163.com/#/discover/toplist?id=19723756", headers=head).text
        print(html)


bot = neteaseMusicBot()
bot.top()
