import urllib.request
import json
# import time
# from platform import system
# from selenium import webdriver
from bs4 import BeautifulSoup


url = 'https://dev.to'


def checkLastPost(user):
    """Get the title of the last post only, can be used to check if there is a new post"""
    user_url = url + '/' + user
    web = urllib.request.urlopen(user_url)

    soup = BeautifulSoup(web, 'html.parser')

    last_post = soup.find('h3')
    last_post = last_post.text.strip()

    return last_post


def getLastPosts(user):
    """Get the lasts 5 posts of the user because Dev.to loads the rest on demand when scrolling"""
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
    totalPosts = getNTotalPosts(user)

    response = create_json(totalPosts, nPosts, posts_names, posts_urls)

    return response


def getNTotalPosts(user):
    """Get the total posts written by the user"""
    user_url = url + '/' + user
    web = urllib.request.urlopen(user_url)

    soup = BeautifulSoup(web, 'html.parser')

    # Get the text inside the first div in sidebar-data,
    # trim it, split it based on spaces and get the first element,
    # which is the number of posts
    total_posts = soup.find(
        'div', attrs={'class': 'sidebar-data'}).find('div').text.strip().split(' ')[0]

    return total_posts


def create_json(totalPosts, nPosts, posts, urls):
    """Takes the parameters and make a json to send as response"""
    json_posts = {'total': totalPosts, 'posts': [{'id': nPost, 'post': post, 'url': url}
                                                 for nPost, post, url in zip(nPosts, posts, urls)]}
    return json.dumps(json_posts)


############# See Readme.md to use this ######################
# def getAllPosts(user):
#     """Get all posts written by the user using selenium to scroll down an load all the posts"""
#     web = infiniteScroll(user)
#
#     soup = BeautifulSoup(web, 'html.parser')
#
#     find_posts = soup.find_all('div', attrs={'class': 'single-article'})
#
#     posts_h3 = filter(lambda x: x is not None,
#                       map(lambda x: x.find('h3'), find_posts))
#     posts_names = list(map(
#         lambda x: x.text.strip(), posts_h3))
#
#     posts_a = filter(lambda x: x is not None, map(
#         lambda x: x.find('a', attrs={'class': 'index-article-link'}), find_posts))
#     posts_urls = list(map(lambda x: url+x['href'], posts_a))
#
#     nPosts = list(range(len(posts_names), 0, -1))
#
#     response = create_json(nPosts, posts_names, posts_urls)
#
#     return response
#
# def infiniteScroll(user):
#     """Uses selenium with chromedriver headless to scroll down the page"""
#     user_url = url + '/' + user
#
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')
#     driver_path = './chromedriver.exe' if system() == 'Windows' else './chromedriver'
#
#     browser = webdriver.Chrome(
#         executable_path=driver_path, chrome_options=options)
#
#     # Tell Selenium to get the URL you're interested in.
#     browser.get(user_url)
#
#     # Selenium script to scroll to the bottom, wait 1 second for the next batch of data to load, then continue scrolling.  It will continue to do this until the page stops loading new data.
#     lenOfPage = browser.execute_script(
#         "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
#     match = False
#     while(match == False):
#         lastCount = lenOfPage
#         time.sleep(1)
#         lenOfPage = browser.execute_script(
#             "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
#         if lastCount == lenOfPage:
#             match = True
#
#     return browser.page_source
#########################################################
