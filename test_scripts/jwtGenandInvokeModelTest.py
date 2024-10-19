import requests
from requests.auth import HTTPBasicAuth

# Base URLs for the local FastAPI application
JWT_BASE_URL = "http://127.0.0.1:8000"
BEDROCK_BASE_URL = "http://127.0.0.1:8000"

# Service account credentials (adjust these as per your local .env or test values)
USERNAME = "testuser"
PASSWORD = "testpassword"

def test_token_generation():
    url = f"{JWT_BASE_URL}/login"  # Adjusted to the correct login route
    auth = HTTPBasicAuth(USERNAME, PASSWORD)
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, auth=auth)
        response.raise_for_status()  # Raises HTTPError if the status is 4xx/5xx
    except requests.exceptions.RequestException as e:
        print(f"Error during token generation: {e}")
        return None
    
    if response.status_code == 200:
        print("Token generation successful")
        token_data = response.json()
        return token_data["access_token"]
    else:
        print(f"Token generation failed. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def test_invoke_claude_3_sonnet(token):
    url = f"{BEDROCK_BASE_URL}/aws-bedrock/anthropic"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "model_id": "anthropic.claude-3-5-sonnet-20240620-v1:0",
        "system_prompt": "You are a helpful assistant that provides concise answers.",
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

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error invoking the model: {e}")
        print(f"Response: {response.text}")
        return
    
    if response.status_code == 200:
        print("Invoke Claude 3 Sonnet successful")
        print(f"Response: {response.json()}")
    else:
        print(f"Invoke Claude 3 Sonnet failed. Status code: {response.status_code}")
        print(f"Response: {response.text}")

def main():
    print("Testing locally deployed FastAPI application...")
    
    # Test token generation
    token = test_token_generation()
    
    if token:
        # Test invoke Claude 3 Sonnet
        test_invoke_claude_3_sonnet(token)
    else:
        print("Skipping Claude 3 Sonnet test due to token generation failure.")

if __name__ == "__main__":
    main()
