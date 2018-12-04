#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 11:53:49 2018

@author: yiqian
"""




import socketserver
import socket

from socketserver import ThreadingTCPServer
import threading
import time

from GetTweetAPI import SearchTwitter
        
class TimeCount(threading.Thread):

    count = 0
    def run(self):
        while True:
            print('server has run: ' + str(self.count) + 's' )
            time.sleep(10)
            self.count += 10

"""
class MyTCPHandler(socketserver.BaseRequestHandler):      
    
    def handle(self):
        
        #self.data=self.request.recv(1024).decode()
        #self.data=self.data.split("\n")
        
        print('Please input the KeyWord of Tweet: ')
        keyWord = input()
        print('Please wait .... (if you want to stop, enter "S")')
        #flag = True
        
        message = keyWord
        self.request.sendall(message.encode())

        while flag:
            
            Tweets = SearchTwitter(keyWord)
            for tweet in Tweets:
                self.request.sendall(tweet.encode())
                message=client.recv(1024).decode()
                print(tweet, message)
        """


if __name__ == "__main__":
    
    protocol = 'TCP'
    host = 'localhost'
    portTCP = 5555
    
    addrTCP = (host, portTCP)
    
    client = socket.socket()
    client.connect(addrTCP)
    count = 4
    while count>0:
        tweet = input()
        
        client.send((tweet).encode())
        message=client.recv(1024).decode()
        print("message")
        count -= 1
    

    dic_para = {'size':'5', 'protocol':'TCP'}
                
    helpmessage1= "------------Parameter List---------------"
    para_size   = "| size:(int)  # the size of DB"
    para_host   = "| host:(str)  # the host of server"
    para_portTCP= "| TCPport:(int)  # port of TCP server"
    para_portUDP= "| UDPport:(int)  # port of UDP server"
    para_evi    = "| eviction:(str)[FIFO, Random, LRU] # the eviction policy"
    helpmessage2= "========================================="        
    
    print(helpmessage1)
    print(para_size)
    print(para_host)
    print(para_portTCP)
    print(para_portUDP)
    print(para_evi)
    print(helpmessage2)        
    
    """
    Time count thread
    """
    count_thread = TimeCount()
    count_thread.start()
    

        
    
