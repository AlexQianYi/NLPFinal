#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 16:37:26 2018

@author: yiqian
"""

import ProData

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

from sklearn.model_selection import cross_validate

def NaiveBayes():
    
    dates, tweets, sentiment = ProData.DivData()
    
    # with unigrams and bigrams
    vectorizer = CountVectorizer(ngram_range=(1, 2))
    
    model = vectorizer.fit_transform(tweets)
    X = model.toarray()
    
    clf = MultinomialNB(alpha=1.0)
    
    scorce = cross_validate(clf, X, sentiment , scoring='accuracy')
    print(scorce)
    
NaiveBayes()
    
    