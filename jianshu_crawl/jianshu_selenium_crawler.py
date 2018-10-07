# coding=utf-8
import html
import os
import time

from selenium import webdriver
import bs4
import mysql_test
import hashlib
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
# 导入selenium模块中的web引擎
from selenium import webdriver

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0'
}


def get_headers_driver():
    desire = DesiredCapabilities.PHANTOMJS.copy()
    for key, value in headers.items():
        desire['phantomjs.page.customHeaders.{}'.format(key)] = value
    driver = webdriver.PhantomJS(desired_capabilities=desire, service_args=['--load-images=yes'])  # 将yes改成no可以让浏览器不加载图片
    return driver


# 建立浏览器对象 ，通过Phantomjs
# browser = webdriver.PhantomJS()
browser_list = get_headers_driver()
browser_detail = get_headers_driver()

# 设置访问的url
MYDIR = os.path.dirname(__file__)
with open(os.path.join(MYDIR, 'urls.txt'), 'r') as f:
    urls = f.readlines()
length = len(urls)
for i in range(length):
    print(urls[i])

    # 访问url
    browser_list.get(urls[i])

    # for j in range(5000):  # 这里循环次数尽量大，保证加载到底
    #     ActionChains(browser_list).key_down(Keys.DOWN).perform()  # 相当于一直按着DOWN键
    #     print(f'已完成{j}次')

    for j in range(10):
        browser_list.execute_script('document.getElementsByClassName("note-list")[0].scrollTop=10000')  # 加载到底部，保证图片文章中的图片加载完
        time.sleep(1)
        print("Scrolling " + str(j) + "....")

    time.sleep(3)
    # 等待一定时间，让js脚本加载完毕
    browser_list.implicitly_wait(3)

    list_block = browser_list.find_elements_by_xpath("//ul[@class='note-list']")

    for item in list_block:
        print(item.id)
        print(item.text)
        print("")
        items = item.find_elements_by_xpath(".//li[starts-with(@class,'have-img')]")

        articles = []

        for item1 in items:
            article = {}
            title = item1.find_element_by_xpath(".//div[@class='content']//a")
            url = title.get_attribute("href")

            name = title.text

            summary = item1.find_element_by_xpath(".//div[@class='content']//p")

            article['title'] = name
            print("tile name:", name)
            article['summary'] = summary.text
            print("Summary:", summary.text)
            article['url'] = url
            print("link:", url)

            md5 = hashlib.md5()
            md5.update(url.encode("utf-8"))
            url_code = md5.hexdigest()
            article['url_code'] = url_code
            print("URL code :", url_code)

            if mysql_test.isDuplicatedUrlCode(url_code):
                print( name + ' link is already existed, continue to next one...')
                continue

            browser_detail.get(url)

            time.sleep(3)
            browser_detail.implicitly_wait(5)

            html_source = browser_detail.page_source
            soup = bs4.BeautifulSoup(html_source, 'lxml')

            if url.find("/p/") > 0:
                content_element = soup.find('div', class_="show-content")
            else:
                print("Links are not expected:", url)

            # 去掉img特殊的样式，影响页面显示
            for img_container in soup.findAll('div', class_="image-container"):
                img_container['style'] = ''
            for img_container in soup.findAll('div', class_="image-container-fill"):
                img_container['style'] = ''

            # 转义html特殊字符
            content = html.escape(str(content_element))
            # 特殊图片处理改为直接显示
            content = content.replace("data-original-src", "src")

            article['content'] = content
            print("Content :", content)
            if len(content) > 65000:
                print("Content exceed 65000, skip")
                continue

            article['img_url'] = ""
            article['author'] = ""
            article['create_user_id'] = '1'
            article['update_user_id'] = '1'

            articles.append(article)
            time.sleep(3)

        '''
        将爬到的小数写入数据库
        '''
        for article in articles:
            mysql_test.saveArticle2DB(article)

# Quit drivers
browser_detail.quit()
browser_list.quit()
