from bs4 import BeautifulSoup
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.alert import Alert

#id,passの指定
USER=input("ユーザ名を入力してください")
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

driver.execute_script("javascript:(function(d,s){s=d.createElement('script');s.src='https://chuniviewer.net/js/getMusicScore.js?'+Date.now();d.getElementsByTagName('head')[0].appendChild(s);})(document);")
time.sleep(1)
Alert(driver).accept()
time.sleep(20)

#chunithmviewerでtwitterで認証をクリック
driver.find_element_by_css_selector('.btn:nth-child(3)').click()
time.sleep(1)
#twitter認証
mail=input("twitterのメールアドレスを入力してください")
pw_twitter=input("パスワードを入力してください")
driver.find_element_by_id('username_or_email').send_keys(mail)
driver.find_element_by_id('password').send_keys(pw_twitter)
driver.find_element_by_css_selector("#allow").click()
time.sleep(5)

#chunithmviewerの操作
driver.find_element_by_xpath('//nav[@id="nav"]/div/ul/li[2]/a').click()
soup = BeautifulSoup(driver.page_source, "html.parser")
best=soup.select("#rate_info_table tr:nth-child(3) > td:nth-child(2)")
recent=soup.select("#rate_info_table tr:nth-child(4) > td:nth-child(2)")
s="Best枠:{}".format(best[0].string)
print(s)
s="Recent枠:{}".format(recent[0].string)
print(s)




