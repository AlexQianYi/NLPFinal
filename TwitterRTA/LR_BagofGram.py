#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 17:36:32 2018

@author: yiqian
"""

import ProData

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

from sklearn.model_selection import cross_validate

def NaiveBayes():
    
    dates, tweets, sentiment = ProData.DivData()
    
    # with unigrams and bigrams
    vectorizer = CountVectorizer(ngram_range=(1, 2))
    
    model = vectorizer.fit_transform(tweets)
    X = model.toarray()
    
    log = LogisticRegression(penalty='l2')
    
    scorce = cross_validate(log, X, sentiment , scoring='accuracy')
    print(scorce)
    
NaiveBayes()