# app/models.py
from pydantic import BaseModel, Field
from typing import List, Optional
# Model for holding user credentials (login)
class UserCredentials(BaseModel):
    username: str
    password: str

# Model for the JWT token response
class Token(BaseModel):
    access_token: str
    token_type: str

# Model for bedrock invocation request
class BedrockRequest(BaseModel):
    model_id: str
    prompt: str  # The prompt string directly in the request
    max_tokens: int
    temperature: float
    top_p: float

# Message model for handling user/assistant messages
class Message(BaseModel):
    role: str = Field(..., description="The role of the message sender ('user' or 'assistant').")
    content: str = Field(..., description="The content of the message.")

# Payload model for AWS Bedrock API
class Payload(BaseModel):
    anthropic_version: str = Field(..., description="Anthropic API version (e.g., 'bedrock-2023-05-31').")
    messages: List[Message] = Field(..., description="A list of messages representing the conversation.")
    max_tokens: Optional[int] = Field(None, description="The maximum number of tokens to generate.")
    temperature: Optional[float] = Field(None, description="Controls randomness of the output (e.g., 0.7).")
    top_p: Optional[float] = Field(None, description="Controls diversity via nucleus sampling (e.g., 0.9).")
    top_k: Optional[int] = Field(None, description="Controls how many of the top tokens are considered during sampling.")
    stop_sequences: Optional[List[str]] = Field(None, description="List of sequences where generation stops.")
    streaming: Optional[bool] = Field(False, description="Enable streaming for response generation.")
    guardrail_id: Optional[str] = Field(None, description="Optional guardrail ID to apply.")
    guardrail_version: Optional[str] = Field(None, description="Optional guardrail version to apply.")

# Bedrock Request model
class BedrockRequest(BaseModel):
    model_id: str = Field(..., description="The ID of the Anthropic model to invoke.")
    system_prompt: Optional[str] = Field(None, description="Optional system-level prompt.")
    payload: Payload

class BedrockResponse(BaseModel):
    result: str = Field(..., description="The result returned from the invoked model.")
