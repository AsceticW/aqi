# -*- coding: utf-8 -*-
import re

import scrapy
from aqi.items import AqiItem

class AqiCitySpider(scrapy.Spider):
    name = 'aqi_city'
    allowed_domains = ['aqistudy.cn']
    start_urls = ['https://www.aqistudy.cn/historydata/']

    def parse(self, response):
        citys = response.xpath('//div[@class = "all"]//a')[3:6]

        for city in citys:
            city_url = 'https://www.aqistudy.cn/historydata/' + city.xpath('./@href').extract_first()
            yield scrapy.Request(city_url,callback=self.parse_month)

    def parse_month(self,response):
        months = response.xpath('//tbody/tr')[3:8]
        if len(months)>1:
            months=months[1:]


            for month in months:
                month_url ='https://www.aqistudy.cn/historydata/'+ month.xpath('./td[1]/a/@href').extract_first()

                yield scrapy.Request(month_url,callback=self.parse_detail)

    def parse_detail(self,response):

        days = response.xpath('//tbody/tr')
        if len(days)>1:
            days = days[1:]
            for day in days:
                item = AqiItem()
                item["city_name"] = re.findall('月(.*?)空气质量',response.body.decode(),re.S)[0]
                item["date"] = day.xpath('./td[1]/text()').extract_first()
                item["AQI"] = day.xpath('./td[2]/text()').extract_first()
                item["quality"] = day.xpath('./td[3]/span/text()').extract_first()
                item["pm2_5"] = day.xpath('./td[4]/text()').extract_first()
                item["pm10"] = day.xpath('./td[5]/text()').extract_first()
                item["so2"] = day.xpath('./td[6]/text()').extract_first()
                item["co"] = day.xpath('./td[7]/text()').extract_first()
                item["no2"] = day.xpath('./td[8]/text()').extract_first()
                print(item)
                yield item
            