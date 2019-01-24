#! /bin/bash
source ./venv/bin/activate
pushd $VIRTUAL_ENV/lib/python3.6/site-packages
zip -9rq /var/task/lambda_prophet.zip *
popd
zip -9j lambda_prophet.zip /var/task/prophet/prophet.py

aws s3api put-object --bucket seneca-racelab --key lambda_prophet.zip --body lambda_prophet.zip

functions=`aws lambda list-functions`

exist=false

for function in $functions; do
    if [[ "$function" == *prophet_worker* ]] ; then
        exist=true
    fi
done

if [[ "$exist" == false ]] ; then
    aws lambda create-function \
    --function-name prophet_worker --runtime python3.6 \
    --role $AWS_ROLE --handler prophet.grid_search_worker \
    --code S3Bucket=seneca-racelab,S3Key=lambda_prophet.zip \
    --timeout 900
fi

aws lambda update-function-code --function-name prophet_worker\
 --s3-bucket seneca-racelab --s3-key lambda_prophet.zip