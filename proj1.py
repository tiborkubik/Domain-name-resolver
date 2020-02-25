#!/usr/bin/env python3

import socket
import sys
import re

def args_check():
    if len(sys.argv) == 2:
        port = sys.argv[1]
        if port.isdigit():
            port = int(sys.argv[1])
            return True
        else:
            return False
    else:
        return False

args_valid = args_check()

if args_valid == False:
    sys.stderr.write("Error: Invalid arguments.\n")
    exit(-1)

HOST = '127.0.0.1'       # Host will be always localhost
PORT = int(sys.argv[1])  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    conn, addr = s.accept()

    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break

            parsed_data = data.decode("utf-8")
            rec_request = parsed_data.split('\n', 1)[0]

            print(rec_request)

            if(rec_request.find("GET") == 0):
                print("-----------Valid, starting with GET!\n")
                #TODO
            elif(rec_request.find("POST") == 0):
                print("-----------Valid, starting with POST!\n")
                #TODO
            else:
                conn.sendall(b'400 Bad Request')

            #conn.sendall(data)

    conn.close()
