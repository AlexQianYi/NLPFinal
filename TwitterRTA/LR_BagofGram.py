#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 17:36:32 2018

@author: yiqian
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

from sklearn.model_selection import cross_validate

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


dataframe = pd.read_csv('training.1600000.processed.noemoticon.csv', \
                        encoding = "ISO-8859-1", header=None).iloc[:, [0, 2, 5]].sample(frac=1).reset_index(drop=True)


dates = np.array(dataframe.iloc[:, 1].values)
tweets = np.array(dataframe.iloc[:, 2].apply(PreProTweet).values)
sentiment = np.array(dataframe.iloc[:, 0].values)

print('----load data finish----')

train, test = [], []

ratio = 0.7                       # train test is 70%, test is 30%
size = 1600000
    

# with unigrams and bigrams
vectorizer = CountVectorizer(ngram_range=(2, 2))

X = vectorizer.fit_transform(tweets)
#X = model.toarray()

print('----Bag of Gram finish----')
    
log = LogisticRegression(penalty='l2')

scorce = cross_validate(log, X, sentiment, cv=5 scoring='accuracy')
print(scorce)