#!/usr/bin/python

import json
import subprocess, time, re
import urllib
import urllib2

class NameComDomain:
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

    def get_account(self):
        """get name.com account info"""
        #print "Trying to get account information ..."
        PATH = self.BASE_URL + "account/get"
        req = urllib2.Request(PATH)
        req.add_header('Api-Session-Token', self.session_token)

        res = urllib2.urlopen(req).read()
        obj = json.loads(res)
        if obj["result"]["code"] == 100:
            print "Account information get successfully!"

    def list_domain(self):
        """list the current available domains"""
        PATH = self.BASE_URL + "domain/list"
        req = urllib2.Request(PATH)
        req.add_header('Api-Session-Token', self.session_token)

        res = urllib2.urlopen(req).read()
        #print res

    def dns_records(self):
        """list the current available domains"""
        PATH = self.BASE_URL + "dns/list/bluezd.info"
        req = urllib2.Request(PATH)
        req.add_header('Api-Session-Token', self.session_token)

        res = urllib2.urlopen(req).read()
        obj = json.loads(res)
        records = obj["records"]

        return records

        i = 0
        while i < len(obj["records"]):
            #print obj[i]
            print records[i]["name"], records[i]["content"]
            if records[i]["name"] == 'www.bluezd.info':
                #print records[i]["name"], records[i]["content"]
                pass
            i += 1

    def del_dnsrecords(self, record_id):
        """delete the existing dns record"""
        PATH = self.BASE_URL + "dns/delete/bluezd.info"
        req = urllib2.Request(PATH)
        req.add_header('Api-Session-Token', self.session_token)

        records = dict()
        records["record_id"] = record_id

        data = json.dumps(records)
        response = urllib2.urlopen(req, data).read()
        obj = json.loads(response)
        if obj["result"]["code"] == 100:
            print "Delete record Successfully!"

    def add_dnsrecords(self, domain_name, ip_addr):
        """add a new dns record"""
        PATH = self.BASE_URL + "dns/create/bluezd.info"
        req = urllib2.Request(PATH)
        req.add_header('Api-Session-Token', self.session_token)

        records = dict()
        records["hostname"] = domain_name
        records["type"] = "A"
        records["content"] = ip_addr
        records["ttl"] = 300
        records["priority"] = "N/A"

        data = json.dumps(records)
        response = urllib2.urlopen(req, data).read()
        obj = json.loads(response)
        if obj["result"]["code"] == 100:
            print "Add record Successfully!"
        else:
            print response
    
def main():
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
        #namecom.add_dnsrecords("home-ddns", "1.1.1.1")

if __name__ == '__main__':
    main()
