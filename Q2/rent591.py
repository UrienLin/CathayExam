import pandas as pd
import requests as req
import scrapy 

import time

from selenium import webdriver
class rentSpider(scrapy.Spider):
    name = "rent591"
    start_urls = ['https://rent.591.com.tw/?kind=0&region=1&order=posttime&orderType=desc']

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome('chromedriver',options=options)
        self.region_dict = {'新北市': '3', '台北市': '1'}

    def next_page(self,bool_gonext):
        btn_next_page = self.driver.find_element_by_css_selector('div.pageBar a.pageNext')
        href_next_page = self.driver.find_element_by_css_selector('div.pageBar a.pageNext').get_attribute('href')
        bool_next_page = (href_next_page == None)
        if (bool_next_page & bool_gonext):
            self.driver.execute_script("arguments[0].click();", btn_next_page)
            time.sleep(3)
            print('Loading Next Page ... ')
        
        current_page = self.driver.find_element_by_css_selector('div.pageBar span.pageCurrent')\
                             .get_attribute('innerText')
        return int(current_page), bool_next_page

    def extract_articles(self):
        ids =[x.get_attribute('data-bind') for x in  self.driver.find_elements_by_css_selector('ul.listInfo img')]
        titles =[x.get_attribute('title') for x in  self.driver.find_elements_by_css_selector('ul.listInfo img')]
        links =[x.get_attribute('href') for x in  self.driver.find_elements_by_css_selector('ul.listInfo h3 a')]
        _df = pd.DataFrame([ids,titles,links]).T
        _df.columns = ['id','title', 'link']
        return _df

    def switch_region(self,region_code):
        region_switch = self.driver.find_element_by_css_selector('span.search-location-span')
        self.driver.execute_script("arguments[0].click();", region_switch)
        btn_region = self.driver.find_element_by_css_selector('ul li.city-li a[data-id="{}"]'.format(region_code))
        print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&',btn_region.get_attribute('innerText'))
        self.driver.execute_script("arguments[0].click();", btn_region)
        self.driver.refresh()
        time.sleep(3)
        print('current url : {}'.format(self.driver.current_url))

    def parse(self, response):
        all_df = pd.DataFrame()
        self.driver.get(response.url)
        #Region Could Be Different
        current_url = self.driver.current_url
        current_region = current_url.split('=')[-1]
        #Start from Taipei (consider about pipitem later)
        if(current_region not in self.region_dict.values()):
            #if region went somewhere else. make it start from taipei
            self.switch_region(self.region_dict['台北市'] )
        int_current_page, bool_next_page = self.next_page(False) 
        while True:
            all_df = pd.concat([all_df,self.extract_articles()])
            int_current_page, bool_next_page = self.next_page(True)
            print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',int_current_page,bool_next_page)
            if(int_current_page % 3 == 0):
                all_df.to_csv('test1page.csv', index=False, encoding='utf-8')

            if(int_current_page>11):
                break





