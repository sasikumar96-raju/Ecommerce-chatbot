import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import json
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, BatchNormalization, Dense, Dropout
from tensorflow.keras.optimizers import Adam

from tensorflow.keras.models import load_model
import json
import numpy as np


with open('/home/ubuntu/Downloads/labels.json', 'r') as labels:
    label_dict = json.load(labels)
model_path = '/home/ubuntu/Downloads/bert_model/content/bert_model'


def get_result(review):
    model = load_model(model_path)
    predictions = model.predict([review])
    class_labels = list(label_dict.keys())
    predicted_class_index = np.argmax(predictions)
    predicted_class = class_labels[predicted_class_index]
    return predicted_class


