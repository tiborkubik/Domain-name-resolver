#!/usr/bin/env python3

# # # Project #1 for IPK: Socket Server Programming
# # # Author: Tibor Kubik (xkubik34)

import socket
import sys
import re

# Function validates input port
def argsValidity():
    if len(sys.argv) == 2:
        port = sys.argv[1]
        if port.isdigit():
            port = int(sys.argv[1])
            return True
        else:
            return False
    else:
        return False

# Function checks if given string is IP
def isIpv4(input_ip):
    pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    test = pat.match(input_ip)
    if test:
       return True
    else:
       return False

# Funciton validates domain names
def isDomainName(input_name):
    pat = re.compile("^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$")
    test = pat.match(input_name)
    if test:
       return True
    else:
       return False

# Function resolves a demand for GET
def resolve_line_get(name_, type_, ret_data):
    if(type_ == "A"):   # type=A
        try:
            ip_addr = socket.gethostbyname(name_)
            ret_data += " 200 OK\r\n\r\n"
            ret_data += name_ + ":" + type_ + "=" + ip_addr + "\r\n"
        except:
            ret_data += " 404 Not Found\r\n\r\n"
    elif(type_ == "PTR"):   # type=B
        try:
            dom_addr = socket.gethostbyaddr(name_)
            ret_data += " 200 OK\r\n\r\n"
            ret_data += name_ + ":" + type_ + "=" + dom_addr[0] + "\r\n"
        except:
            ret_data += " 404 Not Found\r\n\r\n"
    else:
        ret_data += " 400 Bad Request\r\n\r\n"
    return ret_data

# Function resolves a demand for POST
def resolve_line_post(name_, type_, ret_data):
    error = 0
    if(type_ == "A"):   # type=A
        try:
            ip_addr = socket.gethostbyname(name_)
            ret_data += name_ + ":" + type_ + "=" + ip_addr + "\r\n"
        except:
            error = 404
    elif(type_ == "PTR"):   # type=PTR
        try:
            dom_addr = socket.gethostbyaddr(name_)
            ret_data += name_ + ":" + type_ + "=" + dom_addr[0] + "\r\n"
        except:
            error = 404
    else:
        error = 404
    return ret_data, error

# Main function
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('127.0.0.1', int(sys.argv[1]))) # Host will be always localhost, Port to listen on (non-privileged ports are > 1023)
            s.listen()
            while True:
                conn, addr = s.accept()
                data = conn.recv(1024)
                if not data:
                    break

                parsed_data = data.decode("utf-8")                  # Getting input from client into string
                rec_request = parsed_data.split('\r\n', 1)[0]       # First line of input from client, you find method, request etc there
                request_split = rec_request.split()                 # Splits first line into list

                # Getting partial information, such as method, request and protocol
                method = request_split[0]          # e.g GET
                req = request_split[1]             # e.g /resolve?name=www.fit.vutbr.cz&type=A
                http_met = request_split[2]        # e.g HTTP/1.1

                ret_data = http_met                # This string will be returned to client starting with protocol in header

                # GET method part
                if(rec_request.find("GET") == 0):
                    try:
                        r1 = re.findall(r"/resolve?", req)
                        val_url_ = r1[0]
                        r2 = re.findall(r"name=[^&]*", req)
                        name_full_ = r2[0]
                        r3 = re.findall(r"type=\S*", req)
                        type_full_ = r3[0]
                    except:
                        ret_data += " 400 Bad Request\r\n\r\n"
                        conn.sendall(ret_data.encode("utf-8"))
                        conn.shutdown(socket.SHUT_WR)
                        continue

                    name_ = name_full_[5:]              # parsing from name=example.com just "example.com"
                    type_ = type_full_[5:]              # parsing from type=A just "A"

                    if(isIpv4(name_) == False and isDomainName(name_) == False):        # given name is neither IP nor domain
                        ret_data += " 400 Bad Request\r\n\r\n"
                    elif(isIpv4(name_) == True and type_ == "A"):                       # given name is IP and type is A -> Bad request
                        ret_data += " 400 Bad Request\r\n\r\n"
                    elif(isDomainName(name_) == True and type_ == "PTR"):               # given name is a domain and type is PTR -> Bad request
                        ret_data += " 400 Bad Request\r\n\r\n"
                    else:
                        ret_data = resolve_line_get(name_, type_, ret_data)

                # POST method part
                elif(rec_request.find("POST") == 0):
                    input_lines_list = parsed_data.splitlines()

                    if (req != "/dns-query"):
                        ret_data += " 400 Bad Request\r\n\r\n"
                        conn.sendall(ret_data.encode("utf-8"))
                        conn.shutdown(socket.SHUT_WR)
                        continue

                    post_ret = ""
                    errorCode = 0
                    returnErr = 0
                    return_codes = []

                    # We can skip 7 lines as there are not requests to resolve, just info from curl
                    for index, line in enumerate(input_lines_list[7:]):

                        # skipping last line if its empty
                        x = index+1
                        if(x == len(input_lines_list[7:]) and not line.strip()):
                            break
                        try:
                            line = line.strip()
                            r1 = re.findall(r"^[^(:|\s)]*", line)
                            name_ = r1[0]
                            r2 = line.split(':')[-1]
                            r2 = r2.strip()
                            if(r2 == "A" or r2 == "PTR"):
                                type_ = r2
                            else:
                                errorCode = 400
                                continue

                            if(isIpv4(name_) == False and isDomainName(name_) == False):        # given name is neither IP nor domain
                                errorCode = 400
                            elif(isIpv4(name_) == True and type_ == "A"):                       # given name is IP and type is A -> Bad request
                                errorCode = 400
                            elif(isDomainName(name_) == True and type_ == "PTR"):               # given name is a domain and type is PTR -> Bad request
                                errorCode = 400
                            else:
                                post_ret, errorCode = resolve_line_post(name_, type_, post_ret)
                        except:
                            errorCode = 400

                        return_codes.append(errorCode)

                    if (0 in return_codes):
                        ret_data += " 200 OK\r\n\r\n"
                    elif (400 in return_codes and 0 not in return_codes):
                        ret_data += " 400 Bad Request\r\n\r\n"
                    elif(404 in return_codes and 0 not in return_codes):
                        ret_data += " 404 Not Found\r\n\r\n"
                    else:
                        ret_data += " 400 Bad Request\r\n\r\n"

                    ret_data += post_ret
                else:
                    ret_data += "405 Method not allowed\r\n\r\n"

                conn.sendall(ret_data.encode("utf-8"))
                conn.shutdown(socket.SHUT_WR)

        except KeyboardInterrupt:
            print("Interrupt received, stopping.")
        finally:
            s.close()

# # # ___main___
if not argsValidity():
    sys.stderr.write("Error: Invalid arguments.\n")
    exit(-1)

main()
