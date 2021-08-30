import json
from bs4 import BeautifulSoup
import requests
import pprint

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko)'
                  'Chrome/92.0.4515.159 Mobile Safari/537.36',
    'Accept': '*/*'
}
# Код города Улан-Удэ
location = 20
vacation_inquiry = 'python'
page = 0

while True:

    url = f'https://hh.ru/search/vacancy?area={location}&text={vacation_inquiry.lower()}&page={page}'
    print(url)
    response = requests.get(url=url, headers=headers)
    src = response.text
    soup = BeautifulSoup(src, 'lxml')
    all_vacation_info = soup.find_all('div', {'class': 'vacancy-serp-item'})
    try:
        vacation_dict = []
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

            vacation_dict.append({
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
with open('vacation_data.json', "w+", encoding="utf-8") as file:
    json.dump(vacation_dict, file, indent=4, ensure_ascii=False)
