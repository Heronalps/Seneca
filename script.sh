aws lambda invoke \
--function-name "Retries_Test" \
--invocation-type "Event" \
--log-type "Tail" \
output.txt