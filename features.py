import json
import requests

from lxml import etree


class kugouMusicBot():
    def __init__(self) -> None:
        pass

    def top(self):
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

        topJson = requests.get(
            "http://m.kugou.com/rank/info/?rankid=8888&page=1&json=true", headers=head).text
        jsonDict = json.loads(topJson)
        print(json.dumps(jsonDict['info']))

    def top_list(self):
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

        topJson = requests.get(
            "http://m.kugou.com/rank/list&json=true", headers=head).text
        jsonDict = json.loads(topJson)
        print(jsonDict)


bot = kugouMusicBot()
bot.top()
