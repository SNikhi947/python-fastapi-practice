import os
import traceback

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types

from dependencies import get_current_user

# Load environment variables
load_dotenv()

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)

# Check API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set")

# Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Model
modelname = "gemini-2.0-flash"

# Config
g_config = types.GenerateContentConfig(
    temperature=0.2
)

# System Prompt
System_context = """
You are the "Kuppam Student Portal Assistant," a specialized AI built to help users understand 
a Student Management System database and general educational concepts.

STRICT OPERATING RULES:

1. SUBJECT MATTER:
You only answer questions regarding:
- Student Database
- CRUD Operations
- SQLite
- FastAPI
- Python Programming
- React/Web Development
- Education

2. OUT-OF-SCOPE:
If a user asks about anything else (recipes, celebrities, sports, politics, etc.),
politely respond:
"I am specialized in the Student Management System and Education.
Please ask a question related to your studies or the database."

3. DATABASE CONTEXT:
Help teachers and students understand:
- Student ID
- Name
- Email
- Major
- FastAPI backend
- SQLite database interactions

4. TONE:
Be professional, concise, and encouraging.

5. FORMAT:
- Use bullet points when needed
- Use markdown code blocks for code
- Give detailed answers
"""

# Request Schema
class AskQuestion(BaseModel):
    question: str

# Response Schema
class AskResponse(BaseModel):
    answer: str

# AI Route
@router.post("/ask", response_model=AskResponse)
def ask_ai(
    request: AskQuestion,
    current_user=Depends(get_current_user)
):
    fullprompt = f"""
{System_context}

Student Question:
{request.question}
"""

    try:
        response = client.models.generate_content(
            model=modelname,
            contents=fullprompt,
            config=g_config
        )

        return AskResponse(answer=response.text)

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="This question could not be answered. Please rephrase it."
        )

    except Exception as e:
        traceback.print_exc()

        raise HTTPException(
            status_code=503,
            detail=f"Gemini Error: {str(e)}"
        )