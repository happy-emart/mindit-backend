import os
import jwt
from typing import Optional
from fastapi import HTTPException, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
if not SUPABASE_JWT_SECRET:
    print("WARNING: SUPABASE_JWT_SECRET not set. Auth will fail.")

def verify_jwt(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    """
    Validates the JWT token from Supabase Auth.
    Returns the decoded token payload (including user_id/sub).
    """
    token = credentials.credentials
    
    try:
        # Supabase uses HS256 for signing tokens
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated" # Default audience for Supabase Auth
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        print(f"Auth Error: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")

def get_current_user_id(payload: dict = Security(verify_jwt)) -> str:
    """Dependency to get the current user's UUID from the JWT"""
    return payload.get("sub")
