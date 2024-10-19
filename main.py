from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer

app = FastAPI()

# Define Bearer Token Security Scheme
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="AWS Bedrock API By MPI",
        version="1.0.0",
        description="This is a custom FastAPI application with JWT authentication to access AWS Bedrock foundational models.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for route in openapi_schema["paths"].values():
        for operation in route.values():
            operation["security"] = [{"bearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Assign the custom OpenAPI schema
app.openapi = custom_openapi

# Import and include routes (assuming your routes are defined in `app/routes.py`)
from app.routes import router
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
