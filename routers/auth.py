from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.user import User
from utils.hashing import verify_password,converthash
from utils.jwt import tokengen

router=APIRouter()

class usercreate(BaseModel):
    username:str
    password:str

class token(BaseModel):
    access_token:str
    token_type:str

@router.post("/register",status_code=201)
def userregister(u:usercreate,db:Session=Depends(get_db)):
    existing=db.query(User).filter(User.username==u.username).first()
    if existing:
        raise HTTPException(status_code=400,detail="user already exist")
    new_user=User(
        username=u.username,
        Hashedpassword=converthash(u.password)
    )
    db.add(new_user)
    db.commit()
    return {"message":"account created for u "}

@router.post("/login",response_model=token)
def login(u:usercreate,db:Session=Depends(get_db)):
    found=db.query(User).filter(User.username==u.username).first()
    if not found or not verify_password(u.password,found.Hashedpassword):
        raise HTTPException(status_code=401,detail="Invalid credentials")
    return {
        "access_token": tokengen(found.username),
        "token_type":"bearer"
    }
