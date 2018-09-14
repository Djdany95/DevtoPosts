import time
import urllib.request
import json
from platform import system
from selenium import webdriver
from bs4 import BeautifulSoup


url = 'https://dev.to'


def checkLastPost(user):
    """"""
    user_url = url + '/' + user
    web = urllib.request.urlopen(user_url)

    soup = BeautifulSoup(web, 'html.parser')

    last_post = soup.find('h3')
    last_post = last_post.text.strip()

    return last_post


def infiniteScroll(user):
    """"""
    user_url = url + '/' + user

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver_path = './chromedriver.exe' if system() == 'Windows' else './chromedriver'

    browser = webdriver.Chrome(
        executable_path=driver_path, chrome_options=options)

    # Tell Selenium to get the URL you're interested in.
    browser.get(user_url)

    # Selenium script to scroll to the bottom, wait 1 second for the next batch of data to load, then continue scrolling.  It will continue to do this until the page stops loading new data.
    lenOfPage = browser.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False
    while(match == False):
        lastCount = lenOfPage
        time.sleep(1)
        lenOfPage = browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount == lenOfPage:
            match = True

    # Now that the page is fully scrolled, grab the source code.
    source_data = browser.page_source

    return source_data


def getPosts(user):
    """"""
    web = infiniteScroll(user)

    soup = BeautifulSoup(web, 'html.parser')

    find_posts = soup.find_all('div', attrs={'class': 'single-article'})

    posts_h3 = filter(lambda x: x is not None,
                      map(lambda x: x.find('h3'), find_posts))
    posts_names = list(map(
        lambda x: x.text.strip(), posts_h3))

    posts_a = filter(lambda x: x is not None, map(
        lambda x: x.find('a', attrs={'class': 'index-article-link'}), find_posts))
    posts_urls = list(map(lambda x: url+x['href'], posts_a))

    nPosts = list(range(len(posts_names), 0, -1))

    response = create_json(nPosts, posts_names, posts_urls)

    return response


def getLastPosts(user):
    """"""
    user_url = url + '/' + user
    web = urllib.request.urlopen(user_url)

    soup = BeautifulSoup(web, 'html.parser')

    find_posts = soup.find_all('div', attrs={'class': 'single-article'})

    posts_h3 = filter(lambda x: x is not None,
                      map(lambda x: x.find('h3'), find_posts))
    posts_names = list(map(
        lambda x: x.text.strip(), posts_h3))

    posts_a = filter(lambda x: x is not None, map(
        lambda x: x.find('a', attrs={'class': 'index-article-link'}), find_posts))
    posts_urls = list(map(lambda x: url+x['href'], posts_a))

    nPosts = list(range(len(posts_names), 0, -1))

    response = create_json(nPosts, posts_names, posts_urls)

    return response


def create_json(nPosts, posts, urls):
    """"""
    json_posts = [{'id': nPost, 'post': post, 'url': url}
                  for nPost, post, url in zip(nPosts, posts, urls)]
    return json.dumps(json_posts)
