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
USER=input("idを入力してください")
PASS=input("passを入力してください")
kyoku=input("曲名を入力してください")
url="https://chunithm-net.com/mobile/"

options=Options()
options.add_argument('--headless')
driver = webdriver.Chrome()
driver.get(url)
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
#フレンド総合リストの作成
driver.get("https://chunithm-net.com/mobile/friend")
friend_list=[]
soup = BeautifulSoup(driver.page_source, "html5lib")
ninzu=soup.find_all("span",class_="ml_10")
ninzu=int(ninzu[0].string)
for i in range(ninzu):
    hito=soup.select(".w420:nth-child({}) a".format(5+i))
    friend_list.append(hito[0].string)
vs_list={}
#ランキングアクセスのための曲目リストの作成
driver.get("https://chunithm-net.com/mobile/record/musicGenre")
driver.find_element_by_xpath('//div[@id="inner"]/div[2]/div/div[3]/form/div[2]/div[4]/div').click()
html=driver.page_source
soup=BeautifulSoup(html,"html5lib")
music_title=soup.find_all("div",class_="music_title")
title_list={}
title_list_tmp=[]
shogou=False
for d in music_title:
    title_list[d.string]=[]
    title_list_tmp.append(d.string)
    if d.string==kyoku:
        shogou=True
if shogou==False:
    print("そのタイトルの楽曲は存在しません")
    sys.exit()
#アクセスインデックスの構築
#ジャンル順なので曲増えるごとに適宜追加(データは2019:9:12現在)
kyokusuu=[116,126,75,101,46,12,181]
l=0
for i in range(2,9):
    for j in range(1,kyokusuu[i-2]):
        title_list[title_list_tmp[l]].append(int(i))
        title_list[title_list_tmp[l]].append(int(j))
        l=l+1

while (len(friend_list)+1)!=len(vs_list):
    driver.get("https://chunithm-net.com/mobile/record/musicGenre")
    driver.find_element_by_xpath('//div[@id="inner"]/div[2]/div/div[3]/form/div[2]/div[4]/div').click()
    #フレンドデータの収集
    xpath=driver.find_element_by_xpath('//div[@id="inner"]/div[2]/div/div[5]/div[{0}]/form[{1}]/div/div'.format(title_list[kyoku][0],title_list[kyoku][1]))
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
    active=0
    for i in range(len(player_name)):
        vs_list[player_name[i].string]=score[i].string
        active=active+1
    #フレンドアクティブの入れ替え
    driver.get("https://chunithm-net.com/mobile/friend")
    soup = BeautifulSoup(driver.page_source, "html5lib")
    #アクティブ9人いるの前提で
    for i in range(active-1):
        driver.find_element_by_xpath('//div[@id="inner"]/div[2]/div/div[3]/div[2]/form/div').click()
    sum=0
    #フレンドリストの初期化
    friend_list=[]
    soup = BeautifulSoup(driver.page_source, "html5lib")
    ninzu=soup.find_all("span",class_="ml_10")
    ninzu=int(ninzu[0].string)
    for i in range(ninzu):
        hito=soup.select(".w420:nth-child({}) a".format(5+i))
        friend_list.append(hito[0].string)
    #アクティブ入れ替え
    for i in range(ninzu):
        hito=soup.select(".w420:nth-child({}) a".format(5+i))
        if hito[0].string in vs_list:
            sum=sum
        else:
            driver.find_element_by_xpath('//div[@id="inner"]/div[2]/div/div[{}]/div[2]/form/div'.format(3+i)).click()
            sum=sum+1
        if sum==9:
            break
for value in vs_list.values():
    value=int(value.replace(",",""))
dic2 = sorted(vs_list.items(), key=lambda x:x[1], reverse=True)
print(kyoku)
for i in range(len(dic2)):
    print(dic2[i])



