#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 17:06:11 2018

@author: yiqian
"""

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from gensim.models.word2vec import Word2Vec
from sklearn.externals import joblib

import pandas as pd
import re
import numpy as np
import time

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

def splitText(text):
    sentences = []
    for s in text:
        temp = s.split(' ')
        sentences.append(temp)
        
    return sentences

start = time.time()

dataframe = pd.read_csv('training.1600000.processed.noemoticon.csv', \
                        encoding = "ISO-8859-1", header=None).iloc[:, [0, 2, 5]].sample(frac=1).reset_index(drop=True)

ratio = 0.7                       # train test is 70%, test is 30%
size = 1600000

Dates = np.array(dataframe.iloc[:, 1].values)
Tweets = np.array(dataframe.iloc[:, 2].apply(PreProTweet).values)
Sentiment = np.array(dataframe.iloc[:, 0].values)

Tweets = splitText(Tweets)

Xtrain, Xtest, ytrain, ytest = train_test_split(Tweets, Sentiment, test_size = 1-ratio)


# dimension
nDim = 100
# initial model and build vocab
w2vModel = Word2Vec(size=nDim, min_count = 5, window = 5, workers=3)
w2vModel.build_vocab(Xtrain)

# train model
w2vModel.train(Xtrain, epochs=w2vModel.iter, total_examples=w2vModel.corpus_count)


def buildWordVector(text, size):
    vec = np.zeros(size).reshape((1, size))
    count = 0
    
    for word in text:
        try:
            vec += w2vModel[word].reshape((1, size))
            count += 1
        except KeyError:
            continue
    
    if count != 0:
        vec /= count
    return vec

from sklearn.preprocessing import scale

trainVec = np.concatenate([buildWordVector(z, nDim) for z in Xtrain])
trainVec = scale(trainVec)
print('-----train Word2Vec fininish----')

# train word2vec on test
w2vModel.train(Xtest, epochs=w2vModel.iter, total_examples=w2vModel.corpus_count)


testVec = np.concatenate([buildWordVector(z, nDim) for z in Xtest])
testVec = scale(testVec)
print('-----test Word2Vec fininish----')

# train Logic Regression
log = LogisticRegression(penalty='l2')
log.fit(trainVec, ytrain)
print('-----train LR model fininish----')

# save model
print('save model as "log_Word2Vec.m"')
joblib.dump(log, "log_Word2Vec.m")

# use model to predict
predict = log.predict(testVec)
print('-----predict fininish----')

from sklearn.metrics import classification_report

print(classification_report(ytest, predict))
print(time.time() - start)




