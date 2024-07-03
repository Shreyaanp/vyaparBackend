# Vyapar Backend

This project is a backend server built using FastAPI. It provides RESTful APIs for user authentication, product management, store management, and file uploads to AWS S3.

## Features

- User Registration and Login
- Product Upload and Management
- Store Management
- File Upload to AWS S3
- CORS Configuration
- Health Check Endpoint

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- Pydantic
- Motor (for MongoDB)
- Boto3 (for AWS S3)
- Python-dotenv

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/vyapar-backend.git
    cd vyapar-backend
    ```

2. Create a virtual environment and activate it:

    ```sh
    python3 -m venv env
    source env/bin/activate
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file and add your environment variables (e.g., AWS credentials, MongoDB connection string).

## Running the Application

To run the FastAPI application, use the following command:

```sh
uvicorn app.main:app --reload
```

## Api health points

Health Check
- GET /: Check if the server is working.
Authentication
- POST /auth/register: Register a new user.
- POST /auth/login: Login a user.
S3 Upload
- POST /upload/s3: Upload a single file to S3.
- POST /upload/s3/multiple: Upload multiple files to S3.
- POST /upload/s3/generated: Upload a generated file to S3.
Product Management
- POST /product/upload: Upload product details.
- GET /product/{user_id}: Get products by user ID.
- PUT /product/{product_id}: Update product details.
- DELETE /product/{product_id}: Delete a product.
- POST /product/publish: Publish a product.
- GET /public/{shareable_id}: Get a public product by shareable ID.
Store Management
- POST /store: Create a store product.
- GET /store/{user_id}: Get store products by user ID.
- PUT /store/{product_id}: Update store product details.
- DELETE /store/{product_id}: Delete a store product.
CORS Configuration
- The application is configured to allow CORS from the following origins:

http://localhost:5173
https://backend.vlai.in
https://vyaparfrontend.vercel.app

You can add more origins as needed in the origins list in main.py.