#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 17:05:52 2018

@author: yiqian
"""


"""
data format:
    [<id>, <target>, <date>, <content>]
"""

import csv
import random
import pandas as pd
import re
import numpy as np

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

def DivData():

    dataframe = pd.read_csv('training.1600000.processed.noemoticon.csv', \
                            encoding = "ISO-8859-1", header=None).iloc[:, [0, 2, 5]].sample(frac=1).reset_index(drop=True)
    
    
    dates = np.array(dataframe.iloc[:, 1].values)
    tweets = np.array(dataframe.iloc[:, 2].apply(PreProTweet).values)
    sentiment = np.array(dataframe.iloc[:, 0].values)
    
    train, test = [], []
    
    ratio = 0.7                       # train test is 70%, test is 30%
    size = 1600000
    
    return dates, tweets, sentiment

        
DivData()