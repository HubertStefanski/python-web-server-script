#!/usr/bin/env python3
import sys
import boto3
from termcolor import colored


def createBucket(bucketName):
    s3 = boto3.resource("s3")
    print(colored('Creating new Bucket','blue'))
    try:
        response = s3.create_bucket(Bucket=bucketName, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
        print (colored(response, 'yellow'))
    except Exception as error:
        print (colored(error,'red'))
        

