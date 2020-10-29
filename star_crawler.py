from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, RelationsOptions, EntitiesOptions, KeywordsOptions
from selenium import webdriver
from bs4 import BeautifulSoup
import time, re, os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()

from depandemic.models import Post

def instagram_crawler():

    #최초 게시글 클릭 후 오른쪽으로 넘겨주는 함수(반복)
    def move_next(driver):                                                                          #옆 게시물 클릭하여 이동해주는 함수
        right = driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow')
        right.click()
        time.sleep(1)

    #인스타 태그 url 반환함수
    def insta_searching(word):                                                                      # word라는 매개변수를 받는 insta_searching 이라는 함수 생성
        url = 'https://www.instagram.com/explore/tags/' + word
        return url

    #최근 게시글 클릭(최초1회 호출) 함수
    def select_recent_post(driver):
        first = driver.find_elements_by_css_selector('div._9AhH0')                                  #driver.find_elements_by_css_selector 여러개 배열로 받아와 최근게시물 선택
        first[9].click()
        time.sleep(3)  # 로딩을 위해 3초 대기

    #게시글 긁어오는 함수(반복)
    def get_content(driver):                                                                        #데이터를 받아와준다
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        data = {}

        try:#게시글 본문
            data['content'] = soup.select('div.C4VMK > span')[0].text
        except:
            data['content'] = ''

        data['tags'] = re.findall(r'#[^\s#,\\]+', data['content'])

        try:#게시글 날짜(그리니치 시간대 기준)
            data['date'] = soup.select('time._1o9PC.Nzb55')[0]['datetime'][:10]
        except:
            data['date'] = ''
        try:#좋아요수
            data['like'] = int(soup.select('div.Nm9Fw > button')[0].text[4:-1])
        except:
            data['like'] = 0
        try:#장소 있는 경우만
            data['place'] = soup.select('div.JF9hh')[0].text
        except:
            data['place'] = ''
        try:#사용자 id 저장
            data['user'] = soup.select('div.e1e1d')[0].text
        except:
            data['user'] = ''
        try:#게시글 이미지 저장
            data['imgUrl'] = soup.select('div.KL4Bh>img')['src']
            print(data['imgUrl'])
        except:
            data['user'] = ''

        return data

    # 로그인해주는 함수
    def instagram_login(id, password):
        login_section = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button'         #브라우저 켜질 때 마다 경우가 다르다 예외처리 해주깅
        driver.find_element_by_xpath(login_section).click()
        time.sleep(3)
        elem_login = driver.find_element_by_name('username')
        elem_login.clear()
        elem_login.send_keys(id)
        elem_login = driver.find_element_by_name('password')
        elem_login.clear()
        elem_login.send_keys(password)
        time.sleep(2)
        xpath = """//*[@id="loginForm"]/div/div[3]"""
        driver.find_element_by_xpath(xpath).click()
        time.sleep(4)
        xpath1 = """//*[@id="react-root"]/section/main/div/div/div/div/button"""
        driver.find_element_by_xpath(xpath1).click()
        time.sleep(4)

    def ibm_watson_set():
        authenticator = IAMAuthenticator('R_CsLMA0DRULvscHYVRZjmHLaF6uvWjScH_T-AefknQ7')
        natural_language_understanding = NaturalLanguageUnderstandingV1(version='2019-07-12',
                                                                        authenticator=authenticator)
        natural_language_understanding.set_service_url(
            'https://api.kr-seo.natural-language-understanding.watson.cloud.ibm.com/instances/7b8701eb-a403-429f-b9c6-e384776c70d3')

        return natural_language_understanding

    #-------------------------------------------------------------------------------------------------------------------------------------------#

    send_data = {}
    end_data = []
    results = []                                                                                        #크롤링결과 담을 변수
    #target = 9                                                                                          # 크롤링할 게시물 수

    driver = webdriver.Chrome("C:/Users/yechan/hanium/main/chromedriver.exe")                #진황 로컬 파일경로 #driver = webdriver.Chrome("C:\\Users\\chan\\Desktop\\Coding\\cmder\\main\\chromedriver.exe")       #찬우 로컬 파일경로
    keyword = '코로나'                                                                                     #검색키워드
    url = insta_searching(keyword)
    driver.get(url)
    time.sleep(4)

    natural_language_understanding = ibm_watson_set()
    instagram_login('jiiinang', 'chl2425!?')                                                            #로그인함수 호출 => 아이디 비밀번호 매개변수
    select_recent_post(driver)

    #for i in range(target):                                                #갯수로 게시글 크롤링해올때
    #    data = get_content(driver)  # 게시물 정보 가져오기
    #    results.append(data)
    #    if i != (target - 1):
    #        move_next(driver)

    while 1:                                                                        #배치돌릴때 해당날짜만 가져올때
         data = get_content(driver)  # 게시물 정보 가져오기
         results.append(data)

         if data['date'] == "2020-10-21":        #한국 업로드 시간과 해외 업로드시간이 차이가 나서 기준을 정해야 할듯 현 기준은 해외기준은 그리니치 표준시로 되어있음
             move_next(driver)
         else:
             break

    for i, insta in enumerate(results):
        send_data['location'] = "Unknown"
        send_data['categorized'] = ""
        send_data['score'] = 0

        response = natural_language_understanding.analyze(
            text=insta['content'],                                  #태그가 아직 콘텐츠에 있음 *수정
            features=Features(
                entities=EntitiesOptions(emotion=False),
                categories=EntitiesOptions(emotion=False, ),
                semantic_roles=EntitiesOptions(emotion=False, sentiment=False, ),
                keywords=KeywordsOptions(emotion=False, sentiment=False,)
            )
        ).get_result()

        for res in response['entities']:
            if res['type'] == "Location":
                send_data['location'] = res['text']
            else:
                send_data['location'] = "Unknown"

        for res1 in response['categories']:
            send_data['categorized'] = res1['label']
            send_data['score'] = res1['score']

        send_data['author'] = insta['user']
        send_data['title'] = insta['user']
        send_data['contents'] = insta['content']

        dictionary_copy = send_data.copy()
        end_data.append(dictionary_copy)
        print(i);

    return end_data

if __name__ == '__main__':                          #직접실행할때 돌아가는 부분 만약에 외부에서 돌린다면 else문이나 다른방법으로 돌려야할듯
    data = instagram_crawler()
    for x in data:
        Post(author=x['author'], identifier=2, location=x['location'], title=x['title'], contents=x['contents'],
             categorized_contents=x['categorized'], score=x['score']).save()  #published_date=x['published'], created_date=x['created'],
else:
    print("다른 모듈에서 import 해서 실행할때 이쪽으로 돌아간다(간접실행)")