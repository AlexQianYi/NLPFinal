#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 11:53:49 2018

@author: yiqian
"""

import socketserver
import socket
import re

from socketserver import ThreadingTCPServer
import threading
import time

from GetTweetAPI import getTweet


        
class TimeCount(threading.Thread):

    count = 0
    def run(self):
        while True:
            print('server has run: ' + str(self.count) + 's' )
            time.sleep(10)
            self.count += 10
            
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


if __name__ == "__main__":
    
    protocol = 'TCP'
    host = 'localhost'
    portTCP = 5555
    
    
    helpmessage1= "------------Parameter List---------------"
    para_host   = "| host:(str)  # the host of server"
    para_portTCP= "| TCPport:(int)  # port of TCP server"
    helpmessage2= "========================================="        
    
    print(helpmessage1)
    print(para_host)
    print(para_portTCP)
    print(helpmessage2)        
    
    """
    Time count thread
    """
    count_thread = TimeCount()
    count_thread.start()
    
    print('Please input the Keyword in Tweet')
    keyword = input()
    preTweet = ""
    while True:
        count = 1

        Tweets = getTweet(keyword, count)
        if len(Tweets)>0:
            if Tweets == preTweet:
                print('no new Tweet..................')
                time.sleep(5)
            else:
                print(Tweets)
                preTweet = Tweets
                addrTCP = (host, portTCP)
                
                client = socket.socket()
                client.connect(addrTCP)
                
                Tweet = PreProTweet(Tweets[0])
                client.send((Tweet).encode())
                message=client.recv(1024).decode()
                print(message)
                time.sleep(5)
        else:
            print('no new Tweet..................')
            time.sleep(5)
    

        
    
