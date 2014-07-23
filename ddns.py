#!/usr/bin/python
#-*- coding:utf-8 -*-

import socket
import time
from NameCom import NameComDomain, ddns_namecom

def getip():
    sock = socket.create_connection(('ns1.dnspod.net', 6666))
    ip = sock.recv(16)
    sock.close()
    return ip

if __name__ == '__main__':
    current_ip = None

    while True:
        try:
            ip = getip()
            if current_ip != ip:
                if ddns_namecom(ip):
                    current_ip = ip
        except Exception, e:
            print e
            pass
        time.sleep(3600)
