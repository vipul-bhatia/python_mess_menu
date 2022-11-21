import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

chrome_options = Options()   
options = [
    "headless",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-gpu",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]

for option in options:
    chrome_options.add_argument(option)

    
driver = webdriver.Chrome(options = chrome_options, service = chrome_service)

driver.get('https://messmenu.epizy.com/')
d={}
d['date'] = driver.find_elements(by=selenium.webdriver.common.by.By.TAG_NAME, value='h3')[0].text
d['time'] = driver.find_elements(by=selenium.webdriver.common.by.By.TAG_NAME, value='h2')[0].text
d['occ'] = driver.find_elements(by=selenium.webdriver.common.by.By.TAG_NAME, value='h3')[1].text.encode("ascii", "ignore").decode()
li = driver.find_elements(by=selenium.webdriver.common.by.By.TAG_NAME, value='li')
d['li'] = [i.text for i in li]
if len(d['li'])==0:
    td = driver.find_elements(by=selenium.webdriver.common.by.By.TAG_NAME, value='td')
    d['td'] = {}
    for i in range(0,len(td)):
        if i % 2 == 0:
            d['td'][td[i].text] = td[i+1].text.encode("ascii", "ignore").decode().replace(" ", "")
driver.close()

"""
make a dictionary with key meal and value as d
"""
json1 = {}
json1['meal'] = []
json1['meal'].append(d)
with open('data.json', 'w') as outfile:
    json.dump(json1, outfile, indent=4)