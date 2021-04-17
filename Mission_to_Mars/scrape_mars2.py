#!/usr/bin/env python
# coding: utf-8

# In[107]:


import os
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time 

# In[94]:

def scrape_info():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[95]:


    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)


    # In[96]:



    html = browser.html
    soup = bs(html, 'html.parser')


    # In[81]:





    # In[99]:


    # -- LATEST NEWS ABOUT MARS -- #

    results = soup.find_all("li", class_="slide")

    result = results[0] 
        
    news_title = result.find("div", class_= "content_title").text
        
    news_teaser = result.find("div", class_= "article_teaser_body").text
        

    print('-----------------')
    print(news_title)
    print('-----------------')
    print(news_teaser)
        
            
            
        


    # In[101]:


    new_url = 'https://spaceimages-mars.com/'
    browser.visit(new_url)


    # In[102]:


    browser.links.find_by_partial_text('FULL IMAGE').click()


    # In[103]:


    html = browser.html
    soup = bs(html, 'html.parser')


    # In[105]:


    featured_image_url = soup.find("img", class_= "fancybox-image").get("src")
    print(featured_image_url)


    # In[106]:


    # -- FEATURED IMAGE -- #
    featured_image_url = f'http://spaceimages-mars.com/{featured_image_url}'
    print(featured_image_url)


    # In[ ]:





    # In[145]:


    # -- MARS FACTS -- # 

    url = 'https://space-facts.com/mars/'
    df = pd.read_html(url)[0]
    df = df.rename(columns ={0:" Description", 1: "Mars "})
    df = df.to_html(classes= "table table-striped")


    # In[146]:


    new_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(new_url)


    # In[147]:


    titles = browser.links.find_by_partial_text('Hemisphere Enhanced')


    # In[148]:


    # -- MARS HEMISPHERES -- # 

    hemisphere_image_urls = []

    for i in range(len(titles)): 
        image_titles = {}
        browser.links.find_by_partial_text('Hemisphere Enhanced')[i].click()
        
        html = browser.html
        soup = bs(html, 'html.parser')
        
        downloads = soup.find("div", class_="downloads")
        sample_image = downloads.find_all("a")[0]["href"]
        #print(sample_image)
        
        image_titles["img_url"] = sample_image
        titles = soup.find("h2", class_= "title").text
        #print(titles)
        
        image_titles["titles"] = titles
        
        hemisphere_image_urls.append(image_titles)
        
        browser.back()
        
    print(hemisphere_image_urls)
        


    # In[ ]:

    mongo_data = { 
        "news_title" : news_title, 
        "news_paragraph": news_teaser, 
        "featured_image" : featured_image_url, 
        "mars_facts" : df, 
        "hemispheres" : hemisphere_image_urls

    }

    return mongo_data


