#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 15:00:34 2018

@author: yiqian
"""

import re
import tweepy
import time
import random
import pandas as pd

# Twitter API parameter
consumer_key = "U85yS51L50Ox8aHleLBv7PXQW"
consumer_secret = "QqkNI7HfiPR7u6goGVRr8xrb7zKXu28UyX0bUPnKhJoWALu9yX"
access_key = "1060236895622443010-ulBTuLlQDqwTL0I8CuwNtLjF3YyAV2"
access_secret = "80d0OZmvgu8bbYb543OJ1adnyLZb7ap1wJOclyN03V4bF"


# authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

name = "nytimes"

# use list to store
tweets = []

# make initial request for most recent tweets (200 is the maximum all)
while True:
    result = api.user_timeline(id = name, count = 20)
    for w in result:
        print(w)
    """
    new_tweets = api.home_timeline()
    for t in new_tweets:
        print(t)
    """
#new_tweets = api.user_timeline(screen_name = screen_name, count=50)

"""
# add tweets in list
tweets += new_tweets

# save the id of the latest tweets
latest = tweets[-1].id - 1

# keep grabbbing tweets until there are no tweets left to grab
while len(new_tweets) > 0:
    print('getting tweets before %s' % (latest))
    
    finish = True
    while finish:
        try:
            new_tweets = api.user_timeline(screen_name = screen_name, count=50, max_id=latest)
            finish = False
        except Exception as e:
            print(e)
            time.sleep(random.choice(range(300, 600)))
            finish = True
        
        # save most recent tweets
        tweets += new_tweets
        # update the id of the oldest tweet less one
        latest = tweets[-1].id - 1
        print('... %s tweets downloaded so far' % (len(tweets)))
        
outtweets = pd.DataFrame()
outtweets['tweet ID'] = [tweet.id_str for tweet in tweets]
outtweets['tweet date'] = [tweet.created_at for tweet in tweets]
outtweets['tweet content'] = [re.sub(r'\s+'," ", tweet.text) for tweet in tweets]
"""