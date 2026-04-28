from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone

s_k="this-my-secrect-key-i-used-for-now"
algo="HS256"

def tokengen(username : str) -> str:
    payload={
        "sub":username,
        "exp":datetime.now(timezone.utc)+timedelta(minutes=30)
    }
    return jwt.encode(payload,s_k,algorithm=algo)

def tokenver(token :str) ->str:
    payload=jwt.decode(token,s_k,algorithms=[algo])
    username=payload.get("sub")
    if not username:
        raise JWTError("token is been expired")
    return username
