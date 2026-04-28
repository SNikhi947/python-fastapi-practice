from fastapi import Depends,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.orm import Session

from database import get_db
from utils.jwt import tokenver
from models.user import User

berr=HTTPBearer()

def get_current_user(ce: HTTPAuthorizationCredentials=Depends(berr), db: Session=Depends(get_db)):
    token=ce.credentials
    try:
        username=tokenver(token)
    except JWTError:
        raise HTTPException(status_code=401,detail="token is expired")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401,detail="user not found")
    return user
