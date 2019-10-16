#!/usr/bin/env python3
import sys
import boto3
import os
import time
from termcolor import colored
import paramiko



def startSSHConnection(username,instanceIP, resourceName,keyName,commandIssued):
    ssh = paramiko.SSHClient()
    try:
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(instanceIP,username=username,key_filename=keyName)        
        ssh = ssh.invoke_shell()
        stdin = ssh.makefile('wb')
        stdout = ssh.makefile('rb')
        stdin.write(commandIssued)
        print(stdout.read())
        stdout.close()
        stdin.close()

        #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo echo <h1>Welcome to your new web server</h1><p><img src=' +resourceName+' /></p>' '> /var/html/index.html')

    except Exception as err:
        return err
        print(err)

    ssh.close()