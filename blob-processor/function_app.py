import azure.functions as func
import logging
import json
from typing import List

app = func.FunctionApp()

# Define a blob trigger for the function
@app.blob_trigger(arg_name="myblob", path="logsjson",
                               connection="logsjson_connection_string")
# Define an Event Hub output for the function
@app.event_hub_output(arg_name="event",
                      event_hub_name="function-app-logs",
                      connection="event_hub_connection_string")
def blob_processor(myblob: func.InputStream, event: func.Out[List[str]]):
    # Log the name and size of the processed blob
    logging.info(f"Python blob trigger function processed blob "
                f"Name: {myblob.name} "
                f"Blob Size: {myblob.length} bytes")

    # Read the content of the blob line by line
    blob_content = myblob.readlines()
    batch_messages = []
    
    for line in blob_content:
        # Decode the line to a string and load it as a JSON object
        line = line.decode()
        data = json.loads(line)
        
        # Add the JSON object to the batch of messages
        batch_messages.append(data)
        logging.info(f"Data: {data}")
     
    # Send the batch of messages to the Event Hub   
    event.set(batch_messages)
    # Log the batch of messages that was sent to the Event Hub
    logging.info(f"Event: {event.get()}")