#!/usr/bin/env python3

import socket
from multiprocessing import Process
import os


class StudyServer():
    def __init__(self):
        self.study_server = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
    

    def bind(self,port):
        self.study_server.bind(('',port))
        print ('*' * 20)
        print ('监听端口为 :',port)
        print('*' * 20)

    def startServer(self):
        
        self.study_server.listen(128)

        while True:
            client_socket ,client_address = self.study_server.accept()
            print ('客户端地址 ：',client_address)
            handle_process = Process(target=self.handle_client,args=(client_socket,))
            handle_process.start()
            client_socket.close()

    def handle_client(self,client_socket):
        receive_data = client_socket.recv()
        receive_str = receive_data.decode()
        receive_lines = receive_str.splitlines()
        print('*' * 15,'请求内容','*'*15)

        for line in receive_lines:
            print (line)
        print('*' * 15, '请求内容', '*'*15)

        print ('\nheader =',receive_lines[0])

    
