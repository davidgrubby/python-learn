import time

import requests
import bs4
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, ActionChains
from selenium.webdriver.common.keys import Keys

headers = {
    # ':authority': 'www.zhihu.com',
    # ':method': 'GET',
    # ':path': '/search?type=content&q=%E7%A9%BF%E6%90%AD',
    # ':scheme': 'https',
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 'accept-encoding': 'gzip, deflate, br',
    # 'accept-language': 'en-US,en;q=0.9',
    # 'cache-control': 'max-age=0',
    'cookie': 'cy=1; cye=shanghai; _lxsdk_cuid=166411ebf75c8-011fdb993ebb4b-4a506a-13c680-166411ebf76c8; _lxsdk=166411ebf75c8-011fdb993ebb4b-4a506a-13c680-166411ebf76c8; _hc.v=775d374e-531a-83b5-da96-0fe9406e26a4.1538690826; s_ViewType=10; _lx_utm=utm_source%3Ddp_pc_group; _lxsdk_s=1664cf3a1fd-c84-640-fc0%7C%7C184',
    'referer': 'http://www.dianping.com/shanghai/ch10/g110p2?aid=93077944%2C97435241%2C98281287%2C110269910&cpt=93077944%2C97435241%2C98281287%2C110269910',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0'
}

url_shop = "http://www.dianping.com/shop/2873341"

# 获取单店列表页面
r = requests.get(url_shop, headers=headers)
html = r.content.decode('utf-8')
soup = bs4.BeautifulSoup(html, 'lxml')
content = soup.find('ul', attrs={'id': 'reviewlist-wrapper'})
print(content)

