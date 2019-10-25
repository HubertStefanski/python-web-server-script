#!/usr/bin/python3

import boto3
from datetime import datetime, timedelta
from termcolor import colored
import time

cloudwatch = boto3.resource('cloudwatch')



def startCloudWatchMonitor(instID,metricName):
    instID = instID
    metricName = metricName

    print(colored(f'Running metric handler on instance ID : {instID} and metric : {metricName}','magenta'))

    metric_iterator = cloudwatch.metrics.filter(Namespace='AWS/EC2', 
                                            MetricName=metricName, 
                                            Dimensions=[{'Name':'InstanceId', 'Value': instID}])

    for metric in metric_iterator:
        response = metric.get_statistics(StartTime=datetime.now() - timedelta(minutes=65),     # 5 minutes ago
                                        EndTime=datetime.now() - timedelta(minutes=60),       # now
                                        Period=300,                                           # 5 minute intervals
                                        Statistics=['Average'])
        print(f"Average {metricName} utilisation:", response['Datapoints'][0]['Average'])
        return response
        print (colored(response,'yellow'))

