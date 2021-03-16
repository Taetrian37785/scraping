from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import re, time
from webdriver_manager.chrome import ChromeDriverManager
def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser= Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    data = {
        'news_title': news_title,
        'news_p': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'hemisphere': hemisphere_image_urls(browser)
    }
    return data
def mars_news(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")
    # My tutor helped me condence my code from jupyter notebook into single lines as oppesed
    # to multiple commands.
    try:
        slide_element = news_soup.select_one("ul.item_list li.slide")
        latest_news_title = slide_element.find("div", class_="content_title").get_text()
        news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return latest_news_title, news_paragraph
def featured_image(browser):
    featured_image= "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/image/featured/mars3.jpg"
def mars_facts():
    try:
        # Reads off the table into an html format 
        mars_df = pd.read_html("https://space-facts.com/mars/")[0]
    except BaseException:
        return None
    mars_df.columns=["Description", "Value"]
    mars_df.set_index("Description", inplace=True)
    return mars_df.to_html(classes="table table-striped")
def hemisphere_image_urls(browser):
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    hemisphere_image_urls = []
    links = browser.find_by_css("a.product-item h3")
    # Pulls multiple images from the hemisphere site. 
    for item in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[item].click()
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        hemisphere["title"] = browser.find_by_css("h2.title").text
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    return hemisphere_image_urls
if __name__ == "__main__":
    print(scrape())