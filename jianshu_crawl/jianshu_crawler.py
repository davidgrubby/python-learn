import requests
import bs4

headers = {
    # ':authority': 'www.zhihu.com',
    # ':method': 'GET',
    # ':path': '/search?type=content&q=%E7%A9%BF%E6%90%AD',
    # ':scheme': 'https',
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 'accept-encoding': 'gzip, deflate, br',
    # 'accept-language': 'en-US,en;q=0.9',
    # 'cache-control': 'max-age=0',
    # 'cookie': '_xsrf=Goj2PtgOcj3bXKnqrSYT4UHNF4qWnq8N; _zap=7a5d853e-25a1-41f4-89dd-2bcca6dfe561; d_c0="AEDkPvjZUA6PTrWy61VBH6ycjTTkOSy2_0c=|1538724017"; capsion_ticket="2|1:0|10:1538738621|14:capsion_ticket|44:YTcxMTA1NTM0OGNmNDIwMjg2MzY5YmQzODkwZjA5ZmI=|5a975e8a0713e202bf82de5f532eb6c583aea6847ff35a76769f338c182d91d5"; z_c0="2|1:0|10:1538738758|4:z_c0|92:Mi4xSDBtS0F3QUFBQUFBUU9RLS1ObFFEaVlBQUFCZ0FsVk5ScGlrWEFDOHQ2ZlFMYnB6ZEZtODdoM1JoSWxPY0JJQWVB|6680b3840ce7473cd9f1fad0d139eebf081746399717bab9556591d194cfd738"; q_c1=b9eb3c565c054503bfdb0f540360e244|1538738760000|1538738760000; __utma=51854390.819492989.1538738922.1538738922.1538738922.1; __utmc=51854390; __utmz=51854390.1538738922.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.100--|2=registration_date=20161007=1^3=entry_date=20161007=1; tst=f; tgw_l7_route=8605c5a961285724a313ad9c1bbbc186',
    # 'referer': 'https://www.zhihu.com/search?type=content&q=%E7%BE%8E%E9%A3%9F',
    # 'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0'
}

url = 'https://www.jianshu.com/p/30c5a6e59633'

r = requests.get(url, headers=headers)

# print(r.headers)
# r.encoding=r.apparent_encoding
html = r.content
soup = bs4.BeautifulSoup(html, 'lxml')
content = soup.find('div', attrs={'class': 'show-content'})
print(content)
