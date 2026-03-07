from fastapi.security import APIKeyHeader
from fastapi import Depends, HTTPException, Security
import os
from dotenv import load_dotenv

load_dotenv()

auth_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

API_KEY = os.getenv("API_KEY")

def verify_api_key(api_key: str = Security(auth_header)):
    if not api_key:
        raise HTTPException(status_code=401, detail="No API key provided")
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")