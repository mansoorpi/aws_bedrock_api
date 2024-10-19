from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from .providers import aws_handler

class ModelRoutingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        body = await request.json()
        
        provider = body.get("provider")

        if provider == "aws_bedrock":
            # Route request to AWS Bedrock handler
            return await aws_handler.invoke_bedrock_model(request)
        else:
            raise HTTPException(status_code=400, detail="Unsupported provider.")
