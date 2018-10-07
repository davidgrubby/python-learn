# -*- coding: utf-8 -*-
import scrapy

from weather.items import WeatherItem


class SztianqiSpider(scrapy.Spider):
    name = 'SZtianqi'
    allowed_domains = ['suzhou.tianqi.com']
    start_urls = []

    citys = ['nanjing', 'suzhou', 'shanghai']

    for city in citys:
        start_urls.append('http://www.tianqi.com/' + city)

    def parse(self, response):
        items = []
        sixday = response.xpath('//div[@class="week"]')

        for day in sixday:
            item = WeatherItem()

            date = ''
            for datetitle in day.xpath('./h3//text()').extract():
                date += datetitle

            item['date'] = date

            item['week'] = day.xpath('./p//text()').extract()[0]
            item['img'] = day.xpath(
                './ul/li[@class="tqpng"]/img/@src').extract()[0]
            tq = day.xpath('./ul/li[2]//text()').extract()
            # 我们用第二种取巧的方式，将tq里找到的str连接
            item['temperature'] = ''.join(tq)
            item['weather'] = day.xpath('./ul/li[3]/text()').extract()[0]
            item['wind'] = day.xpath('./ul/li[4]/text()').extract()[0]
            items.append(item)
        return items


