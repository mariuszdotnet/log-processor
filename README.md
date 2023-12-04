# Event Driven & Serverless Log Processor

The following repo demonstrates log processing as per the below diagram.

## Process Flow

1. Producer generates a Json log file and saves it in gzip format.
2. Producer uploads the gzip log file to Azure Storage container.
3. Blob Trigger Function is triggered to execute by the “Blob Create Event”.
4. Blob Trigger Function deflates the log file from gzip format.
5. Blob Trigger Function saves the Json log file to another Azure Storage container.
6. Storage Account generates “Blob Create Event”.
7. a. Event Grid triggers Blob Trigger Logic App to process the Json log file.
   b. Blob Create Event” triggers Blob Trigger Function to process the Json log file.
8. Blob Trigger (Function/Logic App) process the Json file and for each Json object in the file produces and publishes and event into Even Hubs.
9. Log Event Consumer ingests log events.

![Example Image](images\log-processor-flow.png)
