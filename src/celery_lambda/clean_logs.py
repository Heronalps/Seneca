#!/usr/bin/env python3
from datetime import datetime, timedelta
from dateutil import tz
from time import sleep

import boto3

client = boto3.client('logs')

def print_log_group(log_group, message):
    print("[{}] {}".format(log_group['logGroupName'], message))


def get_log_groups(prefix, next_token=None):
    opts = {
        'logGroupNamePrefix': prefix,
        'limit': 50  # Maximum
    }
    if next_token:
        opts['nextToken'] = next_token
    log_groups_response = client.describe_log_groups(**opts)
    
    if log_groups_response:
        for log_group in log_groups_response['logGroups']:
            yield log_group
        # Exhausted, try to loop with paging token
        if 'nextToken' in log_groups_response:
            yield from get_log_groups(prefix, log_groups_response['nextToken'])


def get_streams(log_group, next_token=None):
    opts = {
        'logGroupName': log_group['logGroupName'],
        'limit': 50  # Max
    }
    if next_token:
        opts['nextToken'] = next_token

    response = client.describe_log_streams(**opts)

    if response:
        for stream in response['logStreams']:
            yield stream
        if 'nextToken' in response:
            yield from get_streams(log_group, response['nextToken'])


def delete_old_streams(log_group):
    """
    Delete old log streams that are empty. Events get cleaned up by log_group['retentionInDays'] but the streams don't.
    """
    print_log_group(log_group, "Checking for old streams...")

    print(" - Streams in group: " + log_group['logGroupName'])
    for stream in get_streams(log_group):

        # lastEventTimestamp doesn't update right away sometimes or if the stream was created with no events
        # it is missing
        if 'lastEventTimestamp' in stream:
            stream_time = datetime.fromtimestamp(stream['lastEventTimestamp'] / 1000, tz=tz.tzutc())
        else:
            # Assume stream creation if we don't have a lastEventTimestamp
            stream_time = datetime.fromtimestamp(stream['creationTime'] / 1000, tz=tz.tzutc())

        client.delete_log_stream(
            logGroupName=log_group['logGroupName'],
            logStreamName=stream['logStreamName']
        )
        print_log_group(log_group, "Deleted stream: " + stream['logStreamName'])
        # The AWS API gets overloaded if we go too fast.
        sleep(0.2)

# This function is the invocation point of clean logs.
# It takes i.e. "/aws/lambda/" + LAMBDA_NAME

def clean_logs(prefix):
    for log_group in get_log_groups(prefix):
        delete_old_streams(log_group)
    print("Done")