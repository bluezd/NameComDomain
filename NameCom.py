#!/usr/bin/python

import json
import sys, subprocess, time, re
import urllib
import urllib2

class NameComDomain(object):
    def __init__(self):
        """docstring for __init__"""
        self.BASE_URL = "https://api.name.com/api/"
        self.params = dict()
        self.params['username'] = "bluezhudong@gmail.com"
        self.params['api_token'] = "c838bb6d0718b18b9bbcf6454c6480aaf278d54e"
        self.session_token = None

    def login(self):
        """login the name.com"""
        PATH = self.BASE_URL + "login"

        data = json.dumps(self.params)
        response = urllib.urlopen(PATH, data).read()
        obj = json.loads(response)
        if obj["result"]["code"] == 100:
            print "Login Successfully!"
            self.session_token = obj["session_token"]
            return obj["session_token"]

    def authentication(self, url, data=None):
        """authentication method"""
        PATH = self.BASE_URL + url
        req = urllib2.Request(PATH)
        req.add_header('Api-Session-Token', self.session_token)

        res = urllib2.urlopen(req, data).read()
        obj = json.loads(res)
        if obj["result"]["code"] == 100:
            return obj
        else:
            return False

    def get_account(self):
        """get name.com account info"""
        #print "Trying to get account information ..."
        res = self.authentication('account/get')
        if res:
            print "Account information get successfully!"

    def list_domain(self):
        """list the current available domains"""
        print "Listing the existing domains:"
        res = self.authentication('domain/list')
        if res:
            for i in res["domains"].keys():
                print "->  ""www." + i

    def dns_records(self):
        """list the current available domains"""
        res = self.authentication('dns/list/bluezd.info')
        if res:
            records = res["records"]
            return records

    def del_dnsrecords(self, record_id):
        """delete the existing dns record"""
        records = dict()
        records["record_id"] = record_id
        data = json.dumps(records)

        res = self.authentication('dns/delete/bluezd.info', data)
        if res:
            print "Delete record Successfully!"

    def add_dnsrecords(self, domain_name, ip_addr):
        """add a new dns record"""
        records = dict()
        records["hostname"] = domain_name
        records["type"] = "A"
        records["content"] = ip_addr
        records["ttl"] = 300
        records["priority"] = "N/A"
        data = json.dumps(records)

        res = self.authentication('dns/create/bluezd.info', data)
        if res:
            print "Add record Successfully!"
        else:
            print res
    
def ddns_namecom(ip_addr):
    """main funciton"""
    namecom = NameComDomain()

    res = namecom.login()
    if res:
        namecom.get_account()
        namecom.list_domain()
        records = list()
        records = namecom.dns_records()

        i = 0
        while i < len(records):
            #print records[i]
            #print records[i]["name"], records[i]["content"]

            # check the records
            if records[i]["name"] == "home-ddns.bluezd.info":
                # remove this records
                print "Find the existing record:"
                namecom.del_dnsrecords(records[i]["record_id"])

            i += 1
        # add new dns record
        namecom.add_dnsrecords("home-ddns", ip_addr)

def usage():
    """usage of NameCom.py"""
    print "python NameCom.py <IP address>"
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        ddns_namecom(sys.argv[1])
        sys.exit(0)
    else:
        usage()
