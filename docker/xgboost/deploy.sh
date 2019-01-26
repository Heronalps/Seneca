#! /bin/bash
source ./venv/bin/activate
pushd $VIRTUAL_ENV/lib/python3.6/site-packages
zip -9rq /var/task/lambda_xgboost.zip *
popd
zip -9j lambda_xgboost.zip /var/task/xgboost/XGBoost.py

aws s3api put-object --bucket seneca-racelab --key lambda_xgboost.zip \
--body lambda_xgboost.zip

functions=`aws lambda list-functions`

exist=false

for function in $functions; do
    if [[ "$function" = *xgboost_worker* ]] ; then
        exist=true
    fi
done

if [[ "$exist" == false ]] ; then
    aws lambda create-function \
    --function-name XGBoost_worker --runtime python3.6 \
    --role $AWS_ROLE --handler XGBoost.lambda_handler \
    --code S3Bucket=seneca-racelab,S3Key=lambda_xgboost.zip \
    --timeout 900 \
    --layers arn:aws:lambda:us-west-2:420165488524:layer:AWSLambda-Python36-SciPy1x:2
fi
if [[ "$exist" == true ]] ; then
    aws lambda update-function-code --function-name xgboost_worker \
    --s3-bucket seneca-racelab --s3-key lambda_xgboost.zip
fi