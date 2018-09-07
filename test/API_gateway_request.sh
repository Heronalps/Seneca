for i in {1..10}
do
    echo "Call API Gateway $i time"
    curl --header "messagetype:retrieveId" https://gnpi5k7uh0.execute-api.us-west-2.amazonaws.com/default/cold-start-test-py-api
    echo 
done
