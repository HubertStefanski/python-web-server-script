#!/usr/bin/env python3
# Import for feedback highlighing
from termcolor import colored
# Import library for ssh connections and sshClientside
import paramiko


# Connect to specified ip using params through ssh and execute provided code 
def startSSHConnection(username,instanceIP, resourceName,keyName,commandIssued):
    ssh = paramiko.SSHClient()
    try:
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())#automatically add hostname and host key to local HostKeys object and save
        ssh.connect(instanceIP,username=username,key_filename=keyName)  #Begin connection     
        ssh = ssh.invoke_shell()
        stdin = ssh.makefile('wb')
        stdout = ssh.makefile('rb')
        stdin.write(commandIssued) # write to stdin the command/s passed trough params
        print(stdout.read())
        stdout.close()
        stdin.close()
    except Exception as err:
        return err
        print(err)
    # Close connection upon function completion
    ssh.close()