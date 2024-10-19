# AWS Bedrock Model with FastAPI

This repository contains the codebase for accessing AWS Bedrock models using FastAPI. The project aims to provide a simple and efficient way to interact with AWS Bedrock services through a RESTful API.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Running the Application with Docker](#running-the-application-with-docker)
- [Testing with cURL](#testing-with-curl)
- [Conclusion](#conclusion)

## Installation

To set up the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the FastAPI application, use the following command:
```bash
uvicorn main:app --reload
```

This will start the application, and you can access the FastAPI documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Directory Structure

```
├── app/
│   ├── __init__.py
│   ├── auth.py          # Handles user authentication and JWT generation
│   ├── routes.py        # Main routing file, defines endpoints for login and invoking models
│   ├── models.py        # Pydantic models for request validation
│   ├── providers/
│   │   └── aws_handler.py  # AWS Bedrock handler to invoke Anthropic models
├── .env                 # Contains environment variables (explained below)
├── Dockerfile           # Dockerfile to build the Docker image
├── requirements.txt     # Python dependencies for the project
├── main.py              # Entry point to the FastAPI application
└── README.md            # Project documentation
```

## Environment Variables

You need to create a `.env` file to store sensitive information such as your AWS credentials and JWT secret. Below is an example `.env` file:

```
# JWT Settings
JWT_SECRET_KEY=your_jwt_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_ALGORITHM=HS256

# AWS Credentials for Bedrock
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION=us-east-1
```

Ensure you update the `.env` file with your own AWS credentials and JWT secret.

## API Endpoints

1. **/login** - Authenticate and Generate JWT
   - **Method:** POST
   - **Description:** Authenticates a user and generates a JWT token.
   - **Authentication:** Basic Auth (Username and Password from .env).
   - **Response:** Returns a JWT token to be used for authenticated requests.

   Example cURL request:
   ```bash
   curl -X POST http://127.0.0.1:8000/login --user testuser:testpassword
   ```

2. **/aws-bedrock/anthropic** - Invoke Anthropic Model
   - **Method:** POST
   - **Description:** Invokes AWS Bedrock Anthropic models (e.g., Claude 3) with the provided parameters.
   - **Authentication:** Bearer Token (JWT from /login endpoint).
   - **Payload Example:**
   ```json
   {
     "model_id": "anthropic.claude-3-5-sonnet-20240620-v1:0",
     "system_prompt": "You are a helpful assistant.",
     "payload": {
       "anthropic_version": "bedrock-2023-05-31",
       "temperature": 0.7,
       "top_k": 250,
       "top_p": 1,
       "max_tokens": 4000,
       "messages": [
         {"role": "user", "content": "What is the capital of France?"}
       ]
     }
   }
   ```
   - **Response:** Returns the model's response.

   Example cURL request:
   ```bash
   curl -X POST http://127.0.0.1:8000/aws-bedrock/anthropic \
     -H "Authorization: Bearer <your-jwt-token>" \
     -H "Content-Type: application/json" \
     -d '{
       "model_id": "anthropic.claude-3-5-sonnet-20240620-v1:0",
       "system_prompt": "You are a helpful assistant.",
       "payload": {
         "anthropic_version": "bedrock-2023-05-31",
         "temperature": 0.7,
         "top_k": 250,
         "top_p": 1,
         "max_tokens": 4000,
         "messages": [
           {"role": "user", "content": "What is the capital of France?"}
         ]
       }
     }'
   ```

## Running the Application with Docker

The API is containerized using Docker for easy deployment and isolation. Follow the steps below to build and run the application in a Docker container.

### Prerequisites

- Docker should be installed and running on your machine.

### Steps to Run

1. **Build the Docker Image:** From the root directory of the project, run the following command to build the Docker image:
   ```bash
   docker build -t fastapi-bedrock-app .
   ```

2. **Run the Docker Container:** Once the image is built, run the following command to start the container:
   ```bash
   docker run --env-file .env -d -p 8000:8000 fastapi-bedrock-app
   ```
   - `--env-file .env`: This passes the .env file with the necessary environment variables.
   - `-p 8000:8000`: Maps port 8000 of the container to port 8000 on your local machine.

3. **Access the API:** The API will be accessible at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Testing with cURL

Once the application is running in Docker, you can test the API using cURL.

1. **Get JWT Token:**
   ```bash
   curl -X POST http://127.0.0.1:8000/login --user testuser:testpassword
   ```

2. **Invoke Anthropic Model:** Replace `<your-jwt-token>` with the JWT token obtained from the /login request.
   ```bash
   curl -X POST http://127.0.0.1:8000/aws-bedrock/anthropic \
     -H "Authorization: Bearer <your-jwt-token>" \
     -H "Content-Type: application/json" \
     -d '{
       "model_id": "anthropic.claude-3-5-sonnet-20240620-v1:0",
       "system_prompt": "You are a helpful assistant.",
       "payload": {
         "anthropic_version": "bedrock-2023-05-31",
         "temperature": 0.7,
         "top_k": 250,
         "top_p": 1,
         "max_tokens": 4000,
         "messages": [
           {"role": "user", "content": "What is the capital of France?"}
         ]
       }
     }'
   ```
## Adding More AWS Bedrock Models

To extend the API and include more AWS Bedrock models (e.g., Mistral, Titan), follow these steps:

### Steps to Add a New Model

1. **Identify the Model**:
   - Obtain the `model_id` for the new AWS Bedrock model you wish to integrate.
   - Refer to the AWS Bedrock documentation to ensure you have the correct model parameters (e.g., `temperature`, `top_k`, etc.).

2. **Update `.env` (if necessary)**:
   - Ensure that your `.env` file contains valid AWS credentials, as this will be used for invoking the new models.
   - If there are additional environment variables required for the new models, add them to `.env`.

3. **Modify the Routes**:
   - In `app/routes.py`, add a new route specific to the model. For example, create a new route for `Mistral`:
     ```python
     @router.post("/aws-bedrock/mistral")
     async def invoke_mistral_model(payload: ModelPayload, Authorize: AuthJWT = Depends()):
         Authorize.jwt_required()
         return await invoke_bedrock_model(payload.dict(), model_id="mistral-model-id")
     ```

4. **Add Custom Handling in `aws_handler.py` (if needed)**:
   - If the new model requires a different payload structure or special handling, modify the `invoke_bedrock_model` function in `aws_handler.py` to handle this. For example, handle different required parameters or optional ones.

5. **Test the New Route**:
   - Once you have added the new model route, test it using `cURL` or Postman with the appropriate parameters.
   - Example cURL request for the new model:
     ```bash
     curl -X POST http://127.0.0.1:8000/aws-bedrock/mistral \
     -H "Authorization: Bearer <your-jwt-token>" \
     -H "Content-Type: application/json" \
     -d '{
         "model_id": "mistral-model-id",
         "system_prompt": "You are a helpful assistant.",
         "payload": {
           "temperature": 0.5,
           "max_tokens": 2000,
           "messages": [
             {"role": "user", "content": "Explain quantum computing."}
           ]
         }
     }'
     ```

6. **Document the New Model**:
   - Ensure that you update the `README.md` file with the details of the new model, including its `model_id`, required parameters, and any unique features.

7. **Deploy and Test**:
   - After updating the code, re-deploy the application (using Docker if necessary), and ensure the new model works as expected.

## Conclusion

This project provides a robust framework for interacting with AWS Bedrock models using FastAPI. By following the installation and usage instructions, you can quickly set up the application and start making requests to the API. The provided endpoints allow for user authentication and model invocation, making it a powerful tool for developers looking to leverage AWS Bedrock's capabilities. Feel free to explore the codebase and customize it to fit your needs.
