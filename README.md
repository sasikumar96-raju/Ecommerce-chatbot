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

**Examples**
    
    - User text:
    
        Hi how are you


    - Chatbot response:
    
        Hi! I'm doing well, thank you. How can I assist you today?

    - User text:
        
        Delivered on right time thank you
    
    - Chatbot response:

        Hey there! Perfect is what we aim for! If there's anything else you need or if you have more orders in the future, we're
        ready to assist.

    - User text:
   
        Worst service!
    
    - Chatbot response:

        We're sorry to hear about your unsatisfactory experience. Please provide details about the issue, and we'll do our best
        to address and resolve it for you.
    
    - User text:

        My phone is very good

    - Chatbot response:

        Good day! Thank you for the compliment on our product quality. We're committed to delivering excellence. Anything
        specific you'd like to know or explore?
    
    - User text:
        
        Can you help me with product details

    - Chatbot response:

        Please provide product details like `Product: your product model name

    - User text:

        Product:Moto E

    - Chatbot response:

        Hi! The product price for Moto E is 8684 and its rating is 3.0

        

        ``````
    