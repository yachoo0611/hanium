import csv
import datetime
import json

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, RelationsOptions, EntitiesOptions, KeywordsOptions

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re, os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()
from depandemic.models import Post

def instagram_crawler():
    send_data = {}
    end_data2 = []

    def move_next(driver):
        right = driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow')
        right.click()
        time.sleep(1)

    def insta_searching(word):  # word라는 매개변수를 받는 insta_searching 이라는 함수 생성
        url = 'https://www.instagram.com/explore/tags/' + word
        return url

    def select_first(driver):
        first = driver.find_element_by_css_selector('div._9AhH0')
        first.click()
        time.sleep(3)  # 로딩을 위해 3초 대기

    def get_content(driver):
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        try:
            content = soup.select('div.C4VMK > span')[0].text
        except:
            content = ' '

        tags = re.findall(r'#[^\s#,\\]+', content)

        try:
            date = soup.select('time._1o9PC.Nzb55')[0]['datetime'][:10]  # 앞에서부터 10자리 글자
        except:
            date = ''
        try:
            like = soup.select('div.Nm9Fw > button')[0].text[4:-1]
        except:
            like = 0
        try:
            place = soup.select('div.JF9hh')[0].text
        except:
            place = ''
        try:
            user = soup.select('div.e1e1d')[0].text
        except:
            user = ''

        data = [content, date, like, place, tags, user]
        return data

    # 1. 크롬으로 인스타그램 - '' 검색
    #driver = webdriver.Chrome("C:\\Users\\user\\Documents\\webdriver\\chromedriver.exe")
    driver = webdriver.Chrome("C:\\Users\\chan\\Desktop\\Coding\\cmder\\main\\chromedriver.exe")
    word = '코로나'
    url = insta_searching(word)
    driver.get(url)
    time.sleep(4)

    elem_login = driver.find_element_by_name("username")
    elem_login.clear()
    elem_login.send_keys('jiiinang')
    elem_login = driver.find_element_by_name('password')
    elem_login.clear()
    elem_login.send_keys('chl2425!?')
    time.sleep(2)

    xpath = """//*[@id="loginForm"]/div/div[3]"""
    driver.find_element_by_xpath(xpath).click()

    time.sleep(4)
    xpath1 = """//*[@id="react-root"]/section/main/div/div/div/div/button"""
    driver.find_element_by_xpath(xpath1).click()
    time.sleep(4)

    select_first(driver)
    results = []
    target = 9  # 크롤링할 게시물 수

    for i in range(target):
        data = get_content(driver)  # 게시물 정보 가져오기
        results.append(data)
        if i != (target - 1):
            move_next(driver)

    authenticator = IAMAuthenticator('R_CsLMA0DRULvscHYVRZjmHLaF6uvWjScH_T-AefknQ7')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2019-07-12',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(
        'https://api.kr-seo.natural-language-understanding.watson.cloud.ibm.com/instances/7b8701eb-a403-429f-b9c6-e384776c70d3')

    for i, insta in enumerate(results):
        send_data['location'] = "Unknown"
        send_data['categorized'] = ""
        send_data['score'] = ""

        #print(insta, i)
        response = natural_language_understanding.analyze(
            text=insta[0],
            features=Features(
                entities=EntitiesOptions(emotion=False),
                categories=EntitiesOptions(emotion=False, ),
                semantic_roles=EntitiesOptions(emotion=False, sentiment=False, ),
                keywords=KeywordsOptions(emotion=False, sentiment=False, )
            )
        ).get_result()

        # print(response)

        for res in response['entities']:
            if res['type'] == "Location":
                send_data['location'] = res['text']
            else:
                send_data['location'] = "Unknown"

        for res1 in response['categories']:
            send_data['categorized'] = res1['label']
            send_data['score'] = res1['score']

        send_data['author'] = insta[5]
        send_data['title'] = insta[5]
        send_data['contents'] = insta[0]
        send_data['created'] = insta[1]
        send_data['published'] = insta[1]

        dictionary_copy = send_data.copy()
        end_data2.append(dictionary_copy)

    return end_data2

    # return results

if __name__ == '__main__':
    data1 = instagram_crawler()
    for x in data1:
        Post(author=x['author'], identifier=1, location=x['location'], title=x['title'], contents=x['contents'],
             created_date=x['created'],
             published_date=x['published'], categorized_contents=x['categorized'], score=x['score']).save()

        # print(instagram_crawler())