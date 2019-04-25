# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd

# Function to scrape mission to mars data
def scrape_sites():

    # Define path for chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # NASA Mars News Site url
    nasa_url = 'https://mars.nasa.gov/news'

    # Get NASA url
    nasa_response = requests.get(nasa_url)

    # Create BeautifulSoup object to parse with 'html.parser'
    nasa_soup = BeautifulSoup(nasa_response.text, 'html.parser')

    # Nasa's Mars Latest News
    news_title = nasa_soup.find('div', class_="content_title").text
    news_p = nasa_soup.find('div', class_="rollover_description_inner").text
    
    # JPL Mars Space Featured Image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    html = browser.html
    jpl_soup = BeautifulSoup(html, 'html.parser')

    image_url = jpl_soup.find('article')['style'].split(":")[1].split("'")[1]
    featured_image_url = jpl_url[0:24] + image_url
    
    # Mars Weather
    mars_twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_twitter_url)
    html = browser.html
    mars_twitter_soup = BeautifulSoup(html, 'html.parser')

    # Mars Weather Tweet
    mars_weather = mars_twitter_soup.find('p', class_="TweetTextSize").text
   
    # # Facts table from Mars 'Facts' url
    mars_facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_facts_url)
    
    # Converting to DataFrame
    mars_df = tables[0]
    mars_df.columns = ['Description', 'Value']
    mars_df

    # Convert mars_df to html table and save to mars_table.html file
    mars_html_table = mars_df.to_html(index=False, classes='table-condensed table-striped', table_id="mars_table")

    # Hemisphere_image_urls
    hemisphere_image_urls = [
        {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
        {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},    
    ]

    # Add all scraped elements to one dictionary
    mars_dict = {"news_title": news_title,
                       "news_p": news_p,
                       "featured_image_url": featured_image_url,
                       "mars_weather": mars_weather,
                       "mars_facts": mars_html_table,
                       "hemisphere_image_urls": hemisphere_image_urls,                   
                        
                        }

    return mars_dict