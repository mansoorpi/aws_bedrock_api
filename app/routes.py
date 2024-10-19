# app/routes.py
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBearer, HTTPBasicCredentials, HTTPAuthorizationCredentials
from .auth import authenticate_user, create_access_token
from .auth import verify_token
from datetime import timedelta
from .models import Token, BedrockRequest, Token, BedrockResponse
from .config import settings
import boto3
from .config import settings
from jose import JWTError
import json
from .providers.aws_handler import invoke_bedrock_model

router = APIRouter()

security = HTTPBasic()


# /login route for user authentication and JWT token generation
@router.post("/login", response_model=Token, summary="Login and get JWT token")
def login(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Generate a JWT token using username and password.

    - **username**: Your account username
    - **password**: Your account password
    - **response**: Returns a JWT token if authentication is successful
    """
    # Authenticate the user using credentials
    is_authenticated = authenticate_user(credentials.username, credentials.password)
    if not is_authenticated:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    # Create a JWT token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": credentials.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Define route for AWS Bedrock with Anthropic models
# Secure the route with Bearer token
@router.post("/aws-bedrock/anthropic", 
    response_model=BedrockResponse,
    summary="Invoke Anthropic Claude model via AWS Bedrock",
    description="""
        This route allows you to invoke the Anthropic Claude model using AWS Bedrock.

        ### Required Fields:
        - **model_id**: The ID of the model to invoke (e.g., anthropic.claude-3-5-sonnet-20240620-v1:0).
        - **payload.anthropic_version**: The API version for Bedrock (e.g., bedrock-2023-05-31).
        - **payload.messages**: A list of message objects representing the conversation history. Each message should have:
            - **role**: Either "user" or "assistant".
            - **content**: The content of the message (text).

        ### Optional Fields:
        - **system_prompt**: A system prompt to prepend to the conversation (for context or instructions).
        - **payload.max_tokens**: Maximum number of tokens to generate.
        - **payload.temperature**: Controls the randomness of the output. Values between 0 and 1 are accepted.
        - **payload.top_p**: Controls diversity via nucleus sampling. Typical values are between 0 and 1.
        - **payload.top_k**: Controls how many of the top tokens are considered during sampling.
        - **payload.stop_sequences**: List of sequences where generation stops.
        - **payload.streaming**: Enable streaming for response generation.
        - **payload.guardrail_id**: Optional guardrail ID to restrict responses to predefined rules.
        - **payload.guardrail_version**: Version of the guardrail to apply.
    """
)
async def invoke_anthropic_model(
    request: BedrockRequest, 
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    token = credentials.credentials
    verify_token(token)  # Ensure token verification logic is in place
    return await invoke_bedrock_model(request)