# Imports
from splinter import Browser
import pandas as pd
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Create Scrape function
def scrape():
    # Scrape the Mars News Site and assign text to variables.
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)
    news_html = browser.html
    news_soup = BeautifulSoup(news_html, "html.parser")
    news_title = news_soup.find("div", class_="content_title").text
    news_paragraph = news_soup.find("div", class_="article_teaser_body").text

    # Scrape the Space Image sight and save the image URL to a variable
    image_url = "https://spaceimages-mars.com"
    browser.visit(image_url)
    image_html = browser.html
    image_soup = BeautifulSoup(image_html, "html.parser")
    link_element = browser.links.find_by_partial_href("jpg").first
    featured_image_url = link_element["href"]

    # Convert Mars Facts to a table string using Pandas.
    facts_url = "https://galaxyfacts-mars.com"
    table_string = pd.read_html(facts_url,header=0)[0].to_html(classes = "table table-stripe table-light")

    # Create a dictionary with Mars's hemispheres
    hemi_url = "https://marshemispheres.com/"
    browser.visit(hemi_url)
    hemi_html = browser.html
    hemi_soup = BeautifulSoup(hemi_html, "html.parser")
    image = browser.find_by_tag("img")
    hemi_pics = []
    for i in range(3, len(image)):
        image[i].click()
        hemi_pic_link = browser.links.find_by_partial_text("Sample")["href"]
        hemi_title = browser.find_by_tag("h2").text
        hemi_title = hemi_title.split()
        hemi_title_modified = hemi_title[:-1]
        hemi_title_modified = " ".join(hemi_title_modified)
        hemi_pics.append({"title": hemi_title_modified, "img_url": hemi_pic_link})
        browser.back()
    
    scraping_data = {
        "News Title": news_title,
        "News Paragraph": news_paragraph,
        "Featured Image URL": featured_image_url,
        "Facts Table": table_string,
        "Hemispheres": hemi_pics
    }

    return scraping_data