import os
import google.cloud.dialogflow as dialogflow
from google.api_core.exceptions import InvalidArgument

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'pybot-napw-ae8fb38e8e64.json'

# Agent info
DIALOGFLOW_PROJECT_ID = 'pybot-napw'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'


def get_res(query):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.TextInput(text=query, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    return(response.query_result.fulfillment_text)