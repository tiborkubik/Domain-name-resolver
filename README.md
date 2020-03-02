
# Project 1 for IPK course ([Computer Communications and Networks](https://www.fit.vut.cz/study/course/13334/.en))

**Author:** Tibor Kubik
**Contact mail:** xkubik34@stud.fit.vutbr.cz

The aim of this project is to to implement a server which will be able to resolve domain names. For this purpose two methods will be garanted: **GET** and **POST**.

## Implementation details

I have decided to use Python of version 3.6 to solve this project. For the server implementation `socket` library was used. For getting the input and for its validity, libraries `sys` and `re` were used.

## Main idea of my approach to the solution

After argument validation, I have initialized the server using functions from aforementioned `socket` library. After decoding the input I parsed the request from client. Then I made a decision tree to distinguish whether the input method is `GET`, `POST` or other. If it was either GET nor POST, error code and message was sent to client. To get the type, input address/name I used the strength of regular expressions.
There are 2 types of resolving: **A** and **PTR**. I used functions `gethostbyname()` and `gethostbyaddr()` for the resolving. 
Server always works on localhost.
When the input from client was proceeded, server is waiting for another requests from (the same or different) client. To interrupt the server operation `Ctr + C` must be pressed.

## Special cases

There are sever special cases that can happen - cases, when server must act somehow special (excluding those mentioned in the assignment)

 - Request is an IP address and type is A. Error 400 is returned.
 - Request is a domain name and type is PTR. Error 400 is returned.
 - Request contains both invalid line(e.g google.com:BLAHBLAH) and an address that was not resolved. 400 Bad Request is returned in this case.
 -  Client asks for following: *curl --data-binary @queries.txt -X POST http://localhost:1500/dns-query -i* where file queries.txt  contains one line with invalid input and then queries.txt is edited and it contains an empty line. For both cases, my program tries to resolve everything and it tries to provide client as much information as possible. It means that it resolves everything what is possible, sends it to client and in mentioned cases(invalid line, empty line) if there is at least one line that was resolved successfuly, error code 200 OK is returned.
 - Repeating lines in body in `POST` method: output is returned to client exactly the same time it was required (excluding invalid input cases).
 - Empty line at the end of input. This line is skipped and does not have effect on return value.

## Conclusion
Working on this project was my first contact with network programming using sockets (actually any network programming). At first I was a little bit lost but after reading some articles and my notes from lectures I found out how to get the desired solution. I tested my implementation on large amount of tests and I am satisfied with the results. I really enjoyed working on it and it has definitely widened my gaze in CS.
