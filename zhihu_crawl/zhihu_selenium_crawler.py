# coding=utf-8
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
    # ':authority': 'www.zhihu.com',
    # ':method': 'GET',
    # ':path': '/search?type=content&q=%E7%A9%BF%E6%90%AD',
    # ':scheme': 'https',
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 'accept-encoding': 'gzip, deflate, br',
    # 'accept-language': 'en-US,en;q=0.9',
    # 'cache-control': 'max-age=0',
    'cookie': '_xsrf=Goj2PtgOcj3bXKnqrSYT4UHNF4qWnq8N; _zap=7a5d853e-25a1-41f4-89dd-2bcca6dfe561; d_c0="AEDkPvjZUA6PTrWy61VBH6ycjTTkOSy2_0c=|1538724017"; capsion_ticket="2|1:0|10:1538738621|14:capsion_ticket|44:YTcxMTA1NTM0OGNmNDIwMjg2MzY5YmQzODkwZjA5ZmI=|5a975e8a0713e202bf82de5f532eb6c583aea6847ff35a76769f338c182d91d5"; z_c0="2|1:0|10:1538738758|4:z_c0|92:Mi4xSDBtS0F3QUFBQUFBUU9RLS1ObFFEaVlBQUFCZ0FsVk5ScGlrWEFDOHQ2ZlFMYnB6ZEZtODdoM1JoSWxPY0JJQWVB|6680b3840ce7473cd9f1fad0d139eebf081746399717bab9556591d194cfd738"; q_c1=b9eb3c565c054503bfdb0f540360e244|1538738760000|1538738760000; __utma=51854390.819492989.1538738922.1538738922.1538738922.1; __utmc=51854390; __utmz=51854390.1538738922.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.100--|2=registration_date=20161007=1^3=entry_date=20161007=1; tst=f; tgw_l7_route=8605c5a961285724a313ad9c1bbbc186',
    'referer': 'https://www.zhihu.com/search?type=content&q=%E7%BE%8E%E9%A3%9F',
    'upgrade-insecure-requests': '1',
    'Content-Type': 'text/html; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
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
    browser_list.execute_script('window.scrollTo(0, document.body.scrollHeight)')  # 加载到底部，保证图片文章中的图片加载完
    time.sleep(3)
    for j in range(5000):  # 这里循环次数尽量大，保证加载到底
        ActionChains(browser_list).key_down(Keys.DOWN).perform()  # 相当于一直按着DOWN键
        print(f'已完成{j}次')

    time.sleep(3)
    # 等待一定时间，让js脚本加载完毕
    browser_list.implicitly_wait(3)

    list_block = browser_list.find_elements_by_xpath("//div[@class='Card']")

    for item in list_block:
        print(item.id)
        print(item.text)
        print("")
        items = item.find_elements_by_xpath(".//div[starts-with(@class,'List-item')]")

        articles = []

        for item1 in items:
            article = {}
            title = item1.find_element_by_xpath(".//h2[@class='ContentItem-title']//a")
            url = title.get_attribute("href")

            name = title.text

            summary = item1.find_element_by_xpath(".//div[@class='RichContent-inner']//span")

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
            browser_detail.implicitly_wait(5)
            # content = browser.find_element_by_xpath("//div[@class='QuestionAnswer-content'|
            # @class='Post-Main Post-NormalMain']")
            html = browser_detail.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

            soup = bs4.BeautifulSoup(html, 'lxml')

            if url.find("/question/") > 0:
                content = soup.find('span', attrs={'class': 'RichText ztext CopyrightRichText-richText'}).text.strip()
            elif url.find("/p/") > 0:
                content = soup.find('div', attrs={'class': 'RichText ztext Post-RichText'}).text.strip()
            else:
                print("Links are not expected:", url)

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
