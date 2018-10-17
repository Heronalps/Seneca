import time, os, sys, json, decimal
from datetime import datetime

containerId = str(int(time.time()))[-6:]
configTimestamp = str(datetime.now())
local_repo = os.path.join(os.path.sep, "tmp", os.path.basename('container'))

def lambda_handler(request):
    request_json = request.get_json()
    response = ''
    if request_json['messageType'] == 'work':
        response = {
            'Message' : "Container " + containerId + ": work is done with timestamp " + configTimestamp
        }

    elif request_json['messageType'] == 'refreshConfig':
        configTimestamp2 = str(datetime.now())
        response = {
            'Message' : "Container " + containerId + ": work is done with timestamp " + configTimestamp2
        }
    
    elif request_json['messageType'] == 'writeId':
        if not os.path.exists(local_repo):
            os.makedirs(local_repo)

        with open(local_repo + "Id.txt", 'w') as f:
            f.write(containerId)
        response = {
            'Message' : "Successfully write container id " + containerId + " to " + local_repo + "Id.txt"
        }

    elif request_json['messageType'] == 'retrieveId':
        try:
            with open(local_repo + 'Id.txt') as f:
                container_id = f.read()
        except FileNotFoundError:
            response = {
                'Message' : "The container id is not saved in this lambda " + containerId + " container."
            }
        if not response:
            response =  {
                'Message' : "Retrieved Container id : " + container_id
            }
    
    # Generate Log events
    print(response)
    response_str = json.dumps(response)
    print(response_str) 
    return response_str
    