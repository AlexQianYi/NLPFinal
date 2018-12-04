#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 15:00:34 2018

@author: yiqian
"""

import tweepy


    
def getTweet(keyWords, c):
    
    # Twitter API parameter
    consumer_key = "U85yS51L50Ox8aHleLBv7PXQW"
    consumer_secret = "QqkNI7HfiPR7u6goGVRr8xrb7zKXu28UyX0bUPnKhJoWALu9yX"
    access_key = "1060236895622443010-ulBTuLlQDqwTL0I8CuwNtLjF3YyAV2"
    access_secret = "80d0OZmvgu8bbYb543OJ1adnyLZb7ap1wJOclyN03V4bF"
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    
    # make initial request for most recent tweets (200 is the maximum all)
    result = api.search(q = keyWords, lang = 'en', count = c)
    
    Tweets = []
    for t in result:
        Tweets.append(str(t.text))
    return Tweets
            

