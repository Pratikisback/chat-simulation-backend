from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from core.database import get_db
from features.user.model import User
from core.security import decode_token

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    print(token)

    if not token:
        raise HTTPException(status_code=401, detail="Token required")

    payload = decode_token(token)

    if isinstance(payload, dict) and "error" in payload:
        if payload["error"] == "signature_expired":
            raise HTTPException(status_code=401, detail="Token has expired")
        elif payload["error"] == "invalid_token":
            raise HTTPException(status_code=401, detail="Token is invalid")

    user = db.query(User).filter(User.email == payload["email"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    print(user.role)
    return user
