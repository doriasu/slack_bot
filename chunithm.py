import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import sys
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.chrome.options import Options

## Selectタグ利用
from selenium.webdriver.support.ui import Select

import chromedriver_binary

#id,passの指定
USER=""
PASS=""

url="https://chunithm-net.com/mobile/"

options=Options()
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)
driver.get(url)

#操作
driver.find_element_by_name('segaId').send_keys(USER)
element=driver.find_element_by_name('password')
element.send_keys(PASS)
element.send_keys(Keys.ENTER)
#aime選択
driver.implicitly_wait(1)
driver.find_element_by_class_name('btn_select_aime').click()

driver.get("https://chunithm-net.com/mobile/record/musicGenre/master")

html = driver.page_source
print(html)