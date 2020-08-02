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

from twitterscraper.query import query_tweets 
import csv 
import datetime 
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, RelationsOptions

keyword = 'covid' 
f = open(keyword+'.csv','w',encoding='utf-8-sig',newline='') 
w = csv.writer(f,delimiter=',') 
list_of_tweets = query_tweets(keyword, begindate=datetime.date(2020,7,27), enddate=datetime.date(2020,8,1), limit=5) 

for tweet in list_of_tweets: 
    w.writerow([tweet.timestamp, tweet.text]) 
f.close()


authenticator = IAMAuthenticator('Fuxoqi_ltW0gcE6PZkYT-lMS8zsY0Xtd7AfaKzqesa_W')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    authenticator=authenticator
)

natural_language_understanding.set_service_url('https://api.kr-seo.natural-language-understanding.watson.cloud.ibm.com/instances/f85b9cf9-3ab1-477c-8627-5dd173ced2c1')

f = open('covid.csv','rt',encoding='utf-8-sig')
rdr = csv.reader(f)
with open("testfile2.json","w") as json_file:
    for line in rdr:
        response = natural_language_understanding.analyze(text=line[1],features=Features(relations=RelationsOptions()),language='en').get_result()

        json.dump(response, json_file, indent=2)
