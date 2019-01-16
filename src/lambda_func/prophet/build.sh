python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --no-cache

pip uninstall -y matplotlib
find "$VIRTUAL_ENV/lib/python3.6/site-packages" -name "test" | xargs rm -rf
find "$VIRTUAL_ENV/lib/python3.6/site-packages" -name "tests" | xargs rm -rf
rm -rf "$VIRTUAL_ENV/lib/python3.6/site-packages/pystan/stan/src"
rm -rf "$VIRTUAL_ENV/lib/python3.6/site-packages/pystan/stan/lib/stan_math/lib"
echo "venv size $(du -sh $VIRTUAL_ENV | cut -f1)"

pushd $VIRTUAL_ENV/lib/python3.6/site-packages
zip -9rq /var/task/lambda.zip *
popd
zip -9 lambda.zip prophet.py

aws s3api put-object --bucket prophet-racelab --key lambda.zip --body lambda.zip
aws lambda update-function-code --function-name prophet_worker\
 --s3-bucket prophet-racelab --s3-key lambda.zip