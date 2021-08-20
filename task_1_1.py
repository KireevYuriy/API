import requests
import json
#from pprint import pprint

url = 'https://api.github.com'
user = 'KireevYuriy'

inquiry = requests.get(f'{url}/users/{user}/repos')
with open('result.json', 'w') as f:
    json.dump(inquiry.json(), f)
for elem in inquiry.json():
    print(elem['name'])

#pprint(inquiry.json())
