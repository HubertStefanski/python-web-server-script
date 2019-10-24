#!/usr/bin/python3

import boto3
from datetime import datetime, timedelta

cloudwatch = boto3.resource('cloudwatch')
def startCloudWatchMonitorCPU(instID):
    instID = instID
    print(instID)

    metric_iterator = cloudwatch.metrics.filter(Namespace='AWS/EC2', 
                                            MetricName='CPUUtilization', 
                                            Dimensions=[{'Name':'InstanceId', 'Value': instID}])

    for metric in metric_iterator:
        response = metric.get_statistics(StartTime=datetime.now() - timedelta(minutes=65),     # 5 minutes ago
                                        EndTime=datetime.now() - timedelta(minutes=60),       # now
                                        Period=300,                                           # 5 minute intervals
                                        Statistics=['Average'])
        print ("Average CPU utilisation:", response['Datapoints'][0]['Average'])
        return response
        print (response)   # for debugging only

def startCloudWatchMonitorMEM(instID):
    instID = instID

    metric_iterator = cloudwatch.metrics.filter(Namespace='AWS/EC2', 
                                            MetricName='MemoryUtilization', 
                                            Dimensions=[{'Name':'InstanceId', 'Value': instID}])

    for metric in metric_iterator:
        response = metric.get_statistics(StartTime=datetime.now() - timedelta(minutes=65),     # 5 minutes ago
                                        EndTime=datetime.now() - timedelta(minutes=60),       # now
                                        Period=300,                                           # 5 minute intervals
                                        Statistics=['Average'])
        print ("Average Memory utilisation:", response['Datapoints'][0]['Average'])
        return response
        print (response)   # for debugging only

def startCloudWatchMonitorDISK(instID):
    instID = instID

    metric_iterator = cloudwatch.metrics.filter(Namespace='AWS/EC2', 
                                            MetricName='DiskSpaceUtilization', 
                                            Dimensions=[{'Name':'InstanceId', 'Value': instID}])

    for metric in metric_iterator:
        response = metric.get_statistics(StartTime=datetime.now() - timedelta(minutes=65),     # 5 minutes ago
                                        EndTime=datetime.now() - timedelta(minutes=60),       # now
                                        Period=300,                                           # 5 minute intervals
                                        Statistics=['Average'])
        print ("Average disk space  utilisation:", response[Datapoints][0]['Average'])
        return response
        print (response)   # for debugging only
