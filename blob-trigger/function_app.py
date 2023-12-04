# Import necessary modules
import azure.functions as func
import logging
import gzip
import io

# Create an instance of FunctionApp
app = func.FunctionApp()

# Define a blob trigger that gets triggered when a new blob is added to the "logs" path
# Define an output binding that writes to a new blob in the "logsjson" path
@app.blob_trigger(arg_name="myblob", path="logs", connection="logs_connection_string")
@app.blob_output(arg_name="outputblob", path="logsjson/{rand-guid}.json", connection="logs_connection_string")
def blob_trigger(myblob: func.InputStream, outputblob: func.Out[func.InputStream]):
    try:
        # Log the name and size of the processed blob
        logging.info(f"Python blob trigger function processed blob "
                     f"Name: {myblob.name} "
                     f"Blob Size: {myblob.length} bytes")
        
        # Open the blob as a gzip file
        with gzip.open(myblob, 'rb') as output:
            # Decode the binary data into text data
            with io.TextIOWrapper(output, encoding='utf-8') as decoder:
                # Read the content of the blob
                content = decoder.read()
                # Log the content of the blob
                logging.info(f"Content: {content}")

        # Write the content to the output blob
        outputblob.set(content)

    except Exception as e:
        # Log any error that occurs
        logging.error(f"An error occurred: {str(e)}")