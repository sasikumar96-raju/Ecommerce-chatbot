# Ecommerce Customer Service Chatbot Flask App

## Overview

This Flask application is a customer service chatbot for an Ecommerce platform, utilizing a MySQL database to store customer feedback and product information. Follow the steps below to set up and run the app.

## Prerequisites

- Python 3.x
- MySQL installed
- Postman installed (for testing API endpoints)

## Installation

1. **Clone the GitHub repository:**

    ```bash
    git clone https://github.com/sasikumar96-raju/Ecommerce-chatbot.git
    cd Ecommerce-chatbot
    ```

2. **Install MySQL and upadting configs:**

    Ensure that MySQL is installed on your system. If not, follow the official MySQL installation instructions.
    Open app.py and check the `source_complaint_data` and `source_products_data` file path's are given correctly.
    Update the `db_config.json` with your mysql configurations.

4. **Create Database and Tables:**

    - Login to MySQL:

        ```bash
        mysql -u your-username -p
        ```

    - Create the database and tables:

        ```sql
        CREATE TABLE customer_feedback (
            complaint_id INT PRIMARY KEY,
            customer_id VARCHAR(255),
            date_of_complain DATE,
            time_of_complain TIME,
            complaint_text VARCHAR(255),
            sentiment_score FLOAT,
            intent VARCHAR(255)
        );

        CREATE TABLE products (
            product_id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255),
            rating FLOAT,
            price INT
        );
        ```

5. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Running the App

1. **Start the Flask app:**

    ```bash
    python app.py
    ```

2. **Open Postman and test the endpoints:**

    - Insert customer feedback data:

        ```bash
        POST http://localhost:5000/insert_review
        ```

        If successful, you will see the message: "Successfully inserted."

    - Insert product data:

        ```bash
        POST http://localhost:5000/insert_products
        ```

        If successful, you will see the message: "Successfully inserted products."

    - Test the chatbot:

        ```bash
        POST http://localhost:5000/review
        ```

        Set the body as form data with key "review" and the user's message as the value. Execute the request to get the customer service response as a string in the output.