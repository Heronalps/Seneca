#!/bin/bash
# Set variables alone and hardcode them for now

source ../../venv/bin/activate
python setup.py build_ext --inplace
zip -r9 lambda.zip lambda_function.py integrate.cpython-36m-darwin.so
aws lambda create-function \
--function-name "cython_test" \
--runtime "python3.6" \
--role "arn:aws:iam::603495292017:role/lambda" \
--handler "lambda_function.lambda_handler" \
--zip-file "fileb://lambda.zip"

