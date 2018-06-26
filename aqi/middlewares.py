# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import time
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class Aqi_Selenium_Middleware(object):
    def __init__(self):
        # 有界面
        self.driver = webdriver.Chrome()
        # 无界面
        # self.options = Options()
        # self.options.set_headless()
        # self.driver = webdriver.Chrome(options = self.options)

    def process_request(self,spider,request):
        if 'monthdata' in request.url or 'daydata' in request.url:

            self.driver.get(request.url)
            try:
                # 如果不写0.3，默认0.5,3秒内每次相隔0.3检查是否满足条件，满足则跳出等待，超过3秒则报错
                element = WebDriverWait(self.driver,3,0.3).until(EC.text_to_be_present_in_element((By.XPATH, '//td[position()=1]'),'-'))
                html = self.driver.page_source
                return HtmlResponse(url=self.driver.current_url,
                                    body=html.encode("utf-8"),
                                    encoding='utf-8',
                                    request=request)
            except:
                
                logging.error("该地址没有信息：%s" % request.url)

    def __del__(self):
        self.driver.quit()
