#!/usr/bin/env python3

# HTTP request handler
import requests

# regular expression operations
import re

# Import for feedback highlighting
from termcolor import colored

# Import time librarby for sleep method
import time


def sendRequest(reqUrl, timeout=20):
    # send get request to specified url, allow for 20 seconds of timeout (Account for slower connections) 
    try:
        _ = requests.get(reqUrl, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False

# Perform internet connectivity check by get request for specified url
# Return True if connection is up
# Return False and quit system if connection is down
def checkConnectionToResource(url):
    if(sendRequest(url) == True):
        print(colored('Internet connection to: ' + url + ' is up', 'green'))

    if(sendRequest(url) == False):
        print(colored('Internet connection to : ' + url +
                      ' is down Ensure Internet connectivity', 'red', attrs=['bold']))
        print(colored('Quiting System', 'magenta'))
        sys.exit(0)

# Perform internet connectivity check trough get request and wait until connection is up, sleep if false for set time
def WaitForConnection(url):

    if(sendRequest(url) == False):
        print(colored('Waiting for resource to become available','magenta'))
        time.sleep(5)
        WaitForConnection(url)
    if(sendRequest(url) == True):
        print(colored('Connection to resource gained','green'))
