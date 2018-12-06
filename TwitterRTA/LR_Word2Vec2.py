#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 17:53:09 2018

@author: yiqian
"""

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from gensim.models.word2vec import Word2Vec
from gensim.corpora.dictionary import Dictionary

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

# create word dictionary
def create_dictionary(w2v_model):
    dic = Dictionary()
    dic.doc2bow(w2v_model.wv.vocab.keys(), allow_update=True)
    w2index = {v:k+1 for k, v in dic.items()}
    w2vec = {word: w2v_model[word] for word in w2index.keys()}
    return w2index, w2vec

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
Tweets = dataframe.iloc[:, 2].apply(PreProTweet).values
Sentiment = np.array(dataframe.iloc[:, 0].values)

Tweets = splitText(Tweets)

#Xtrain, Xtest, ytrain, ytest = train_test_split(Tweets, Sentiment, test_size = 1-ratio)

# dimension
nDim = 100

"""
# initial model and build vocab
w2vModel = Word2Vec(Tweets, size=nDim, min_count = 10, window = 5, workers = 3)
w2vModel.save('Word2Vec.model')     #save model
"""
w2vModel = Word2Vec.load('Word2Vec.model')

index_dict, word_vectors = create_dictionary(w2vModel)

def text_to_index_vector(dic, text):
    sentence = []
    for sen in text:
        temp_s = []
        for w in sen:
            try:
                temp_s.append(dic[w])
            except:
                temp_s.append(0)
        sentence.append(temp_s)
    print(sentence[0])
    return np.array(sentence)
    
    
n_symbols = len(index_dict)+1
# use model to predict
# inital weights
embedding_weights = np.zeros((n_symbols, 100))
new_dict = index_dict
for w, index in index_dict.items():
    embedding_weights[index, :] = word_vectors[w]
    
Tweets = text_to_index_vector(new_dict, Tweets)

Xtrain, Xtest, ytrain, ytest = train_test_split(Tweets, Sentiment, test_size = 1-ratio)


# train Logic Regression
log = LogisticRegression(penalty='l2')
log.fit(Xtrain, ytrain)
print('-----train LR model fininish----')

# use model to predict
predict = log.predict(Xtest)
print('-----predict fininish----')

from sklearn.metrics import classification_report

print(classification_report(ytest, predict))
print(time.time() - start)




