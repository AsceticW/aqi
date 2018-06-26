# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import csv

class AqiPipeline(object):
    def open_spider(self,spider):
        # 打开csv文件对象
        self.csv_file = open('aqi.csv','w')
        # 把csv对象定位写入对象
        self.csv_writer=csv.writer(self.csv_file)
        # 定义表头
        table_title = ["city_name", "date", "quality", "pm10", "no2", "co", "so2", "pm2_5", "AQI","source"]
        # 写入表头
        # 一次写入多行使用writerows
        self.csv_writer.writerow(table_title)

    def process_item(self, item, spider):
        item["source"] = spider.name
        item = dict(item)
        # 根据表头按顺序写入数据
        self.csv_writer.writerow((item["city_name"],item["date"],item["quality"],item["pm10"],item["no2"],item["co"],item["so2"],item["pm2_5"],item["AQI"],item["source"]))

        return item

    def close_spider(self,spider):
        self.csv_file.close()
