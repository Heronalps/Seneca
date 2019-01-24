#! /bin/bash
source ./venv/bin/activate
pushd $VIRTUAL_ENV/lib/python3.6/site-packages
zip -9rq /var/task/lambda_multi_regression.zip *
popd
zip -9j lambda_multi_regression.zip /var/task/multi_regression/multi_regression.py

aws s3api put-object --bucket seneca-racelab --key lambda_multi_regression.zip \
--body lambda_multi_regression.zip

functions=`aws lambda list-functions`

exist=false

for function in $functions; do
    if [[ "$function" = *multi_regression_worker* ]] ; then
        exist=true
    fi
done

if [[ "$exist" == false ]] ; then
    aws lambda create-function \
    --function-name multi_regression_worker --runtime python3.6 \
    --role $AWS_ROLE --handler multi_regression.lambda_handler \
    --code S3Bucket=seneca-racelab,S3Key=lambda_multi_regression.zip \
    --timeout 900
fi

aws lambda update-function-code --function-name multi_regression_worker \
--s3-bucket seneca-racelab --s3-key lambda_multi_regression.zip