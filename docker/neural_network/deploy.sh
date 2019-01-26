#! /bin/bash
source ./venv/bin/activate
pushd $VIRTUAL_ENV/lib/python3.6/site-packages
zip -9rq /var/task/lambda_neural_network.zip *
popd
zip -9j lambda_neural_network.zip /var/task/neural_network/neural_network.py

aws s3api put-object --bucket seneca-racelab --key lambda_neural_network.zip \
--body lambda_neural_network.zip

functions=`aws lambda list-functions`

exist=false

for function in $functions; do
    if [[ "$function" = *neural_network_worker* ]] ; then
        exist=true
    fi
done

if [[ "$exist" == false ]] ; then
    aws lambda create-function \
    --function-name neural_network_worker --runtime python3.6 \
    --role $AWS_ROLE --handler neural_network.lambda_handler \
    --code S3Bucket=seneca-racelab,S3Key=lambda_neural_network.zip \
    --timeout 900 \
    --layers arn:aws:lambda:us-west-2:420165488524:layer:AWSLambda-Python36-SciPy1x:2
fi
if [[ "$exist" == true ]] ; then
    aws lambda update-function-code --function-name neural_network_worker \
    --s3-bucket seneca-racelab --s3-key lambda_neural_network.zip
fi