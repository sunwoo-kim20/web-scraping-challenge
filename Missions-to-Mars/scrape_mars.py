# Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs

from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


# Scrape Function
def mars_scrape():
    # Set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ## News Scrape

    # Visit news webpage and scrape the page
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the news
    news = soup.find('div', id = 'news')

    news_title = news.find_all('div', class_='content_title')[0].text
    news_teaser = news.find_all('div', class_='article_teaser_body')[0].text

    ## Space Image Scrape

    # Visit webpage and scrape the page
    space_img_url = "https://spaceimages-mars.com/"
    browser.visit(space_img_url)
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the image
    space_img = soup.find('a', class_='showimg')

    featured_image_url = f"{url}{space_img['href']}"

    ## Table Scrape

    # Get tabular data from webpage
    table_url = "https://galaxyfacts-mars.com/"
    tables = pd.read_html(table_url)

    # Convert table to a datframe
    mars_df = tables[0]

    # Reformat dataframe
    clean_mars_df = mars_df.rename(columns= {0: 'Mars-Earth Comparisons', 1: 'Mars', 2:'Earth'})
    clean_mars_df = clean_mars_df.drop(0, axis = 0)
    clean_mars_df.set_index('Mars-Earth Comparisons', inplace = True)

    # Convert dataframe to an HTML string
    mars_html_table = clean_mars_df.to_html()

    ## Hemisphere scrape

    # Create url strings
    base_url = 'https://marshemispheres.com/'
    hemi_urls = [
        'cerberus.html',
        'schiaparelli.html',
        'syrtis.html',
        'valles.html'
        ]

    # Loop through hemisphere list and scrape images and titles
    img_urls = []
    hemi_titles = []

    for url_extension in hemi_urls:

        # Visit webpage and scrape the page
        browser.visit(base_url+url_extension)
        html = browser.html
        soup = bs(html, "html.parser")

        # Get the image
        downloads = soup.find('div', class_ = 'downloads')
        img_url = downloads.find_all('a')[0]['href']

        full_img_url = f"{base_url}{img_url}"

        img_urls.append(full_img_url)

        # Get the title
        cover = soup.find('div', class_ = 'cover')
        title = cover.h2.text.replace(' Enhanced', '')
        hemi_titles.append(title)

    # Close browser
    browser.quit()

    # Create list of dictionaries to hold titles and urls
    hemi_img_urls = []
    for i in range(len(img_urls)):
        hemi_dict = {'title': hemi_titles[i], 'img_url': img_urls[i]}
        hemi_img_urls.append(hemi_dict)

    # Create output dictionary containing all scraped data
    mars_output_dict = {
        "news_title" : news_title,
        "news_teaser" : news_teaser,
        "featured_image_url" : featured_image_url,
        "table_html" : mars_html_table,
        "hemisphere_images" : hemi_img_urls
    }

    return mars_output_dict
