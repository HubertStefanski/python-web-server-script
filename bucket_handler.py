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
        response = s3.create_bucket(Bucket='web-server-bucket-' + bucketName, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
        print (colored(response, 'yellow'))
    except Exception as error:
        print (colored(error,'red'))
        

def pullImageFromURL(url):
    try:
        requests.get(url,'local_image.jpg')
    except FileNotFoundError as error:
        print(error)