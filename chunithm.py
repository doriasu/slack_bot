from bs4 import BeautifulSoup
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#id,passの指定
USER=input("idを入力してください")
PASS=input("パスワードを入力してください")

url="https://chunithm-net.com/mobile/"


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

driver.get("https://chunithm-net.com/mobile/record/musicGenre")
driver.find_element_by_xpath('//div[@id="inner"]/div[2]/div/div[3]/form/div[2]/div[4]/div').click()
time.sleep(1)
#楽曲用辞書
dict={}
#ジャンル順なので曲増えるごとに適宜追加(データは2019:9:12現在)
kyokusuu=[116,126,75,101,46,12,181]
for i in range(2,9):
    for j in range(1,kyokusuu[i-2]):
        xpath=driver.find_element_by_xpath('//div[@id="inner"]/div[2]/div/div[5]/div[{0}]/form[{1}]/div/div'.format(i,j))
        #div[2]/div/div[5]/div[2-8]/form[1-180]
        xpath.click()
        #beautifulsoupつかう和洋
        soup = BeautifulSoup(driver.page_source, "html.parser")
        kaisuu = soup.select(".bg_master span:nth-child(3)")
        title=soup.select(".play_musicdata_title")
        if len(kaisuu)==0:
            dict[title[0].string]=0
        else:
            dict[title[0].string]=int(kaisuu[0].string)
        driver.back()
        time.sleep(1)

dic2 = sorted(dict.items(), key=lambda x:x[1], reverse=True)
for i in range(len(dic2)):
    print(dic2[i])
driver.quit()