from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from time import sleep

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scraper():
    # scrape Mars news
    browser = init_browser()

    url_news = "https://mars.nasa.gov/news/"
    browser.visit(url_news)

    html = browser.html
    soup = bs(html, "html.parser")

    headline = soup.find("div", class_="content_title").text
    paragraph = soup.find("div", class_="article_teaser_body").text

    browser.quit()
    sleep(3)

    # scrape Mars space image
    browser = init_browser()

    url_image = "https://www.jpl.nasa.gov"
    url_image_path = "/spaceimages/?search=&category=Mars"
    browser.visit(url_image+url_image_path)

    image_html = browser.html
    image_soup = bs(image_html, "html.parser")

    image_element = image_soup.find("a", class_="button fancybox")
    element_image_path = image_element["data-fancybox-href"]
    featured_image_url = f'{url_image}{element_image_path}'

    browser.quit()
    sleep(3)

    # scrape Mars weather

    browser = init_browser()

    url_twitter = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_twitter)

    twitter_html = browser.html
    twitter_soup = bs(twitter_html, "html.parser")

    weather = twitter_soup.find("p", class_="TweetTextSize").text

    browser.quit()
    sleep(3)

    # scrape Mars facts

    browser = init_browser()

    facts_url = "https://space-facts.com/mars/"
    facts_tables = pd.read_html(facts_url)
    facts_df = facts_tables[1]
    facts_df.rename(columns={0: "description", 1: "value"}, inplace=True)
    facts_df.set_index(["description"], inplace=True)
    facts_html = facts_df.to_html(classes="dataframe table-responsive table-striped table-bordered")

    browser.quit()
    sleep(3)

    # scrape hemispheres

    browser = init_browser()

    url_hemi = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemi)

    hemi_html = browser.html
    hemi_soup = bs(hemi_html, "html.parser")

    items = hemi_soup.find_all("div", class_="item")

    hemisphere_results = []
    hemisphere_url_main = "https://astrogeology.usgs.gov"

    for i in items:

        # scrape title
        title = i.find("h3").text
        # scrape link to visit site of the hemishere image
        hemisphere_url_partial = i.find(
            "a", class_="itemLink product-item")["href"]
        # visit link to scrape hemispher image
        browser.visit(hemisphere_url_main + hemisphere_url_partial)

        individual_image_html = browser.html
        individual_soup = bs(individual_image_html, "html.parser")

        # scrape image src
        img_url = hemisphere_url_main + \
            individual_soup.find("img", class_="wide-image")["src"]

        # append scraped results to list
        hemisphere_results.append({"title": title, "img_url": img_url})

    browser.quit()
    sleep(4)

    scraped_data = {
        "news_title": headline,
        "news_p": paragraph,
        "featured_image": featured_image_url,
        "weather": weather,
        "facts": facts_html,
        "hemispheres": hemisphere_results
    }

    return scraped_data
