from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['new_mvideo']
my = db.my
chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(executable_path='../chromedriver.exe', options=chrome_options)
driver.get('https://www.mvideo.ru/')
driver.implicitly_wait(10)
actions = ActionChains(driver)
# new_product = driver.find_element_by_xpath('//li[@class="gallery-list-item"]')
product = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[7]/div/div[2]')
actions.move_to_element(product)
actions.perform()
link = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[7]/div/div[2]/div/div[1]/'
                                    'a[contains(@class,"i-icon-fl-arrow-right")]')
new_set = set()
for i in range(6):
    names = driver.find_elements_by_xpath(
        '/html/body/div[2]/div/div[3]/div/div[7]//li/'
        '/a[@class="fl-product-tile-title__link sel-product-tile-title"]')
    for name in names:
        new_set.add(name.text)
    link.click()
new_product = []
for i in new_set:
    new_product.append(i)
print(new_product)
my_dict = {'Новинки': new_product}
my.insert_one(my_dict)
