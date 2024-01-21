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
import mysql.connector

db_config = {
    'user': 'root',
    'password': 'ubuntu',
    'host': 'localhost',
    'database': 'sample_ecom',
    'port': 3306  # Change if your MySQL server is running on a different port
}


def fetch_data():
    table_name = 'customer_feedback'
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print(f"Connected to MySQL database: {db_config['database']}")
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, connection)
            return len(df)
    except mysql.connector.Error as e:
        return f"Error: {e}"
    finally:
        if connection.is_connected():
            connection.close()
            return "Connection closed."


def preprocess_and_train(df):
    le = LabelEncoder()
    df['Label'] = le.fit_transform(df['Intent'])
    label_dict = dict(zip(le.classes_, le.transform(le.classes_).tolist()))

    Y = df['Label']
    X = df.drop(columns=['Label', 'Intent', 'Time of Complain', 'Date of Complain', 'Customer ID', 'Response'], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, stratify=Y, random_state=33)

    text_input = Input(shape=(), dtype=tf.string, name='text')
    preprocessed_text = bert_preprocess(text_input)
    outputs = bert_encoder(preprocessed_text)

    batch_norm = BatchNormalization(name='batch_norm')(outputs['pooled_output'])
    dropout = Dropout(0.1, name='dropout')(batch_norm)
    dense = Dense(128, activation='relu', name='dense_layer')(dropout)
    output = Dense(len(label_dict), activation='softmax', name='output')(dense)

    model = Model(inputs=[text_input], outputs=[output])

    y_train = (tf.keras.utils.to_categorical(y_train, len(label_dict))).astype(int)
    y_test = (tf.keras.utils.to_categorical(y_test, len(label_dict))).astype(int)

    model.compile(optimizer=Adam(learning_rate=1e-5), loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=32)

    model.save('bert_model_multilabel')

    return 'bert_model_multilabel'


def main():
    df = fetch_data()
    model_path = preprocess_and_train(df)


if __name__ == '__main__':
    main()








