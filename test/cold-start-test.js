var containerId = Date.now().toString().slice(-6);
var configTimestamp = new Date().toISOString();
var workTime = 2000;
var fs = require("fs");

exports.handler = (event, context, callback) => {
    switch (event.messageType) {
        case 'work' : 
            setTimeout(function() { 
                context.succeed("Container " + containerId + ": Work done, with timestamp " + configTimestamp);
            }, workTime);
            break;

        case 'refreshConfig' :
            configTimestamp = new Date().toISOString();
            context.succeed("Container " + containerId + " : Refresh Config done, new timestamp " + configTimestamp);
            break;
        
        case 'writeId' :
            fs.writeFile('/tmp/containerId.txt', containerId, function(err) {
                if (err) {
                    context.fail("writeFile failed: " + err);
                } else {
                    context.succeed("Successfully Writing container id to /tmp/containerId.txt at container " + containerId)
                }
            });
            break;

        case 'retrieveId' :
            fs.readFile('/tmp/containerId.txt', function read (err, data) {
                if (err) {
                    context.fail("The container Id hasn't been written to /tmp at container " + containerId + " "+ err);
                } else {
                    context.succeed("Successfully Retrieve container id : " + data)
                }
            });
            break;
    }
};