#!/usr/bin/env python3
# Python 3 AWS api
import boto3

# HTTP request handler
import requests

# regular expression operations
import re

# library to accept command line arguments
import sys

# Import instance, bucket and ssh handlers
import instance_handler
from bucket_handler import *
import ssh_handler

# Import for feedback highlighting
from termcolor import colored

# Import time for timestamp-based name creation
import time

# Create a timestamp to give UID to each component
timestamp = time.strftime("%Y%m%d-%H%M")

instIP = ''
keyName = 'new_web_server_key'
resourceURL = 's3://web-server-bucket-' + timestamp + '/resource-' + timestamp + '.jpg'

# Set Url var to argument from command else
try:
    resourceURL = sys.argv[1]
except IndexError:
    print(colored('resource not found, setting to default image', 'red'))
    resourceURL = "http://www.infinitecat.com/archive18/cute18/finger-on-cat-nose.jpg"

# Perform internet connectivity check


def checkConnectionToResource(url):
    reqUrl = url

    def sendRequest(reqUrl, timeout=20):
        try:
            _ = requests.get(reqUrl, timeout=timeout)
            return True
        except requests.ConnectionError:
            return False

    if(sendRequest(url) == True):
        print(colored('Internet connection to: ' + url + ' is up', 'green'))

    if(sendRequest(url) == False):
        print(colored('Internet connection to : ' + url +
                      ' is down Ensure Internet connectivity', 'red', attrs=['bold']))
        print(colored('Quiting System', 'magenta'))
        sys.exit(0)

def waitForResource(url):
    reqUrl = url
    def sendRequest(reqUrl, timeout=5):
        try:
            _ = requests.get(reqUrl, timeout=timeout)
            return True
        except requests.ConnectionError:
            return False
    if(sendRequest(reqUrl) == False):
        print(colored('Waiting for resource to become available','magenta'))
        time.sleep(5)
        waitForResource(url)
    if(sendRequest(reqUrl) == True):
        print(colored('Connection to resource gained','green'))

# Check Internet connection
checkConnectionToResource('http://google.com/')

# Call bucket handler to create new Bucket
checkConnectionToResource(resourceURL)
createBucket('web-server-bucket-' + timestamp)
print(colored('Pulling image down from : ' + resourceURL, 'cyan'))
pullImageFromURL(resourceURL, 'resource-'+ timestamp + '.jpg')
print(colored('Putting image to Bucket', 'cyan'))

# wait for bucket to setup, avoid putting to non-existent bucket
time.sleep(10)

putImageToBucket('web-server-bucket-' + timestamp,
                 'resource-' + timestamp + '.jpg')


# Call instance handler to create new instance and run http server
instance_handler.createEC2Instance()
for i in instance_handler.ec2.instances.all():
    instList = [i.public_ip_address]
    # instanceIP = instList[-1]
    instIP = str(instList[-1])
    print(instIP)

waitForResource('http://'+instIP)
print(colored('running ssh connection','blue'))
ssh_handler.startSSHConnection('ec2-user',instIP,resourceURL,'new_web_server_key.pem' )
