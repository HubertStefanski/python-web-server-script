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
import bucket_handler

# Import for feedback highlighting
from termcolor import colored

# Import time for timestamp-based name creation
import time

# Create a timestamp to give UID to each component
timestamp = time.strftime("%Y%m%d-%H%M")

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
         print(colored('Internet connection is Up','green'))

    if(sendRequest(url) == False):
        print(colored('Internet connection to : ' + url + ' is down Ensure Internet connectivity','red', attrs=['bold']))   
        print(colored('Quiting System','magenta'))
        sys.exit(0)
        
# Check Internet connection
checkConnectionToResource('http://google.com/') 

# Call bucket handler to create new Bucket
bucket_handler.createBucket('web_bucket' + timestamp )


# Call instance handler to create new instance and run http server
instance_handler.createEC2Instance()
