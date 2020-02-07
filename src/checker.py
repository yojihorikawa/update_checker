# -*- coding: utf-8 -*-

import sys
import os
import requests
import json
import chromedriver_binary
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import datetime
from lxml import html

import tweepy

ROOT = "/src/"
TWITTERKEYS_FILE = ROOT + 'keys.json'
CONFIG_FILE = ROOT + 'config.json'
TWITTER_FILE = ROOT + 'twitter.json'
GITRELEASEJSON_FILE = ROOT + 'git_release.json'
MEDIUMJSON_FILE = ROOT + 'medium.json'
MEDIUM_SEARCHMAX=7

api = None

def read_twitter_keys():
    res = None
    try:
        with open(TWITTERKEYS_FILE, 'r', encoding='utf-8') as f:
            res = json.load(f)
            if res == None:
                raise Exception('Not valid keys.json')

            #認証
            auth = tweepy.OAuthHandler(res['Consumer_key'], res['Consumer_secret'])
            auth.set_access_token(res['Access_token'], res['Access_secret'])
            global api
            api = tweepy.API(auth, wait_on_rate_limit = True)
    except Exception as ex:
        print(ex)


twitter_prev={}
def twitter_load_prev():
    if os.path.exists(TWITTER_FILE):
        with open(TWITTER_FILE, 'r', encoding='utf-8') as f:
            global twitter_prev #下記でローカルと勘違いされてしまう為global宣言
            twitter_prev = json.load(f)

twitter_all={}
def collect_twitter(proj, user_name):
    if user_name == '':
        return

    twitter_data = []
    index = 0
    for status in api.user_timeline(screen_name=user_name, count=20):
        dtt = str(status.created_at)
        title = status.id_str
        text = ' '.join(status.text[0:100].splitlines()) + '...'
        # print(text)

        twitter_data.append({'date': dtt, 'title': title, 'text': text})

        # 前回までに登録されている記事じ含まれていなかった場合はログ出力
        # urlbase = 'https://twitter.com/' + user_name + '/status/' + title
        if not title_exists(twitter_prev, proj, title):
            print('[Twitter] Project: {0}, text: "{1}" is added.'.format(proj, text))

        index +=1
        if index >= 10:
            break

    twitter_all[proj] = twitter_data

    # twitter releaseの記事をダンプ
    # dttf = datetime.datetime.now().strftime('%Y%m%d')
    with open(TWITTER_FILE, 'w', encoding='utf-8') as fp:
        json.dump(twitter_all, fp, ensure_ascii=False, indent=4)



gitrelease_prev={}
def gitrelease_load_prev():
    if os.path.exists(GITRELEASEJSON_FILE):
        with open(GITRELEASEJSON_FILE, 'r', encoding='utf-8') as f:
            global gitrelease_prev #下記でローカルと勘違いされてしまう為global宣言
            gitrelease_prev = json.load(f)

gitrelease_all={}
def collect_gitrelease(name, url):
    if url == '':
        return

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    gitrelease_data = []
    for o1 in soup.find_all(attrs={'class': 'release-header'}):
        title = o1.find('a').text
        o3 = o1.find('relative-time')
        dtt = str(o3['datetime'])
        gitrelease_data.append({'date': dtt, 'title': title})

        # 前回までに登録されている記事じ含まれていなかった場合はログ出力
        if not title_exists(gitrelease_prev, name, title):
            print('[Git Releaase] Project: {0}, Title: "{1}" is added.'.format(name, title))

    gitrelease_all[name] = gitrelease_data
    # print(gitrelease_all)

    # git releaseの記事をダンプ
    # dttf = datetime.datetime.now().strftime('%Y%m%d')
    with open(GITRELEASEJSON_FILE, 'w') as fp:
        json.dump(gitrelease_all, fp, indent=4)


def title_exists(item_list, proj, title):
    if proj in item_list.keys():
        for item in item_list[proj]:
            if item['title'] == title:
                return True
    return False

medium_prev={}
def medium_load_prev():
    if os.path.exists(MEDIUMJSON_FILE):
        with open(MEDIUMJSON_FILE, 'r', encoding='utf-8') as f:
            global medium_prev #下記でローカルと勘違いされてしまう為global宣言
            medium_prev = json.load(f)

medium_all={}
def collect_medium(name, url):
    if url == '':
        return

    page = requests.get(url)
    tree = html.fromstring(page.content)

    medium_data = []
    for idx in range(2, MEDIUM_SEARCHMAX):
        source = tree.xpath('//*[@id="root"]/div/section/div[2]/div[1]/div[{0}]'.format(idx))
        soup = BeautifulSoup(html.tostring(source[0]), "html.parser")

        dtt = soup.find_all('a')[3].text #date
        title = soup.find('h1').text #title
        medium_data.append({'date': dtt, 'title': title})

        # 前回までに登録されている記事じ含まれていなかった場合はログ出力
        if not title_exists(medium_prev, name, title):
            print('[Medium] Project: {0}, Title: "{1}" is added.'.format(name, title))

    medium_all[name] = medium_data

    # Mediumの記事をダンプ
    # dttf = datetime.datetime.now().strftime('%Y%m%d')
    with open(MEDIUMJSON_FILE, 'w') as fp:
        json.dump(medium_all, fp, indent=4)


def load_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1280,1024')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(chrome_options=options)
    return driver

def collect_all_data(res):
    medium_load_prev()
    gitrelease_load_prev()
    twitter_load_prev()

    #driver = load_driver()
    for config_json in res:
        name = config_json["name"]
        medium = config_json["medium"]
        twitter = config_json["twitter"]
        release = config_json["release"]

        collect_medium(name, medium)
        collect_gitrelease(name, release)
        collect_twitter(name, twitter)

    # driver.quit()
    #driver.close()

def read_config():
    res = None
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            res = json.load(f)
    except Exception as ex:
        print(ex)
    return res


if __name__ == '__main__':
    read_twitter_keys()
    res = read_config()
    collect_all_data(res)

    exit()
