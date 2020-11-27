from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import datetime
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, RelationsOptions

from selenium.webdriver.chrome.options import Options
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()
from depandemic.models import Post

authenticator = IAMAuthenticator('Fuxoqi_ltW0gcE6PZkYT-lMS8zsY0Xtd7AfaKzqesa_W')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    authenticator=authenticator
)
natural_language_understanding.set_service_url('https://api.kr-seo.natural-language-understanding.watson.cloud.ibm.com/instances/f85b9cf9-3ab1-477c-8627-5dd173ced2c1')


def facebook_crawler():


    # 권한 팝업창때문에 넣음
    option = Options()
    option.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 1
    })

    driver = webdriver.Chrome(executable_path="C:/Users/chan/Desktop/Coding/cmder/main/chromedriver.exe", chrome_options=option)
    #chrome driver 경로 확인합시당~

    driver.implicitly_wait(3)

    driver.get('https://www.facebook.com/')

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    ## 로그인
    email = driver.find_element_by_xpath("//input[@name='email']")
    password = driver.find_element_by_xpath("//input[@name='pass']")
    btn = driver.find_element_by_xpath("//*[@id='u_0_b']")
    #이메일 비밀번호 입력하세용   + 접속시 최신 UI 기준으로 xpath설정했으니 과거 UI로 접속되는 아이디는 에러남.
    email.send_keys("")
    password.send_keys("")
    btn.click()
    # 키워드 검색하기
    searchbox = driver.find_element_by_xpath("//*[@id='mount_0_0']/div/div[1]/div[1]/div[2]/div[2]/div/div/div/div/label")
    searchbox.send_keys("covid")
    # time.sleep(3)
    searchbox.send_keys(Keys.RETURN)




    last_height = driver.execute_script("return document.body.scrollHeight")


    while True:
        # 스크롤최대
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(3)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # # 창 일단 모두 열어두자
    down_Scroll = 40
    for i in range(down_Scroll):
        body = driver.find_element_by_css_selector('body')
        body.send_keys(Keys.PAGE_DOWN)
        print(i)

    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    scope = 20
    send_data = {}
    end_data2 = []
    # 0. 이름 추출
    author = soup.select('#mount_0_0 > div > div:nth-child(1) > div.rq0escxv.l9j0dhe7.du4w35lb > div.rq0escxv.l9j0dhe7.du4w35lb > div > div > div.j83agx80.cbu4d94t.d6urw2fd.dp1hu0rb.l9j0dhe7.du4w35lb > div.rq0escxv.l9j0dhe7.du4w35lb.j83agx80.pfnyh3mw.jifvfom9.gs1a9yip.owycx6da.btwxx1t3.buofh1pr.dp1hu0rb.ka73uehy > div.rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.g5gj957u.d2edcug0.hpfvmrgz.rj1gh0hx.buofh1pr.dp1hu0rb > div > div > div > div > div > div > div > div > div > div > div > div > div.discj3wi.hv4rvrfc.qt6c0cv9.dati1w0a > div > div.hpfvmrgz.g5gj957u.buofh1pr.rj1gh0hx.o8rfisnq > div > div:nth-child(1) > span > span > a > span:nth-child(1)')

    # 1. text만 뽑으려면 자식 태그(date)를 제외해서 text만 추출 해야함 ---> decompose() 등등 몇개 시험해봤는데 잘 안됨 왜 안되지..?

    text_data = soup.select('#mount_0_0 > div > div:nth-child(1) > div.rq0escxv.l9j0dhe7.du4w35lb > div.rq0escxv.l9j0dhe7.du4w35lb > div > div > div.j83agx80.cbu4d94t.d6urw2fd.dp1hu0rb.l9j0dhe7.du4w35lb > div.rq0escxv.l9j0dhe7.du4w35lb.j83agx80.pfnyh3mw.jifvfom9.gs1a9yip.owycx6da.btwxx1t3.buofh1pr.dp1hu0rb.ka73uehy > div.rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.g5gj957u.d2edcug0.hpfvmrgz.rj1gh0hx.buofh1pr.dp1hu0rb > div > div > div > div > div > div > div > div > div > div > div > div > div.jb3vyjys.hv4rvrfc.ihqw7lf3.dati1w0a > a > div > div.hpfvmrgz.buofh1pr > span > span')


    # 시간 추출
    date = soup.select('#mount_0_0 > div > div:nth-child(1) > div.rq0escxv.l9j0dhe7.du4w35lb > div.rq0escxv.l9j0dhe7.du4w35lb > div > div > div.j83agx80.cbu4d94t.d6urw2fd.dp1hu0rb.l9j0dhe7.du4w35lb > div.rq0escxv.l9j0dhe7.du4w35lb.j83agx80.pfnyh3mw.jifvfom9.gs1a9yip.owycx6da.btwxx1t3.buofh1pr.dp1hu0rb.ka73uehy > div.rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.g5gj957u.d2edcug0.hpfvmrgz.rj1gh0hx.buofh1pr.dp1hu0rb > div > div > div > div > div > div > div > div > div > div > div > div > div.jb3vyjys.hv4rvrfc.ihqw7lf3.dati1w0a > a > div > div.hpfvmrgz.buofh1pr > span > span > span')
    for a in range(scope):
        author2 = author[a].text

        text_data2 = text_data[a].text
        text_data3 = text_data2[9:]

        response = natural_language_understanding.analyze(
            text=text_data3,
            features=Features(
                entities=EntitiesOptions(emotion=False),
                categories=EntitiesOptions(emotion=False, ),
                semantic_roles=EntitiesOptions(emotion=False, sentiment=False, ),
                keywords=KeywordsOptions(emotion=False, sentiment=False, )
            )
        ).get_result()
        for re in response['entities']:
            if re['type'] == "Location":
                send_data['location'] = re['text']
            else:
                send_data['location'] = "Unknown"

        for re1 in response['categories']:
            send_data['categorized'] = re1['label']
            send_data['score'] = re1['score']

        send_data['author'] = author2
        send_data['title'] = 'facebook - '+str(author2)+str(a)
        send_data['contents'] = text_data3
        # send_data['created'] = date_transfer(date)
        send_data['published'] = datetime.datetime.now()

        dictionary_copy = send_data.copy()
        end_data2.append(dictionary_copy)

    # print(end_data2)

    return end_data2

# def date_transfer(date):
#     scope=20
#     today_config='분'
#     another_config='월'
#     for i in range(scope):
#         if today_config in date[i]:
#             return datetime.datetime.now()
#         elif another_config in date[i]:
#             return datetime.datetime.now()-datetime.timedelta(1)

if __name__=='__main__':
    data1 = facebook_crawler()
    for x in data1:
        Post(author=x['author'],identifier=1,title=x['title'],contents=x['contents'],
             published_date=x['published'],categorized_contents=x['categorized'],score=x['score']).save()
