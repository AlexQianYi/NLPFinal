#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 16:08:27 2018

@author: yiqian
"""

import re

import threading
import time
import datetime
import random
import pickle

import os

from GetTweetAPI import getTweet

f = open("NaiveBayes_BagofWord.pkl", 'rb')
model = pickle.load(f) 
f1 = open("BagofGram.pkl", 'rb')
vectorizer = pickle.load(f1)   

class SendTweet(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self, Tweet, client):
        client.send((Tweet).encode())
        message=client.recv(1024).decode()
        return message
    
        
class TimeCount(threading.Thread):

    count = 0
    def run(self):
        while True:
            print('server has run: ' + str(self.count) + 's' )
            time.sleep(10)
            self.count += 10
            
def PreProTweet(tweet):

    #Preprocess the text in a single tweet
    #arguments: tweet = a single tweet in form of string 
    #convert the tweet to lower case
    tweet.lower()
    #convert all urls to sting "URL"
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #convert all @username to "AT_USER"
    tweet = re.sub('@[^\s]+','AT_USER', tweet)
    #correct all multiple white spaces to a single white space
    tweet = re.sub('[\s]+', ' ', tweet)
    #convert "#topic" to just "topic"
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    tweet = re.sub(r'\W*\b\w{1,3}\b', '', tweet)
    return tweet

if __name__ == "__main__":     
    

    """
    Time count thread
    """
    count_thread = TimeCount()
    count_thread.start()
    
    
    location = ['\"continent_name\":\"North America\",\"country_iso_code\":\"US\", \"location\":{\"lat\":37.751, \"lon\":-97.822}', \
                '\"continent_name\":\"China\",\"country_iso_code\":\"CN\", \"location\":{\"lat\":39.906, \"lon\":116.416}', \
                '\"continent_name\":\"United Kindom\",\"country_iso_code\":\"UK\", \"location\":{\"lat\":51.509, \"lon\":-0.105}', \
                '\"continent_name\":\"Austrlia\",\"country_iso_code\":\"AU\", \"location\":{\"lat\":-37.781, \"lon\":-145.018}', \
                '\"continent_name\":\"Koera\",\"country_iso_code\":\"KR\", \"location\":{\"lat\":37.550, \"lon\":126.990}',\
                '\"continent_name\":\"India\",\"country_iso_code\":\"IN\", \"location\":{\"lat\":22.581, \"lon\":78.369}', \
                '\"continent_name\":\"North America\",\"country_iso_code\":\"IT\", \"location\":{\"lat\":43.106, \"lon\":11.671}',\
                '\"continent_name\":\"North America\",\"country_iso_code\":\"US\", \"location\":{\"lat\":43.106, \"lon\":11.671}']
    command1 = 'curl -XPUT '
    command2 = ' -H \'Content-Type: application/json\' -d\' {\"@timestamp\":\"'
    command3 = '\", \"title\":"Twitter\", \"doc_type\":\"entity\", \"sentiment\":\"'                                                    
    command4 = '\", \"parent\":\"1\", \"entity\": {\"text\": \"'
    command5 = '\", \"type\":\"QUANTITY\"}, \"geoip\":{'
    command6 = '}}\''
    
    endPoint = 'https://search-dsfinal-f5oo4flfsyx4lbphh36fmecgam.us-east-1.es.amazonaws.com/'
    file = 'movie-review-'
    timestamp = int(time.time()*1000)
    
    print('Please input the Keyword in Tweet')
    keyword = input()
    preTweet = ""
    TweetCount = 0
    while True:
        count = 1

        Tweets = getTweet(keyword, count)
        if len(Tweets)>0:
            if Tweets == preTweet:
                print('no new Tweet..................')
                time.sleep(5)
            else:
                print(Tweets)
                preTweet = Tweets
                Tweet1 = PreProTweet(Tweets[0])
                TweetCount += 1
                
                realTimeTweet = vectorizer.transform(Tweet1.split('\n'))
                sentiment=result = model.predict(realTimeTweet)
                print('the result from Naive Bayes 1 is :' + str(sentiment))
                d = datetime.datetime.now().strftime("%Y-%m-%d")
                date = d + '/doc/'
                des = endPoint + file + date + str(TweetCount)
                loca = location[int(random.random()*(len(location)-1))]
                #location = location[int(random.random()*len(location))]
                if sentiment[0] == 0:
                    sent = 'NEGATIVE or NETURAL'
                else:
                    sent = 'POSITIVE'
                
                command = command1 + des + command2 + str(timestamp) + command3 + sent + command4 + Tweet1 + command5 + loca + command6
                print('==========')
                print(command)
                print('==========')
                
                os.system(command)
                
                time.sleep(5)
        else:
            print('no new Tweet..................')
            time.sleep(5)

#sample_command = 'curl -XPUT https://search-dsfinal-f5oo4flfsyx4lbphh36fmecgam.us-east-1.es.amazonaws.com/movie-review-2018-05-15/doc/5 -H \'Content-Type: application/json\' -d\' {\"@timestamp\": \"1525523999877\", \"title\": \"test title\", \"doc_type\": \"entity\", \"sentiment\": \"POSITIVE\", \"parent\": \"1\", \"entity\": {\"text\": \"entity-1\", \"type\": \"QUANTITY\"}}\''
#os.system(sample_command)

