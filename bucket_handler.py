#!/usr/bin/env python3
import sys
import boto3
from termcolor import colored
import requests
from botocore.exceptions import ClientError
#from urllib3.request import urlretrieve
s3 = boto3.resource('s3')
s3client = boto3.client('s3')

#create new s3 Bucket with provided name from method Call
def createBucket(bucketName):
    print(colored('Creating new Bucket','blue'))
    try:
        response = s3.create_bucket(Bucket=bucketName, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
        print (colored(response, 'yellow'))
    except Exception as error:
        print (colored(error,'red'))
        
# Downlaod image to local folder from provided URL and save as provided filename
def pullImageFromURL(url,fileName):
    r = requests.get(url, allow_redirects=True)
    open(fileName, 'wb').write(r.content)

# Upload image to s3 bucket created previously with provided parameters
def putImageToBucket(bucketName,fileName,object_name = None):
    if object_name is None:
        object_name = fileName #name the object same as filename
    try:
        s3client.upload_file(fileName,bucketName,object_name,ExtraArgs={'ACL':'public-read'}) # give access for public to read file (neccessary for accessing without key)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# Retun the URL of newly uploaded file  
def getResourceBucketURL(timestamp):
    print(colored('s3://web-server-bucket-'+ timestamp +'/resource-' + timestamp +'.jpg','red',attrs=['bold']))
    return 's3://web-server-bucket-'+ timestamp +'/resource-' + timestamp +'.jpg'

# TODO
# Check for existing buckets apart from user default bucket provided by rossettaHub
def bucketExists():
    print(colored('Available buckets','cyan'))
    for bucket in s3.buckets.all():
        print (colored(bucket.name,'cyan'))
    if (len(s3client.list_buckets()) < 2): # if buckets exists then return true
        return True
        print('true')
    else:
        print('false')  # else return false if no buckets exist apart from default
        return False
        
# TODO       
# If buckets exists then use most recent bucket in the collection of buckets and 
# return the bucket name to variable so that file can be uploaded
# prevents waste of resources by reusing existing buckets
# if bucketExists() returns as false then create a new bucket and use the name as provided
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
    
   