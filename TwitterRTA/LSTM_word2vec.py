# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 17:21:33 2018

@author: q5638
"""

from sklearn.model_selection import train_test_split
from gensim.models.word2vec import Word2Vec
from gensim.corpora.dictionary import Dictionary

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

# create word dictionary
def create_dictionary(w2v_model):
    dic = Dictionary()
    dic.doc2bow(w2v_model.wv.vocab.keys(), allow_update=True)
    w2index = {v:k+1 for k, v in dic.items()}
    w2vec = {word: w2v_model[word] for word in w2index.keys()}
    return w2index, w2vec

dataframe = pd.read_csv('training.1600000.processed.noemoticon.csv', \
                        encoding = "ISO-8859-1", header=None).iloc[:, [0, 2, 5]].sample(frac=1).reset_index(drop=True)

def splitText(text):
    
    sentences = []
    for tweet in text:
        s = tweet.split(' ')
        sentences.append(s)
    return sentences

ratio = 0.7                       # train test is 70%, test is 30%
size = 1600000

Dates = np.array(dataframe.iloc[:, 1].values)
Tweets = dataframe.iloc[:, 2].apply(PreProTweet).values
Sentiment = np.array(dataframe.iloc[:, 0].values)

Tweets = splitText(Tweets)

#Xtrain, Xtest, ytrain, ytest = train_test_split(Tweets, Sentiment, test_size = 1-ratio)

# dimension
nDim = 100

# initial model and build vocab
w2vModel = Word2Vec(Tweets, size=nDim, min_count = 10)
w2vModel.save('Word2Vec.model')     #save model

index_dict, word_vectors = create_dictionary(w2vModel)


from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.layers.embeddings import Embedding
from keras.layers.core import Dense, Dropout, Activation


# parameter
vocab_dim = 100
textLen = 140
batch_size = 32
n_epoch = 3
input_length = 140

def LSTMNetWork(p_n_symbols, p_embedding_weights, p_X_train, p_y_train, p_X_test, p_y_test):
    print('-----create LSTM model-----')
    
    model = Sequential()
    # input layer
    model.add(Embedding(output_dim=vocab_dim,
                        input_dim=p_n_symbols,
                        mask_zero=True,
                        weights=[p_embedding_weights],
                        input_length=input_length))
    
    # LSTM layer
    model.add(LSTM(output_dim=50,
                   activation='sigmoid',
                   inner_activation='hard_sigmoid'))
    
    # dropout
    model.add(Dropout(0,5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    
    # compile model
    print('---compile model---')
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    
    # train model
    print('---train model---')
    model.fit(p_X_train, p_y_train, batch_size=batch_size,
              nb_epoch=n_epoch, validation_data=(p_X_test, p_y_test))
    
    # save model
    print('save model as "LSTM_Word2Vec.m"')
    model.save('LSTM_Word2Vec.m')
    
    # evaluate model
    print('---evaluate model---')
    score, acc = model.evaluate(p_X_test, p_y_test, batch_size=batch_size)
    print('score is', score)
    print('acc is', acc)


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

from keras.preprocessing import sequence

# padding train set and test set
Xtrain = sequence.pad_sequences(Xtrain, maxlen = textLen, value = 0.0)
Xtest = sequence.pad_sequences(Xtest, maxlen = textLen, value = 0.0)

print(len(Xtrain[0]), len(Xtest[0]))

LSTMNetWork(n_symbols, embedding_weights, Xtrain, ytrain, Xtest, ytest)