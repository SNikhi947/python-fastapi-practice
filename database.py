import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

d_url=os.getenv('DATABASE_URL', 'sqlite:///./students.db')
if "sqlite" in d_url:
    engine = create_engine(d_url, connect_args={"check_same_thread": False})
else:
    engine = create_engine(d_url)

SessionLocal=sessionmaker(bind=engine,autocommit=False,autoflush=False)
Base=declarative_base()
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()