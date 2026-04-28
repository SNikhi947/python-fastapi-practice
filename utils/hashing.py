from passlib.context import CryptContext

cry=CryptContext(schemes=["bcrypt"],deprecated="auto")
def converthash(password : str) -> str:
    return cry.hash(password)

def verify_password(plain: str,hased: str) -> bool:
    return cry.verify(plain,hased)