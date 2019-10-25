#!/usr/bin/env python3

#Import system module
import sys

# HTTP request handler
import requests

# regular expression operations
import re

# Import for feedback highlighting
from termcolor import colored

# Import time librarby for sleep method
import time




def sendRequest(reqUrl, timeout = 20):
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
        print(colored(f'Internet connection to: {url} is up', 'green'))
    else:
        print(colored(f'Internet connection to : {url} is down Ensure Internet connectivity', 'red', attrs=['bold']))
        print(colored('Quiting System', 'magenta'))
        sys.exit(0)
attemptCounter = 1

# Perform internet connectivity check trough get request and wait until connection is up, sleep if false for set time
def waitForConnection(url):
   
    def userConfirmContinueAttempts():
        global attemptCounter
        contQuestion = input('Attempt counter exceeded set limit for attempts, continue? (y/n)')
        if(contQuestion.upper() == 'Y'):
            attemptCounter = 0
            waitForConnection(url)
        elif(contQuestion.upper() == 'N'):
            print(colored('Quiting system','magenta'))
            sys.exit(0)
        else:   
            print(colored("Sorry,that didn't work,try again",'red'))
            userConfirmContinueAttempts()
    
    def checkRequest(url):
        global attemptCounter
        if(sendRequest(url) == False):
            time.sleep(5)
            attemptCounter += 1
            if(attemptCounter >= 15):
                userConfirmContinueAttempts()
                attemptCounter = 0
            else:
                waitForConnection(url)
        elif(sendRequest(url) == True):
            print(colored('Connection to resource gained','green'))
    checkRequest(url)
