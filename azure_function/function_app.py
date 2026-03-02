import azure.functions as func
import logging
import os
import requests
import json

from domain.models import SpeakEvaluation
from llm_client import LLMClient
from db_client import DbClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

#@app.route(route="http_example")
#@app.queue_output(arg_name="msg", queue_name="outqueue", connection="AzureWebJobsStorage")
#def HttpExample(req: func.HttpRequest, msg: func.Out [func.QueueMessage]) -> func.HttpResponse:
#    logging.info('Python HTTP trigger function processed a request.')
#db_client = DbClient(
#    connection_string=os.environ.get("MONGO_CONNECTION_STRING"),
#    database_name=os.environ.get("MONGO_DATABASE_NAME")
#)
llm_client = LLMClient()
db_client = DbClient()
def transcribe_audio(audio_bytes):
    API_URL = os.environ.get('SPEECH_API_URL')
    API_KEY = os.environ.get('SPEECH_API_KEY')
    headers = {
        'Accept': 'application/json',
        'Ocp-Apim-Subscription-Key': API_KEY
    }
    definition = {
        "locales": ["en-US"],
        "profanityFilterMode": "Masked",
        "channels": [0]
    }
    files = {
        'audio': audio_bytes,
        'definition': (None, json.dumps(definition), 'application/json')
    }
    response = requests.post(API_URL, headers=headers, files=files)
    return response.json()

async def update_db(blob_name, update_data:dict):
    filename = os.path.basename(blob_name)  # archivo.wav
    name, _ = os.path.splitext(filename)
    audio_name = name+".wav"
    logging.warning(f"Updating DB for file: {audio_name} with data: {update_data}")
    speak_eval:SpeakEvaluation = await db_client.findByFileName(audio_name)
    await db_client.update(speak_eval._id, update_data)

@app.blob_output(arg_name="outputblob",path="transcriptions/{name}.json",connection="stab2speaking_STORAGE")
@app.blob_trigger(arg_name="myblob", path="audios/{name}.wav", connection="stab2speaking_STORAGE")
async def BlobTrigger(myblob: func.InputStream, outputblob: func.Out[str]):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")
    audio_bytes = myblob.read()
    transcribe_audio_result = transcribe_audio(audio_bytes)
    logging.info(f"Transcription result: {transcribe_audio_result}")

    outputblob.set(json.dumps(transcribe_audio_result, ensure_ascii=False))
    await update_db(myblob.name, {"state": "TRANSCRIBED", "transcription": transcribe_audio_result["combinedPhrases"]})

    logging.info("Transcription stored successfully")



@app.blob_trigger(arg_name="myblob", path="transcriptions/{name}.json", connection="stab2speaking_STORAGE") 
async def evaluation_function(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")
    # Read the blob content and parse as JSON
    content = myblob.read().decode("utf-8")
    data = json.loads(content)
    # Extract the 'text' field from each item in the list
    # Unir los campos 'text' de cada frase en un solo string
    combined_phrases = " ".join(phrase.get("text", "") for phrase in data.get("combinedPhrases", []))
    logging.info(f"Combined phrases: {combined_phrases}")

    check_transcription_result = llm_client.check_transcription(combined_phrases)

    await update_db(myblob.name, {"state": "EVALUATED", "result": check_transcription_result})
    logging.info("Evaluation stored successfully")

# This example uses SDK types to directly access the underlying BlobClient object provided by the Blob storage trigger.
# To use, uncomment the section below and add azurefunctions-extensions-bindings-blob to your requirements.txt file
# Ref: aka.ms/functions-sdk-blob-python
#
# import azurefunctions.extensions.bindings.blob as blob
# @app.blob_trigger(arg_name="client", path="transcriptions/{name}.json",
#                   connection="stab2speaking_STORAGE")
# def evaluation_function(client: blob.BlobClient):
#     logging.info(
#         f"Python blob trigger function processed blob \n"
#         f"Properties: {client.get_blob_properties()}\n"
#         f"Blob content head: {client.download_blob().read(size=1)}"
#     )
