import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv() 
from database import Base, engine
from routers import auth, students, ai

import models.user  
import models.student
  
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Management API", version="1.0.0")

origins = [
    os.getenv("FRONTEND_URL", "https://student-management-system-sage-two.vercel.app"),
    "http://localhost:5173",  # Vite default port
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Use the list here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(students.router, prefix="/students", tags=["Students"])
app.include_router(ai.router)

@app.get("/")
def root():
    return {"message": "Student API is running"}
