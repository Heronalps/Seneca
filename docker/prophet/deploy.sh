#! /bin/bash
source ./venv/bin/activate
pushd $VIRTUAL_ENV/lib/python3.6/site-packages
zip -9rq /var/task/lambda.zip *
popd
zip -9j lambda.zip /var/task/prophet/prophet.py

aws s3api put-object --bucket prophet-racelab --key lambda.zip --body lambda.zip

functions=`aws lambda list-functions`

exist=false

for function in $functions; do
    if [[ "$function" == 'prophet_worker' ]] ; then
        exist=true
    fi
done

if [[ "$exist" = true ]] ; then
    aws lambda create-function \
    --function-name report --runtime python3.6 \
    --role $AWS_ROLE --handler prophet.grid_search_worker \
    --code S3Bucket=prophet-racelab,S3Key=lambda.zip \
    --timeout 900
fi

aws lambda update-function-code --function-name prophet_worker\
 --s3-bucket prophet-racelab --s3-key lambda.zip