#!/usr/bin/env python3
import sys
import boto3
from termcolor import colored
import requests
#from urllib3.request import urlretrieve


#create new s3 Bucket with timestamp as UID
def createBucket(bucketName):
    s3 = boto3.resource("s3")
    print(colored('Creating new Bucket','blue'))
    try:
        response = s3.create_bucket(Bucket=bucketName, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
        print (colored(response, 'yellow'))
    except Exception as error:
        print (colored(error,'red'))
        

def pullImageFromURL(url,fileName):
    r = requests.get(url, allow_redirects=True)
    open(fileName, 'wb').write(r.content)

def putImageToBucket(bucketName,fileName):
    s3 = boto3.resource('s3')
    try:
        response = s3.Object(bucketName,fileName).put(
            Body = open(fileName,'rb'))
        print(response)
    except Exception as error:
        print(error)

def getResourceBucketURL(timestamp):
    print(colored('s3://web-server-bucket-'+ timestamp +'/resource-' + timestamp +'.jpg','red',attrs=['bold']))
    return 's3://web-server-bucket-'+ timestamp +'/resource-' + timestamp +'.jpg'