FROM lambci/lambda:build-python3.6
WORKDIR /var/task/
COPY build.sh ./
COPY requirements.txt ./
RUN sh build.sh
COPY deploy.sh ./
CMD [ "sh", "deploy.sh" ]