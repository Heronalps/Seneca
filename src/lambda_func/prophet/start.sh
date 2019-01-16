docker run --rm -it -v "$PWD":/var/task lambda-env:0.1 bash build.sh
rm -rf ./venv
rm -rf ./lambda.zip