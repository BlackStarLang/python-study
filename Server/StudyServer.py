#!/usr/bin/env python3

import socket
from multiprocessing import Process
import os
import re

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
        receive_data = client_socket.recv(1024)
        receive_str = receive_data.decode('utf-8')
        receive_lines = receive_str.splitlines()
       
        print('*' * 15, 'header', '*'*15)
        header_line = receive_lines[0]
        print ('\nheader =',header_line)
        print('*' * 15, 'header', '*'*15)
    
        match_result = re.match(r'\w+ +/([^ ]*)',header_line)
        file_name = match_result.group(1)
        cwd = os.getcwd()
        file_path = os.path.join(cwd, 'html',file_name)
        print('cwd = ',cwd,'file path =',file_path)
       
        if file_path.endswith('.html') or file_path.endswith('.css'):

            try:
                send_file_data = open(file_path, 'rb')

                response_start_line = 'HTTP/1.1 200 OK \n'
                response_header = 'Server: Study Server \n'
                response_body = send_file_data.read().decode('utf-8')

            except IOError as identifier:
                print ('读取文件错误：',identifier)
                response_start_line = 'HTTP/1.1 404 Not Found \n'
                response_header = 'Server: Study Server \n'
                response_body = 'file not found'
            finally:
                send_file_data.close()
                            
            response_data='%s%s\r\n%s' % (response_start_line,response_header,response_body)
            print(response_data)

            client_socket.send(response_data.encode('utf-8'))
            client_socket.close()


def main():
    study_server = StudyServer()
    study_server.bind(8000)
    study_server.startServer()


if __name__ == '__main__':
    main()
