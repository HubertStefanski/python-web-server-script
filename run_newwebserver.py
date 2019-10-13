#!/usr/bin/env python3
# Python 3 AWS api
import boto3

# HTTP request handler
import requests

# regular expression operations
import re

# library to accept command line arguments
import sys

# Import instance and bucket handlers 
import instance_handler
from bucket_handler import *

# Import for feedback highlighting
from termcolor import colored

# Import time for timestamp-based name creation
import time

# Create a timestamp to give UID to each component
timestamp = time.strftime("%Y%m%d-%H%M")

# Set Url var to argument from command else
try:
    resourceURL = sys.argv[1]
except IndexError:
    print(colored('resource not found, setting to default image','red'))
    resourceURL = "http://www.infinitecat.com/archive18/cute18/finger-on-cat-nose.jpg"

# Perform internet connectivity check
def checkConnectionToResource(url):
    reqUrl = url
    
    def sendRequest(reqUrl,timeout=5):
        try:
            _ = requests.get(reqUrl,timeout=timeout)
            return True
        except requests.ConnectionError:
            return False
   
    if(sendRequest(url)== True ):
         print(colored('Internet connection to: ' + url +' is up','green'))

    if(sendRequest(url) == False):
        print(colored('Internet connection to : ' + url + ' is down Ensure Internet connectivity','red', attrs=['bold']))   
        print(colored('Quiting System','magenta'))
        sys.exit(0)
        
# Check Internet connection
checkConnectionToResource('http://google.com/') 

# Call bucket handler to create new Bucket
checkConnectionToResource(resourceURL)
createBucket(timestamp)
print(colored('Pulling image down from : ' + resourceURL,'cyan'))
pullImageFromURL(resourceURL)


# Call instance handler to create new instance and run http server
instance_handler.createEC2Instance()
