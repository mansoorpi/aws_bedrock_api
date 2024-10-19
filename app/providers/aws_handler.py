import boto3
import json
from fastapi import HTTPException
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

def prepend_system_prompt(payload, system_prompt):
    """Prepend system prompt to the first user message."""
    if payload.get('messages'):
        first_message = payload['messages'][0]
        if first_message.get('role') == 'user':
            first_message['content'] = f"{system_prompt} {first_message['content']}"
    return payload

def clean_payload(payload):
    """Remove fields that are None or default values from the payload."""
    return {k: v for k, v in payload.items() if v is not None and v != False}

async def invoke_bedrock_model(request):
    """Invoke AWS Bedrock with the provided request data"""
    
    # Convert request to a dictionary
    body = request.dict()  
    payload = body.get("payload")
    model_id = body.get("model_id")
    
    # Check if the system prompt is provided
    system_prompt = body.get("system_prompt", "")
    
    if not model_id:
        raise HTTPException(status_code=400, detail="model_id is required.")
    
    # Ensure required payload parameters
    if "messages" not in payload or "anthropic_version" not in payload:
        raise HTTPException(status_code=400, detail="'messages' and 'anthropic_version' are required.")

    # Prepend system prompt if provided
    if system_prompt:
        payload = prepend_system_prompt(payload, system_prompt)

    # Clean the payload to remove optional fields that are not provided or are default values
    cleaned_payload = clean_payload(payload)

    # AWS Bedrock Client
    client = boto3.client(
        'bedrock-runtime', 
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION")
    )

    try:
        # Serialize cleaned payload to bytes
        payload_bytes = json.dumps(cleaned_payload).encode('utf-8')

        # Invoke the model using Bedrock's API
        response = client.invoke_model(
            modelId=model_id,
            contentType='application/json',
            accept='application/json',
            body=payload_bytes
        )

        # Return the response
        return {"result": response['body'].read()}  # Read and return response body

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bedrock invocation failed: {str(e)}")
