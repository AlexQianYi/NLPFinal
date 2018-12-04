#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 16:37:26 2018

@author: yiqian
"""


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib

import pandas as pd
import re
import numpy as np
import time
import pickle

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


start = time.time()

dataframe = pd.read_csv('training.1600000.processed.noemoticon.csv', \
                        encoding = "ISO-8859-1", header=None).iloc[:, [0, 2, 5]].sample(frac=1).reset_index(drop=True)

ratio = 0.7                       # train test is 70%, test is 30%
size = 1600000

trainDates = np.array(dataframe.iloc[:int(size*ratio), 1].values)
trainTweets = np.array(dataframe.iloc[:int(size*ratio), 2].apply(PreProTweet).values)
trainSentiment = np.array(dataframe.iloc[:int(size*ratio), 0].values)

testDates = np.array(dataframe.iloc[int(size*ratio):, 1].values)
testTweets = np.array(dataframe.iloc[int(size*ratio):, 2].apply(PreProTweet).values)
testSentiment = np.array(dataframe.iloc[int(size*ratio):, 0].values)

print('----load data finish----')

# train bag of words
# with unigrams and bigrams
vectorizer = CountVectorizer(ngram_range=(2, 2))

Xtrain = vectorizer.fit_transform(trainTweets)
print('----Bag of Gram finish----')
# save bag of gram
print('save model as "BagofGram.pkl"')
output = open("BagofGram.pkl", "wb")
pickle.dump(vectorizer, output)


# train Naive Bayes
clf = MultinomialNB(alpha=1.0)
clf.fit(Xtrain, trainSentiment)

# save model
print('save model as "NaiveBayes_BagofWord.pkl"')
output = open("NaiveBayes_BagofWord.pkl", "wb")
pickle.dump(clf, output)

# test bag of words
Xtest = vectorizer.transform(testTweets)

# use model to predict
predict = clf.predict(Xtest)

from sklearn.metrics import classification_report

print(classification_report(testSentiment, predict))
print('run time '+str(time.time()-start))
    
    
    