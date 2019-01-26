#! /bin/bash
source ./venv/bin/activate
pushd $VIRTUAL_ENV/lib/python3.6/site-packages
zip -9rq /var/task/lambda_svc.zip *
popd
zip -9j lambda_svc.zip /var/task/svc/svc.py

aws s3api put-object --bucket seneca-racelab --key lambda_svc.zip \
--body lambda_svc.zip

functions=`aws lambda list-functions`

exist=false

for function in $functions; do
    if [[ "$function" = *svc_worker* ]] ; then
        exist=true
    fi
done

if [[ "$exist" == false ]] ; then
    aws lambda create-function \
    --function-name svc_worker --runtime python3.6 \
    --role $AWS_ROLE --handler svc.lambda_handler \
    --code S3Bucket=seneca-racelab,S3Key=lambda_svc.zip \
    --timeout 900 \
    --layers arn:aws:lambda:us-west-2:420165488524:layer:AWSLambda-Python36-SciPy1x:2
fi
if [[ "$exist" == true ]] ; then
    aws lambda update-function-code --function-name svc_worker \
    --s3-bucket seneca-racelab --s3-key lambda_svc.zip
fi