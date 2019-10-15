#!/usr/bin/env python3
import sys
import boto3
import os
import time
from termcolor import colored
from paramiko import *



def startSSHConnection(instanceIP, resourceName):
    ssh = SSHClient()
    #try:
    ssh.load_system_host_keys()
   # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('ec2-user@'+instanceIP)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('y')
    print(colored(ssh_stdout, 'magenta'))
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo echo <h1>Welcome to your new web server</h1><p><img src=' +resourceName+' /></p>' '> /var/html/index.html')
    #except Exception as err:
    #    return err
    #    print(err)
    
    ssh.close()