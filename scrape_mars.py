import time
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
from selenium import webdriver
import pymongo
import re

def init_browser():
    executable_path = {"executable_path": "/Users/mulrich/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)

def scrape():
    browser = init_browser()
    mars_data_scrape = {}


    mars_news = 'https://mars.nasa.gov/news/'
    browser.visit(mars_news)
    time.sleep(2)
    html = browser.html
    news_soup = bs(html, 'html.parser')

    news_title = news_soup.find('div', class_='content_title').get_text()
    news_p = news_soup.find('div', class_='article_teaser_body').get_text()
    time.sleep(2)

    mars_data_scrape["data1"] = news_title
    mars_data_scrape["data2"] = news_p

    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    time.sleep(2)
    browser.click_link_by_partial_text('.jpg')


    html = browser.html
    jpl_soup = bs(html, 'html.parser')

    featured_img_url = jpl_soup.find('img').get('src')

    mars_data_scrape["image"] = featured_img_url



    weather_url = 'https://twitter.com/marswxreport?lang=en'
    html = requests.get(weather_url)
    weather_soup = bs(html.text, 'html.parser')

    mars_weather = weather_soup.find_all(string=re.compile("Sol"), class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")[0].text

    mars_data_scrape["weather"] = mars_weather



    mars_facts_url = 'https://space-facts.com/mars/'
    table_df = pd.read_html(mars_facts_url)[0]
    table_df.columns = ["description", "value"]
    table_df = table_df.set_index('description', drop=True)
    mars_data_scrape["table"] = table_df.to_html()



    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hem_url)

    html = browser.html
    hem_soup = bs(html, 'html.parser')



    hem_img_urls = []
    hem_dict = {'title': [], 'img_url': [],}

    x = hem_soup.find_all('h3')


    for i in x:
        t = i.get_text()
        title = t.strip('Enhanced')
        browser.click_link_by_partial_text(t)
        hem_url = browser.find_link_by_partial_href('download')['href']
        hem_dict = {'title': title, 'img_url': hem_url}
        hem_img_urls.append(hem_dict)
        browser.back()

    mars_data_scrape["hemispheres"] = hem_img_urls
    

    return mars_data_scrape
