#!/usr/bin/env python3
import sys
import boto3
import os
from termcolor import colored



def startSSHConnection(instanceIP):
    sshConnectionInit = 'sudo ssh -i new_web_server_key.pem ec2-user@' +instanceIP
    os.system(sshConnectionInit)
    print(sshConnectionInit)