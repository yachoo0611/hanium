import datetime 
import csv 
from twitterscraper import query_tweets 

list_of_tweets = query_tweets('corona', begindate=datetime.date(2020,9,1), enddate=datetime.date(2020,9,3), limit=10)
for tweet in list_of_tweets: 
    print("screen_name: "+tweet.screen_name)
    print("username: "+tweet.username) 
    print("timestamp: "+str(tweet.timestamp)) 
    print("text: "+tweet.text)


