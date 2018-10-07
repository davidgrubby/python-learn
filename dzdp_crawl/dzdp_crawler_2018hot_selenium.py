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

url_hot = "https://m.dianping.com/musteatlist/ranklist?notitlebar=1&shark=1&type=2&cityid=1"


# 获取列表页面
# 获取2018必吃棒
def get_headers_driver():
    desire = DesiredCapabilities.PHANTOMJS.copy()
    for key, value in headers.items():
        desire['phantomjs.page.customHeaders.{}'.format(key)] = value
    driver = webdriver.PhantomJS(desired_capabilities=desire, service_args=['--load-images=yes'])  # 将yes改成no可以让浏览器不加载图片
    return driver


# 建立浏览器对象 ，通过Phantomjs
# browser = webdriver.PhantomJS()
browser_list = get_headers_driver()
browser_list.get(url_hot)

for i in range(10):
    browser_list.execute_script('document.getElementsByClassName("wrap2")[0].scrollTop=10000')  # 加载到底部，保证图片文章中的图片加载完
    time.sleep(1)
    print("Sleeping " + str(i) + " time")


time.sleep(10)
# 等待一定时间，让js脚本加载完毕
browser_list.implicitly_wait(10)

html = browser_list.page_source
soup = bs4.BeautifulSoup(html, 'lxml')
content = soup.findAll('div', attrs={'class': 'card'})
print(content)
