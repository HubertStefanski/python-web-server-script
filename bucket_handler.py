#!/usr/bin/env python3
import sys
import boto3
from termcolor import colored
import requests
from botocore.exceptions import ClientError
#from urllib3.request import urlretrieve
s3 = boto3.resource('s3')
s3client = boto3.client('s3')

#create new s3 Bucket with timestamp as UID
def createBucket(bucketName):
    print(colored('Creating new Bucket','blue'))
    try:
        response = s3.create_bucket(Bucket=bucketName, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
        print (colored(response, 'yellow'))
    except Exception as error:
        print (colored(error,'red'))
        

def pullImageFromURL(url,fileName):
    r = requests.get(url, allow_redirects=True)
    open(fileName, 'wb').write(r.content)

def putImageToBucket(bucketName,fileName,object_name = None):
    if object_name is None:
        object_name = fileName
    try:
        s3client.upload_file(fileName,bucketName,object_name,ExtraArgs={'ACL':'public-read'})
    except ClientError as e:
        logging.error(e)
        return False
    return True

def getResourceBucketURL(timestamp):
    print(colored('s3://web-server-bucket-'+ timestamp +'/resource-' + timestamp +'.jpg','red',attrs=['bold']))
    return 's3://web-server-bucket-'+ timestamp +'/resource-' + timestamp +'.jpg'

# TODO
def bucketExists():
    print(colored('Available buckets','cyan'))
    for bucket in s3.buckets.all():
        print (colored(bucket.name,'cyan'))
    if (len(s3client.list_buckets()) < 2):
        return True
        print('true')
    else:
        print('false')
        return False
        
# TODO       
def chooseBucketOrCreateIfNoneExist(bucketName):
    bucketList = []
    if (bucketExists() == True):
        for bucket in s3.buckets.all():
           bucketList.append(bucket)
        bucketName = str(bucketList[-1].name)
        print(bucketName)
        return str(bucketName)  
    if(bucketExists() == False):
         print(bucketName)
         createBucket(bucketName)
    
   