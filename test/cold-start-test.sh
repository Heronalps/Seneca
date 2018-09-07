#!/bin/bash

for i in {1..100}
do
    echo "Call Lambda Function $i time"
    aws lambda invoke --function-name cold-start-test-js --payload '{"messageType":"work"}' /dev/stderr 1>/dev/null
    echo
done