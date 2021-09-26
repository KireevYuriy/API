from lxml import html
from pprint import pprint
import requests
from pymongo import MongoClient

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/93.0.4577.63 Safari/537.36'}
url = 'https://yandex.ru/news/'
response = requests.get(url=url, headers=header)
dom = html.fromstring(response.text)
items = dom.xpath("//div[contains(@class,'news-top-flexible-stories')]/div[contains(@class,'mg-grid__col')]")
top_news = []
for item in items:
    item_date = {}
    news = item.xpath('.//h2/text()')
    news = ' '.join(news[0].split())
    source = item.xpath('.//a/@aria-label')
    source = ' '.join(source[0].split())
    tmp_link = item.xpath('.//a/@href')
    link = tmp_link[0]
    time = item.xpath('.//span/text()')

    item_date['Источник'] = source[9:]
    item_date['Новость'] = news
    item_date['Сылка'] = link
    item_date['Время'] = str(time)
    top_news.append(item_date)
pprint(top_news)

client = MongoClient('localhost', 27017)
db = client['top_news_yandex']
my = db.my
my.insert_many(top_news)
