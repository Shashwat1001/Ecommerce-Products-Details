#!/usr/bin/env python
# coding: utf-8

# In[56]:


from bs4 import BeautifulSoup
import requests
import urllib
import pandas as pd
import numpy as np
import re
from urllib.parse import urlparse
from selenium import webdriver
from fake_useragent import UserAgent

class ExtractWebsiteData:
    def __init__(self):
        self.df = pd.DataFrame(columns = ['Product URL','Product Title','Brand',
                                     'Promo Price','List Price','Warranty',
                                     'Color Variation','Size Variation',
                                     'Stock details','Seller Name',
                                     'Seller rating','Site SKU code',
                                     'Specification','Product rating',
                                     'Product reviews'])

    def getData(self,url):
        
        book2 = pd.read_csv('task1.csv')
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6'}
        #self.html =  requests.get(url, headers=headers)
        options = webdriver.ChromeOptions()
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'}
        preferences= {"profile.default_content_settings.popups": 0,"directory_upgrade": True}
        options.add_experimental_option("prefs",preferences)
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36")
        # options.add_argument("--headless")
        #driver = webdriver.Chrome(ChromeDriverManager().install(), options= options)
        chrome = r'chromedriver_win32\chromedriver.exe'
        driver = webdriver.Chrome(chrome,chrome_options = options)
        driver.get(url)
        driver.implicitly_wait(15)
        self.soup = BeautifulSoup(driver.page_source, 'lxml')
        html_txt = driver.page_source
        self.getProductDetails(url,html_txt)
        driver.quit()
        self.df.to_csv('task2.csv')
    def getDetailUtil(self, tag, className):
        try:
            x = self.soup.find_all(tag, class_ = className)[0]
            x = x.text

            return x
        except Exception as e:
            print(e)
            return "NULL"

    def getSizes(self):
        parentdiv = self.soup.find_all('span', class_= "sku-variable-name-text")
        # print(parentdiv)
        # children = parentdiv.find_all('span',recursive=False, class_="sku-variable-name-text")
        sizes = []
        # print(children)
        for child in parentdiv:
            sizes.append(child.text)

        return ";".join(sizes)

    def getProductDetails(self,url,html_txt):
        
        
        # getting product name 
        product_name = self.getDetailUtil('h1','pdp-mod-product-badge-title')


        # getting brand name 
        brand_name = self.getDetailUtil('a',"pdp-link pdp-link_size_s pdp-link_theme_blue pdp-product-brand__brand-link")


        # getting promo price 
        promo_price = self.getDetailUtil('span','pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl')


        # getting list price
        list_price = self.getDetailUtil('span', 'pdp-price pdp-price_type_deleted pdp-price_color_lightgray pdp-price_size_xs')



        # warranty_detail = self.getDetailUtil('div','delivery-option-item__title')
        # print(warranty_detail)
        # getting warranty detail
        try:
            warranty_detail = self.soup.find_all("div", class_ = "delivery-option-item__title")[-1]
            warranty_detail = warranty_detail.text
        except Exception as e:
            print(e)
            warranty_detail="NULL"

        # getting color and size variant 
        # issue 

        # getting size variant
        sizes = self.getSizes()



        # getting stock detail
        stock_detail = self.getDetailUtil('span','quantity-content-default')


        # getting seller name
        seller_name = self.getDetailUtil('a','pdp-link pdp-link_size_l pdp-link_theme_black seller-name__detail-name')


        # getting seller rating 
        seller_rating = self.getDetailUtil('div','seller-info-value rating-positive')


        # getting sku code
        try:
            x = re.search('"sku":"', html_txt)
            a,b= x.span()
            y = re.search('","mpn":', html_txt)
            c,d = y.span()
            sku_code=html_txt[b:c]
        except Exception as e:
            print(e)
            sku_code="NULL" 

        # getting product rating
        try:
            prod_rating = self.getDetailUtil('div','score')
            z=re.search('"rating":{"score":',html_txt)
            o,h = z.span()
            q=re.search(',"total"',html_txt)
            f,g = q.span()
            prod_rating=html_txt[h:f]
        except Exception as e:
            print(e)
            prod_rating="NULL" 

        # check 
        parentdiv = self.soup.find_all('div', class_= "html-content pdp-product-highlights")
        #specification
        try:
            parentdiv = self.soup.find_all('div', class_= "html-content pdp-product-highlights")[0]
            children = parentdiv.find_all('li')
            specs = []
            for child in children:
                specs.append(child.text)
            specification = " ".join(specs)
        except Exception as e:
            print(e)
            specification = 'NULL'


        # getting product reviews
        prod_reviews = self.getDetailUtil('a','pdp-link pdp-link_size_s pdp-link_theme_blue pdp-review-summary__link')
        self.df=self.df.append({'Product URL':url,'Product Title':product_name,'Brand':brand_name,
                                 'Promo Price':promo_price,'List Price':list_price,'Warranty':warranty_detail,
                                 'Color Variation':'NAN','Size Variation':sizes,
                                 'Stock details':stock_detail,'Seller Name':seller_name,
                                 'Seller rating':seller_rating,'Site SKU code':sku_code,
                                 'Specification':specification,'Product rating':prod_rating,
                                 'Product reviews':prod_reviews},ignore_index = True)
        
        




if __name__ == "__main__":
    obj = ExtractWebsiteData()
    url='https://www.lazada.sg/products/smallst-flip-cellphone-ulcool-f1-32mb32mb-mtk6261-gsm-300mah-bluetooth-mini-backup-pocket-portable-mobile-phone-gift-for-kid-i1088422896-s4195686653.html?search=1'
    obj.getData(url)


# In[ ]:




