import requests
import pymongo
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from selenium import webdriver

def init_browser():
    executable_path = {"executable_path":"C:/Users/Melissa/Anaconda3/envs/PythonData/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_data = {}
    hemisphere_image_urls = []
    
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    #print(soup.prettify)
    #content_title
    #rollover_description_inner
    
    #News Pull
    results = soup.find("div", class_="content_title")
    news_title = results.find("a").get_text()
    p = soup.find("div", class_="rollover_description_inner")
    news_p = p.get_text()

    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p
    
    #Image Pull
    feat_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    feat_response = requests.get(feat_url, "html.parser")
    feat_soup = bs(feat_response.text, "html.parser")
    #print(feat_soup.prettify)
    #carousel_items
    #article
    #style

    feat_results = feat_soup .find("div", class_="carousel_items")
    bg_url = feat_results.article["style"]
    base_url = "https://www.jpl.nasa.gov"

    #str.split(separator, maxsplit)
    split_bg_url = bg_url.split('/',1)[1].split("'",1)[0]

    featured_image_url= base_url + "/" + split_bg_url
    #print(split_bg_url)
    #print(base_url)
    #print(featured_image_url)
    
    mars_data["featured_image_url"] = featured_image_url

    #Tweet Pull 
    weather_url = "https://twitter.com/marswxreport?lang=en"
    weather_response = requests.get(weather_url)
    weather_soup = bs(weather_response.text, "html.parser")
    #print(weather_soup.prettify())
    #p
    #"TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"

    mars_weather = weather_soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    #print(mars_weather)
    #temp

    mars_data["mars_weather"] = mars_weather

    #Table Pull
    mars_facts_url = "https://space-facts.com/mars/"
    mars_table = pd.read_html(mars_facts_url)
    #mars_table
    mars_df = mars_table[0]
    mars_df.columns = ["Fields", "Values"]
    mars_df

    mars_data["mars_facts"] = mars_df

    #Multi-Image Pull
    hemisphere_image_urls= [
        {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
        {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
    ]

    mars_data["mars_hemisphere"] = hemisphere_image_urls

    browser.quit()

    return mars_data

