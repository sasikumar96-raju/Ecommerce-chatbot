# import tensorflow as tf
# import tensorflow_hub as hub
# import tensorflow_text as text
# import pandas as pd
# from sklearn.preprocessing import LabelEncoder
# import json
# from sklearn.model_selection import train_test_split
# from tensorflow.keras.models import Model
# from tensorflow.keras.layers import Input, BatchNormalization, Dense, Dropout
# from tensorflow.keras.optimizers import Adam
#
# from tensorflow.keras.models import load_model
# import json
# import numpy as np
import pandas as pd
from sqlalchemy import create_engine
# import mysql.connector
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
nlp = spacy.load("en_core_web_sm")


greetings_keywords = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "how are you"]
product_keywords = ["product", "item", "buy", "purchase", "sale", "discount", "price", "cost", "brand", "model", 'details', 'query', 'help', 'get']
positive_keywords = ["good","great", "excellent", "fantastic", "wonderful", "awesome", "terrific", "super", "amazing", "outstanding", "impressive", 'thank you', 'thank']
negative_keywords = ["sorry", "apologies", "unfortunate", "concerned", "frustrated", "regret", "disappointing", "issue", "challenge", "problem"]


def extract_entities(message, db_config):
    try:
        split_message = message.split(":", 1)
        if len(split_message) == 2:
            extracted_text = split_message[1].strip()
            where_condition = f"name = '{extracted_text}'"
            query = f"SELECT * FROM products WHERE {where_condition}"
            engine = create_engine(f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
            df = pd.read_sql_query(query, con=engine)
            if len(df) == 0:
                return "Please provide a valid Product name"
            engine.dispose()
            product_name, price, rating = df.iloc[0]['name'], df.iloc[0]['price'], df.iloc[0]['rating']
            return f"Hi! The product price for {product_name} is {price} and its rating is {rating}"
        else:
            return "Please provide product details like `Product: your product model name `"
    except Exception as e:
        print(e)
        return "Please provide product details like `Product: your product model name `"


def has_common_elements(list1, list2):
    return any(element in list2 for element in list1)


def get_result(message, db_config, sentiment_score, preprocessed_tokens):
    if has_common_elements(preprocessed_tokens, product_keywords):
        # intent = 'Product'
        entities = extract_entities(message, db_config)
        return entities
    elif has_common_elements(preprocessed_tokens, greetings_keywords):
        intent = 'Greetings'
    elif has_common_elements(preprocessed_tokens, positive_keywords) or sentiment_score >= 0.5:
        intent = "Positive Feedback"
    elif has_common_elements(preprocessed_tokens, negative_keywords) or sentiment_score < 0.5:
        intent = "Negative Feedback"
    where_condition = f"intent = '{intent}'"
    query = f"SELECT * FROM customer_feedback WHERE {where_condition}"
    engine = create_engine(f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    df = pd.read_sql_query(query, con=engine)
    engine.dispose()
    vectorizer = CountVectorizer()
    sentence_vectors = vectorizer.fit_transform(df['complaint_text'])
    input_vector = vectorizer.transform([message])
    cosine_sim_values = cosine_similarity(input_vector, sentence_vectors)[0]
    max_similarity_index = cosine_sim_values.argmax()
    most_similar_row = df.loc[max_similarity_index]
    return most_similar_row.response_text