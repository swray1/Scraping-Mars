from splinter import Browser
import pandas as pd


def init_browser():
    exec_path = {'executable_path': '/Users/stephenwray/Desktop/chromedriver'}
    return Browser('chrome', **exec_path, headless=True)


def scrape():

    mars_data = {}

    browser = init_browser()
    browser.visit('https://mars.nasa.gov/news/')
    news_title = browser.find_by_css('.content_title').first.text
    news_p = browser.find_by_css('.article_teaser_body').first.text

    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p

    browser = init_browser()
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    browser.find_by_id('full_image').click()
    featured_image_url = browser.find_by_css('.fancybox-image').first['src']

    mars_data['featured_image_url'] = featured_image_url

    browser = init_browser()
    browser.visit('https://twitter.com/marswxreport?lang=en')
    for tweet in browser.find_by_css('.tweet-text'):
        if tweet.text.startswith('Sol'):
            mars_weather = tweet.text

    mars_data['mars_weather'] = mars_weather

    df = pd.read_html('http://space-facts.com/mars/', attrs={'id': 'tablepress-mars'})[0]
    df = df.set_index(0)
    df = df.rename(columns={1: "Value"})
    del df.index.name
    mars_facts = df.to_html()
    
    mars_data['mars_facts'] = mars_facts


    browser = init_browser()
    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')

    titles = []

    for i in range(4):
        titles.append(browser.find_by_tag('h3')[i].text)

    imgs = []

    for x in range(4):
        browser.find_by_css(".thumb")[x].click()
        imgs.append(browser.find_by_text("Sample")["href"])
        browser.back()

    hemisphere_image_urls = [
        {'title': titles[0], 'img_url': imgs[0]},
        {'title': titles[1], 'img_url': imgs[1]},
        {'title': titles[2], 'img_url': imgs[2]},
        {'title': titles[3], 'img_url': imgs[3]}
    ]

    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_data
