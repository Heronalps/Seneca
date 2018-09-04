import boto3, time
from datetime import datetime

client = boto3.client('cloudwatch')

def duration(StartTime, EndTime, Stat='Sum'):
    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'duration_id',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/Lambda',
                        'MetricName': 'Duration',
                        'Dimensions': [
                            {
                                'Name': 'FunctionName',
                                'Value': 'container_tester'
                            },
                        ]
                    },
                    'Period': 1,
                    'Stat': Stat,
                    'Unit': 'Milliseconds'
                },
                'Label': 'Total_Execution_time',
                'ReturnData': True
            },
        ],
        StartTime = StartTime, # time.time() - 1200,
        EndTime = EndTime, # time.time(),
        ScanBy = 'TimestampAscending'
    )

    return response

def duration_stat(StartTime, EndTime, Stat='Sum'):
    response = client.get_metric_statistics(
        Namespace = 'AWS/Lambda',
        MetricName = 'Duration',
        Dimensions = [
            {
                'Name': 'FunctionName',
                'Value': 'container_tester'
            },
        ],
        Period = 1,
        Statistics = [Stat],
        Unit = 'Milliseconds',
        StartTime = StartTime, 
        EndTime = EndTime
    )

    return response


if __name__ == "__main__":
    timestamp_start = time.time() - 1440
    timestamp_end = time.time()
    print("Start timestamp : ", timestamp_start)
    print("End timestamp : ", timestamp_end)
    response = duration(timestamp_start, timestamp_end)
    # response = duration_stat(timestamp_start, timestamp_end)
    print(response)
    timestamps = response['MetricDataResults'][0]['Timestamps']
    for t in timestamps:
        print(t.timestamp())

