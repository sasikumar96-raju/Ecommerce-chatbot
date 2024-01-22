import random
from inference import get_result
import gradio as gr

from app import get_service_response


db_config = {
    'user': 'root',
    'password': 'ubuntu',
    'host': 'localhost',
    'database': 'sample_ecom',
    'port': 3306
}


# message, db_config, sentiment_score, preprocessed_tokens

# def get_intent(message, db_config, preprocessed_tokens):
#     prediction = get_result(message)
#     return prediction

def get_response(message):
    prediction = get_result(message)
    return prediction



gr.ChatInterface(get_intent).launch(share=True)
