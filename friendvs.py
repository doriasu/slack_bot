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
import time
import chromedriver_binary

#id,passの指定
USER=""
PASS=""

url="https://chunithm-net.com/mobile/"

options=Options()
options.add_argument('--headless')
driver = webdriver.Chrome()
driver.get(url)
print("曲名を入力してください")
vs_title=input()
#操作
driver.find_element_by_name('segaId').send_keys(USER)
element=driver.find_element_by_name('password')
element.send_keys(PASS)
element.send_keys(Keys.ENTER)
time.sleep(1)
#aime選択
driver.implicitly_wait(1)
driver.find_element_by_class_name('btn_select_aime').click()
time.sleep(1)

driver.get("https://chunithm-net.com/mobile/record/musicGenre")
driver.find_element_by_xpath('//div[@id="inner"]/div[2]/div/div[3]/form/div[2]/div[4]/div').click()
time.sleep(1)
#楽曲用辞書
dict={}
#楽曲リストの取得
html=driver.page_source
soup=BeautifulSoup(html,"html5lib")
music_title=soup.find_all("div",class_="music_title")
title_list={}
title_list_tmp=[]
shogou=False
for d in music_title:
    title_list[d.string]=[]
    title_list_tmp.append(d.string)
    if d.string==vs_title:
        shogou=True
if shogou==False:
    print("そのタイトルの楽曲は存在しません")
    sys.exit()


#ジャンル順なので曲増えるごとに適宜追加(データは2019:9:12現在)
kyokusuu=[116,126,75,101,46,12,181]
l=0
for i in range(2,9):
    for j in range(1,kyokusuu[i-2]):
        title_list[title_list_tmp[l]].append(int(i))
        title_list[title_list_tmp[l]].append(int(j))
        l=l+1
xpath=driver.find_element_by_xpath('//div[@id="inner"]/div[2]/div/div[5]/div[{0}]/form[{1}]/div/div'.format(title_list[vs_title][0],title_list[vs_title][1]))
#div[2]/div/div[5]/div[2-8]/form[1-180]
xpath.click()
#vsの取得処理
xpath=driver.find_element_by_xpath('//div[@id="inner"]/div[2]/div/div[3]/div/form[2]/div')
xpath.click()
#再取得忘れない！！
html=driver.page_source
soup=BeautifulSoup(html,"html5lib")
player_name=soup.find_all("div",class_="rank_block_name")
score=soup.find_all("div",class_="rank_block_num")
vsscore={}
for i in range(len(player_name)):
    vsscore[player_name[i].string]=score[i].string
    print("{}位:{},スコア:{}".format(i+1,player_name[i].string,score[i].string))
