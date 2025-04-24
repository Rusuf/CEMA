import os
from fastapi import Security, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Key configuration
API_KEY = os.getenv("API_KEY", "dev_api_key_for_testing")
API_KEY_NAME = "X-API-Key"

# Define API Key header
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# API Key validation function
async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid API Key"
        ) 