"""
import datetime
from twitterscraper import query_tweets

list_of_tweets = query_tweets('코로나바이러스', begindate=datetime.date(2020,7,6), enddate=datetime.date(2020,7,7), limit=5)

for tweet in list_of_tweets:
    print("screen_name: "+tweet.screen_name) #사용자아이디
    print("username: "+tweet.username) #닉네임
    print("timestamp: "+str(tweet.timestamp)) #날짜
    print("text: "+tweet.text) #트윗내용
"""

# from twitterscraper.query import query_tweets
import csv
import datetime

import os
# Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
django.setup()

import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, RelationsOptions, EntitiesOptions, KeywordsOptions

# 크롤링해오는 부분
# keyword = 'covid'
# f = open(keyword+'.csv','w',encoding='UTF-8-sig',newline='')
# w = csv.writer(f,delimiter=',')
# list_of_tweets = query_tweets(keyword, begindate=datetime.date(2020,7,27), enddate=datetime.date(2020,8,1), limit=100)
#
# for tweet in list_of_tweets:
#     w.writerow([tweet.timestamp, tweet.text])
# f.close()
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re, csv
import pandas as pd
from depandemic.models import Post




def instagram_crawler():
    def move_next(driver):
        right = driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow')
        right.click()
        time.sleep(1)

    # 함수 작성
    def insta_searching(word):  # word라는 매개변수를 받는 insta_searching 이라는 함수 생성
        url = 'https://www.instagram.com/explore/tags/' + word
        return url

    def select_first(driver):
        first = driver.find_element_by_css_selector('div._9AhH0')
        # find_element_by_css_selector 함수를 사용해 요소 찾기
        first.click()
        time.sleep(3)  # 로딩을 위해 3초 대기

    # 본문 내용, 작성 일시, 위치 정보 및 해시태그(#) 추출
    def get_content(driver):
        # 1. 현재 페이지의 HTML 정보 가져오기
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        # 2. 본문 내용 가져오기
        try:  # 여러 태그중 첫번째([0]) 태그를 선택
            content = soup.select('div.C4VMK > span')[0].text
        # 첫 게시글 본문 내용이 <div class="C4VMK"> 임을 알 수 있다.
        # 태그명이 div, class명이 C4VMK인 태그 아래에 있는 span 태그를 모두 선택.
        except:
            content = ' '

        #print(content)

        # 3. 본문 내용에서 해시태그 가져오기(정규표현식 활용)
        tags = re.findall(r'#[^\s#,\\]+',
                          content)  # content 변수의 본문 내용 중 #으로 시작하며, #뒤에 연속된 문자(공백이나 #, \ 기호가 아닌 경우)를 모두 찾아 tags 변수에 저장
        # 4. 작성 일자 가져오기
        try:
            date = soup.select('time._1o9PC.Nzb55')[0]['datetime'][:10]  # 앞에서부터 10자리 글자
        except:
            date = ''
        # 5. 좋아요 수 가져오기
        try:
            like = soup.select('div.Nm9Fw > button')[0].text[4:-1]
        except:
            like = 0
        # 6. 위치 정보 가져오기
        try:
            place = soup.select('div.JF9hh')[0].text
        except:
            place = ''

        data = [content, date, like, place, tags]

        return data

    # 1. 크롬으로 인스타그램 - '' 검색
    driver = webdriver.Chrome("C:\\Users\\user\\Documents\\webdriver\\chromedriver.exe")
    word = 'covid'
    url = insta_searching(word)
    driver.get(url)
    time.sleep(4)
    # 2. 로그인 하기
    login_section = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button'
    driver.find_element_by_xpath(login_section).click()
    time.sleep(3)
    elem_login = driver.find_element_by_name("username")
    elem_login.clear()
    elem_login.send_keys('jiiinang')
    elem_login = driver.find_element_by_name('password')
    elem_login.clear()
    elem_login.send_keys('chl2425!?')
    time.sleep(1)
    xpath = """//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button"""
    driver.find_element_by_xpath(xpath).click()
    time.sleep(4)
    xpath1 = """//*[@id="react-root"]/section/main/div/div/div/div/button"""
    driver.find_element_by_xpath(xpath1).click()
    time.sleep(4)
    # 3. 검색페이지 접속하기
    driver.get(url)
    time.sleep(4)
    # 3-1. if문써서 see posts 페이지 나오면 클릭하고 아니면 그냥바로 게시글 열기로 가기
    see_post = '//*[@id="react-root"]/section/main/article/div/ul/li[1]/button'
    driver.find_element_by_xpath(see_post).click()
    time.sleep(3)
    # 4. 첫번째 게시글 열기
    select_first(driver)
    # 5. 비어있는 변수(results) 만들기
    results = []
    # 여러 게시물 크롤링하기
    target = 5  # 크롤링할 게시물 수

    for i in range(target):
        data = get_content(driver)  # 게시물 정보 가져오기
        results.append(data)
        if i != (target - 1):
            move_next(driver)
        #print(i)

    #print(results[:target])

    results_df = pd.DataFrame(results)
    results_df.columns = ['content', 'data', 'like', 'place', 'tags']

    # results_df['tags']

    results_df = pd.DataFrame(results)
    results_df.columns = ['content', 'data', 'like', 'place', 'tags']
    results_df.to_csv("C:\\Users\\user\\test2.csv", encoding='utf-8-sig')

    authenticator = IAMAuthenticator('R_CsLMA0DRULvscHYVRZjmHLaF6uvWjScH_T-AefknQ7')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2019-07-12',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(
        'https://api.kr-seo.natural-language-understanding.watson.cloud.ibm.com/instances/7b8701eb-a403-429f-b9c6-e384776c70d3')

    f = open('C:\\Users\\user\\test2.csv', 'r', encoding='UTF-8-sig', newline='')
    rdr = csv.reader(f)
    data = []
    for line in rdr:
        with open(line[0][:10] + '.json', 'w', encoding='UTF-8-sig', newline='') as json_file:
            response = natural_language_understanding.analyze(text=line[1],
                                                              features=Features(relations=RelationsOptions(),
                                                                                entities=EntitiesOptions(emotion=True,
                                                                                                         sentiment=True,
                                                                                                         limit=2),
                                                                                keywords=KeywordsOptions(emotion=True,
                                                                                                         sentiment=True,
                                                                                                         limit=2)),
                                                              language='en').get_result()
            #print(response)
            json.dump(response, json_file, indent=2)

        data.append(response)

    #print('시작합니데이', data)

    return data


if __name__=='__main__':
    post_data = instagram_crawler()
    cnt = 0
    for i in post_data:
        print(i)
        Post(author=cnt).save()
        cnt = cnt + 1
        #Post(content=str(i)).save()


#instagram_crawler()