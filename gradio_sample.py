import random
from inference import get_result
import gradio as gr


def get_intent(message, history):
    prediction = get_result(message)
    return prediction


gr.ChatInterface(get_intent).launch(share=True)
