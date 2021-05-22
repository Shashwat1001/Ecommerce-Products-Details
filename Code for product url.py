#!/usr/bin/env python
# coding: utf-8

# In[26]:


import pandas as pd
import requests
import re
import numpy as np
from bs4 import BeautifulSoup
import requests
import urllib
from urllib.parse import urlparse
import time
from fake_useragent import UserAgent
from selenium import webdriver

class ExtractWebsiteData:
    def __init__(self):
        self.df = pd.DataFrame(columns = ['Product_Title','Product_Link'])

    def getData(self,keywords):
        keywords = keywords.lower()
        text = urllib.parse.quote_plus(keywords)
        options = webdriver.ChromeOptions()
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'}
        preferences= {"profile.default_content_settings.popups": 0,"directory_upgrade": True}
        options.add_experimental_option("prefs",preferences)
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36")
        # options.add_argument("--headless")
        #driver = webdriver.Chrome(ChromeDriverManager().install(), options= options)
        chrome = r'chromedriver_win32\chromedriver.exe'
        driver = webdriver.Chrome(chrome,chrome_options = options)
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6'}
        for x in range(1,100):
            try:
                listURLS = f'https://www.lazada.sg/catalog/?page={x}&q='+text
                # self.html =  requests.get(listURLS, headers=headers)
                driver.get(listURLS)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(10)
                self.soup = BeautifulSoup(driver.page_source, 'lxml')
                self.getProductDetails()
            except:
                break
        driver.quit()
        self.df.to_csv('task1.csv')
            
    def getProductDetails(self):
        results = self.soup.find_all('a')
        product=[]
        product_name = []
        for i in results:
            k = i.get('href')
            try:
                q = re.search('www.lazada.sg/products/',k)
                a,b =q.span()
                if q and i.text:
                    product.append([i.text,'https:'+k])
            except Exception as e:
                print(e)
                continue
        print(product)
        self.df = self.df.append(pd.DataFrame(product, 
               columns=[ 'Product_Title','Product_Link']),
               ignore_index = True)
        
                    
if __name__ == "__main__":
    obj = ExtractWebsiteData()
    obj.getData('mobile phones')


# In[ ]:




