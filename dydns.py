#!/usr/bin/env python
import subprocess
import time
import re

hostname = ""
key = ""

sleep = 30 # number of seconds between each check
errCount = 0
maxErr = 10 # after this many errors email
url = "{0}:{1}@dyn.dns.he.net/nic/update?hostname={0}".format(hostname,key)
ip = '!' # need something here for regex first check

while True:
    ifcfg = subprocess.check_output(["ifconfig"])
    haveIt = re.search(ip,ifcfg)
    if (not haveIt):
        try:
            if errCount == maxErr:
                print("WEWE this should email")
                pass

            res = subprocess.check_output(["curl", "-6", "-s", url ])
            if res == 'abuse':
                sleep += 15
                print("abuse, slowing down - sleep : {0}".format(sleep))
                pass
            (status, ip) = res.split(' ')
            if status == 'good':
                errCount = 0
                print("IP address is now {0}".format(ip))
            elif status == 'nochg':
                print("curl IP address did not change: {0}".format(ip))
            else:
                print("Unknown status {0} ip {1}".format(status,ip))
        except:
                errCount += 1
                print("No network connection: {0}".format(res))
    else:
        print("regex IP address did not change: {0}".format(ip))
    time.sleep(sleep)
