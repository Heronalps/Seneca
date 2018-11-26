from datetime import datetime

def build_response(event):
    response = {}

    if event['messageType'] == 'work':
        response = {
            'Message' : "Container " + containerId + ": work is done with timestamp " + configTimestamp
        }

    elif event['messageType'] == 'refreshConfig':
        configTimestamp2 = str(datetime.now())
        response = {
            'Message' : "Container " + containerId + ": work is done with timestamp " + configTimestamp2
        }
    
    elif event['messageType'] == 'writeId':
        if not os.path.exists(local_repo):
            os.makedirs(local_repo)

        with open(local_repo + "Id.txt", 'w') as f:
            f.write(containerId)
        response = {
            'Message' : "Successfully write container id " + containerId + " to " + local_repo + "Id.txt"
        }

    elif event['messageType'] == 'retrieveId':
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
    return response
