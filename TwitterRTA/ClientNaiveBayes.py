#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 19:31:26 2018

@author: yiqian
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 13:23:43 2018

@author: kailinghuang
"""

import socket
import sys
import joblib
import socketserver

from socketserver import ThreadingTCPServer
import threading
import time


model = joblib.load("NaiveBayes_BagofWord.pkl")            

class TimeCount(threading.Thread):

    count = 0
    def run(self):
        while True:
            print('server has run: ' + str(self.count) + 's' )

            time.sleep(10)
            self.count += 10

class MyTCPHandler(socketserver.BaseRequestHandler):      
    
    def handle(self):
        
        self.data=self.request.recv(1024).decode()
        self.data=self.data.split("\n")
        print(self.data)
        
        
        self.request.sendall(('get message'.encode()))


if __name__ == "__main__":
    
    #DB = {}
    #queue = []
    
    """
    size: the DB size of server
    protocol: the protocol use to transport
    """
    
    protocol = 'TCP'
    host = 'localhost'
    portTCP = 5555
    

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
    
    
    """
    TCP server thread
    """
    server = ThreadingTCPServer((host, portTCP), MyTCPHandler)
    server_thread = threading.Thread(target = server.serve_forever)
    server_thread.start()        
    
    messageTCP = "------------------TCP Start---------------------\n\
    | host:            " + host + "\n\
    | TCP port:        " + str(portTCP) + "\n"
    
    print(messageTCP)

        
    
