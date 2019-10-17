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

# Variables

instIP = ''
keyName = 'new_web_server_key'
bucketName = 'web-server-bucket-' + timestamp
resourceName = 'resource-' + timestamp + '.jpg'
resourceS3URL = 'https://s3-eu-west-1.amazonaws.com/'+ bucketName +'/'+ resourceName
userName = 'ec2-user'


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

def WaitForConnection(url):
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
        WaitForConnection(url)
    if(sendRequest(reqUrl) == True):
        print(colored('Connection to resource gained','green'))

# Check Internet connection
checkConnectionToResource('http://google.com/')

# Call bucket handler to create new Bucket
checkConnectionToResource(resourceURL)
createBucket(bucketName)
print(colored('Pulling image down from : ' + resourceURL, 'cyan'))
pullImageFromURL(resourceURL, resourceName)
print(colored('Putting image to Bucket : ' + bucketName, 'cyan'))

putImageToBucket(bucketName,resourceName,None)


# Call instance handler to create new instance and run http server
instance_handler.createEC2Instance()
for i in instance_handler.ec2.instances.all():
    instList = [i.public_ip_address]
    # instanceIP = instList[-1]
    instIP = str(instList[-1])
    print(instIP)

instanceHTTP = 'http://'+instIP

WaitForConnection(instanceHTTP)
checkConnectionToResource(resourceS3URL)
print(colored('running ssh connection to setup index','blue'))
ssh_handler.startSSHConnection(userName,instIP,resourceS3URL,'new_web_server_key.pem','''
        sudo touch /var/www/html/index.html
        sudo chown ec2-user /var/www/html/index.html
        sudo echo '<img src ="''' + resourceS3URL + '''" alt = "resourcePicture">' >> /var/www/html/index.html
        exit
        ''' )
print(colored('running ssh connection to retrieve meta-data','blue'))
ssh_handler.startSSHConnection(userName,instIP,resourceS3URL,'new_web_server_key.pem','''
        sudo curl http://169.254.169.254/latest/meta-data/public-hostname >> /var/www/html/index.html
        exit
        ''' )