from selenium import webdriver
from pprint import pprint
import time
import json

browser = webdriver.Chrome()
url = 'https://mp.weixin.qq.com/'
cookie = {}
browser.get(url)
time.sleep(2)
browser.find_element_by_xpath('//*[@id="account"]').clear()
browser.find_element_by_xpath('//*[@id="account"]').send_keys('username')

browser.find_element_by_xpath('//*[@id="pwd"]').clear()
browser.find_element_by_xpath('//*[@id="pwd"]').send_keys('password')

browser.find_element_by_xpath('//*[@id="loginForm"]/div[3]/label/i').click()
browser.find_element_by_xpath('//*[@id="loginBt"]').click()
time.sleep(10)

cookies = browser.get_cookies()
for item in cookies:
    cookie[item.get('name')] = item.get('value')
pprint(cookie)
with open('weixin_cookie.txt','w',encoding='utf-8') as f:
    f.write(json.dumps(cookie))
browser.close()








