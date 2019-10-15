#!/usr/bin/env python3
import boto3
import sys
# coloured output for important information to stand out
from termcolor import colored

ec2 = boto3.resource('ec2', region_name='eu-west-1')



def createEC2Instance():
    instance = ec2.create_instances(
        ImageId='ami-0ce71448843cb18a1',
        MinCount=1,
        MaxCount=1,
        # group ID with SSH and HTTP access rules in place
        SecurityGroupIds=['sg-03057cb040ad8642c'],
        InstanceType='t2.micro',
        KeyName='new_web_server_key',
        # launch HTTP service to allow access through web browser
        UserData="""
             #!/bin/bash                  
             sudo yum update -y
             sudo yum install httpd -y
             sudo systemctl enable httpd
             sudo service httpd start
             sudo touch /var/www/html/index.html
             """
    )
    # give the user feedback creation
    print(colored(">>>Waiting for instance to Launch, this may take a while",
                  'green', attrs=['bold']))

    # Wait to proceed until instance is fully launched
    instance[0].wait_until_running()

    # refresh the api to grab updated information
    instance[0].reload()
    

    # print instance ID and IP in case user wants to SSH manually
    print(colored("Instance ID : " + instance[0].id, 'yellow'))
    print(colored("Public ip for ssh : " +
                  instance[0].public_ip_address, 'yellow'))
    print(colored(">>>Instance is up, HTTP Server should be available shortly",
                  'yellow', attrs=['bold']))


