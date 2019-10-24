#!/usr/bin/env python3
import boto3
import sys
# coloured output for important information to stand out
from termcolor import colored

ec2 = boto3.resource('ec2', region_name='eu-west-1')



# Create new Ec2 instance 
def createEC2Instance(amiID,secGroup,instType,keyName,usrData):
    try:
        instance = ec2.create_instances(
            ImageId=amiID, #most up-to-date AMI
            MinCount=1,
            MaxCount=1,
            # group ID with SSH and HTTP access rules in place
            SecurityGroupIds=secGroup,
            InstanceType=instType,
            KeyName=keyName,
            # launch HTTP service to allow access through web browser
            UserData=usrData,
        )
    except Exception as err:
        return err
        print(err)

    #tag_specification = [{'ResourceType': 'instance', 'Tags': instTags}]
    #instance[0].create_tags(Tags={instTags}) 
    
    # give the user feedback creation
    print(colored(">>>Waiting for instance to Launch, this may take a while",
                  'green', attrs=['bold']))

    # Wait to proceed until instance is fully launched
    instance[0].wait_until_running()

    # refresh the api to grab updated information
    instance[0].reload()
    instance[0].monitor()

    # print instance ID and IP in case user wants to SSH manually
    print(colored(f"Instance ID : {instance[0].id}", 'yellow'))
    print(colored(f"Public ip for ssh : {instance[0].public_ip_address}", 'yellow'))
    print(colored(">>>Instance is up, HTTP Server should be available shortly",
                  'yellow', attrs=['bold']))


