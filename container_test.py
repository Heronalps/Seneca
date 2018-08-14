import time, os, sys
from datetime import datetime

containerId = str(int(time.time()))[-6:]
configTimestamp = str(datetime.now())
local_repo = os.path.join(os.path.sep, "tmp", os.path.basename('container'))

def lambda_handler(event, context):

    if event['messageType'] == 'work':
        return "Container " + containerId + ": work is done with timestamp " + configTimestamp
        
    elif event['messageType'] == 'refreshConfig':
        configTimestamp2 = str(datetime.now())
        return "Container " + containerId + ": work is done with timestamp " + configTimestamp2
    
    elif event['messageType'] == 'writeId':
        if not os.path.exists(local_repo):
            os.makedirs(local_repo)

        with open(local_repo + "Id.txt", 'w') as f:
            f.write(containerId)
        return "Successfully write container id " + containerId + " to " + local_repo + "Id.txt"

    elif event['messageType'] == 'retrieveId':
        try:
            with open(local_repo + 'Id.txt') as f:
                container_id = f.read()
        except FileNotFoundError:
            return ("The container id is not saved in this lambda " + containerId + " container.")
        return "Retrieved Container id : " + container_id