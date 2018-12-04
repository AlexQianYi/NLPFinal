#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 15:00:34 2018

@author: yiqian
"""

import tweepy
import time
import threading

import time

class TimeCount(threading.Thread):

    count = 0
    def run(self):
        while True:
            print('server has run: ' + str(self.count) + 's' )

            time.sleep(10)
            self.count += 10

class SearchTwitter():
    
    def __init__(self):
        # Twitter API parameter
        self.consumer_key = "U85yS51L50Ox8aHleLBv7PXQW"
        self.consumer_secret = "QqkNI7HfiPR7u6goGVRr8xrb7zKXu28UyX0bUPnKhJoWALu9yX"
        self.access_key = "1060236895622443010-ulBTuLlQDqwTL0I8CuwNtLjF3YyAV2"
        self.access_secret = "80d0OZmvgu8bbYb543OJ1adnyLZb7ap1wJOclyN03V4bF"
        self.api = getAPI()
        
        
    def getAPI(self):

        # authorize twitter, initialize tweepy
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_key, self.access_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        return api
    
    def getTweet(self, keyWords):

        # use list to store
        tweets = []
        
        # make initial request for most recent tweets (200 is the maximum all)
        while True:
            
            result = self.api.search(q = keyWords, lang = 'en')
            for w in result:
                print(w.text)

