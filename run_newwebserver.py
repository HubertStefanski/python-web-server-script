#!/usr/bin/env python3
# Python 3 AWS api
import boto3

# library to accept command line arguments
import sys

# Import for feedback highlighting
from termcolor import colored

# Import handlers
import instance_handler
from bucket_handler import *
from metric_handler import *
import ssh_handler
from network_probe_handler import *

# Import for feedback highlighting
from termcolor import colored

# Import time for timestamp-based name creation
import time

# Create a timestamp to give UID to each component
timestamp = time.strftime("%Y%m%d-%H%M")

metricList = ['CPUUtilization','NetworkIn','NetworkOut']
# Variables
# Create inst vars
amiId ='ami-0ce71448843cb18a1' #  CHANGE TO MOST UP TO DATE WHEN USING
secGroup =['sg-03057cb040ad8642c'] # CHANGE TO OWN SECURITY GROUP
instType = 't2.micro'
keyName = 'new_web_server_key' # CHANGE TO PATH OF USER KEY
usrData = """
             #!/bin/bash                  
             sudo yum update -y
             sudo yum install httpd -y
             sudo systemctl enable httpd
             sudo service httpd start
             """
instTags = [
                    {'Key':'project','Value': 'foo'},
                    {'Key': 'owner', 'Value': 'walter'},
        ]             

# Bucket and S3 Vars
instIP = ''
instID = ''
bucketName = f'web-server-bucket-{timestamp}'
resourceName = f'resource-{timestamp}.jpg'
resourceS3URL = f'https://s3-eu-west-1.amazonaws.com/{bucketName}/{resourceName}'

# SSH Commands and params
userName = 'ec2-user'
getMetaDataCMD = '''
        curl http://169.254.169.254/latest/meta-data >> /var/www/html/index.html
        exit'''
getAmiIDCMD = '''
        sudo curl http://169.254.169.254/latest/meta-data/public-hostname >> /var/www/html/index.html
        exit
        ''' 
setImginIndex = '''
        sudo touch /var/www/html/index.html
        sudo chown ec2-user /var/www/html/index.html
        sudo echo '<img src = ''' + resourceS3URL + ''' alt = "resourcePicture">' >> /var/www/html/index.html
        exit
        '''


# Set Url var to argument from command else
try:
    resourceURL = sys.argv[1]
except IndexError:
    print(colored('resource not found, setting to default image', 'red'))
    resourceURL = "http://www.infinitecat.com/archive18/cute18/finger-on-cat-nose.jpg"
 

# Check Internet connection
checkConnectionToResource('http://google.com/')

# Call bucket handler to create new Bucket
checkConnectionToResource(resourceURL)
createBucket(bucketName)
print(colored(f'Pulling image down from : {resourceURL}', 'cyan'))
pullImageFromURL(resourceURL, resourceName)
print(colored(f'Putting image to Bucket : {bucketName}','cyan'))

putImageToBucket(bucketName,resourceName,None)
os.system('sudo rm *.jpg')

    

# Call instance handler to create new instance and run http server
instance_handler.createEC2Instance(amiId,secGroup,instType,keyName,usrData)

# retrieve  instance information for vars
for i in instance_handler.ec2.instances.all():
    instList = [i.public_ip_address]
    instIP = str(instList[-1])
   # print(instIP)                       # used for debugging


for i in instance_handler.ec2.instances.all():
    instList = [i.id]
    instID = str(instList[-1])
   # print(instID)                       # used for debugging

# Provide var with HTTP prefix
instanceHTTP = f'http://{instIP}'
print(colored(f'Waiting for resource {instanceHTTP} to become available','magenta',attrs=['blink']))


waitForConnection(instanceHTTP)     #Wait until instance HTTP is accessible
# Run ssh commands to Instance
print(colored('Running ssh connection to setup index','blue'))
ssh_handler.startSSHConnection(userName,instIP,'new_web_server_key.pem',setImginIndex)

print(colored('Running ssh connection to retrieve meta-data','blue'))
ssh_handler.startSSHConnection(userName,instIP,'new_web_server_key.pem',getAmiIDCMD)

time.sleep(120)
def getMetrics(instID,metricList):
    for metricName in metricList :
        response  = startCloudWatchMonitor(instID,metricName)
        while(response == None):
            time.sleep(1)
        else:
            print(colored(response,'yellow'))

getMetrics(instID,metricList)
