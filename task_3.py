from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko)'
                  'Chrome/92.0.4515.159 Mobile Safari/537.36',
    'Accept': '*/*'
}


def mongo_db():
    location = 20
    vacation_inquiry = 'python'
    page = 0
    while True:
        client = MongoClient('127.0.0.1', 27017)
        db = client['hh_ru']
        vacation_db = db.vacation_db

        url = f'https://hh.ru/search/vacancy?area={location}&text={vacation_inquiry.lower()}&page={page}'
        print(url)
        response = requests.get(url=url, headers=headers)
        src = response.text
        soup = BeautifulSoup(src, 'lxml')
        all_vacation_info = soup.find_all('div', {'class': 'vacancy-serp-item'})
        try:
            for vacation in all_vacation_info:
                vacation_card = vacation.find('a')
                vacation_name = vacation_card.text
                vacation_href = vacation_card.get('href')
                sal_info = vacation.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text.split(' ')
                sal_cur = sal_info[-1]

                if sal_info[0] == 'от':
                    sal_min = int(sal_info[1].replace(u'\u202f', ''))
                    sal_max = None
                elif sal_info[0] == 'до':
                    sal_min = None
                    sal_max = int(sal_info[1].replace(u'\u202f', ''))
                else:
                    sal_min = int(sal_info[0].replace(u'\u202f', ''))
                    sal_max = int(sal_info[2].replace(u'\u202f', ''))
                vacation_db.insert_one({
                    'Название вакансии': vacation_name,
                    'Ссылка на вакансию': vacation_href,
                    'Минимальная зарплата': sal_min,
                    'Максимальная зарплата': sal_max,
                    'Валюта': sal_cur,
                })
            page += 1
        except:
            sal_min = None
            sal_max = None
            sal_cur = None

        if not soup.find(text='дальше'):
            break


mongo_db()
