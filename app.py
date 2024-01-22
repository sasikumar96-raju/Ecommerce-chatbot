from flask import Flask, render_template, request, make_response, jsonify
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import json
import nltk 
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('vader_lexicon')

from preprocess_data import preprocess_text, perform_sentiment_analysis
from inference import get_result
app_path = "/home/ubuntu/app"

source_complaint_data = 'src/updated_feedback_data.csv'
source_products_data = 'src/data.csv'

app = Flask(__name__)


with open('db_config.json', "r") as json_file:
    db_config = json.load(json_file)


@app.route('/insert_review', methods =["POST"])
def insert_review_data():
    df = pd.read_csv(source_complaint_data)
    df['preprocessed_text'] = df['complaint_text'].apply(preprocess_text)
    df['sentiment_score'] = df['preprocessed_text'].apply(perform_sentiment_analysis)
    df = df.drop(columns=['preprocessed_text'])
    df['date_of_complain'] = pd.to_datetime(df['date_of_complain'], format='%Y-%m-%d', errors='coerce')
    df['time_of_complain'] = pd.to_datetime(df['time_of_complain'], format='%I:%M %p').dt.time
    engine = create_engine(f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    df.to_sql('customer_feedback', con=engine, if_exists='append', index=False)
    engine.dispose()
    return "Successfully inserted"


@app.route('/insert_products', methods =["POST"])
def insert_product_data():
    df = pd.read_csv(source_products_data)
    df = df.dropna()
    df['Rating'] = df['Rating'].str.extract(r'(\d+\.\d+)', expand=False).astype(float)
    df['Price'] = df['Price'].astype(int)
    engine = create_engine(f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    df.to_sql('products', con=engine, if_exists='append', index=False)
    return "Successfully inserted products"


@app.route('/review', methods=["POST"])
def get_service_response():
    review = request.form['review']
    preprocessed_tokens = preprocess_text(review)
    sentiment_score = perform_sentiment_analysis(preprocessed_tokens)
    prediction = get_result(review, db_config, sentiment_score, preprocessed_tokens)
    return prediction


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)