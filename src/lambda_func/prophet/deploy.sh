source ./venv/bin/activate
pushd $VIRTUAL_ENV/lib/python3.6/site-packages
zip -9rq /var/task/lambda.zip *
popd
zip -9j lambda.zip /var/task/prophet/prophet.py

aws s3api put-object --bucket prophet-racelab --key lambda.zip --body lambda.zip
aws lambda update-function-code --function-name prophet_worker\
 --s3-bucket prophet-racelab --s3-key lambda.zip