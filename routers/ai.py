import os
from dependencies import get_current_user
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,Field
from google import genai
from google.genai import types

router=APIRouter(prefix="/ai",tags=["AI"])

if not os.getenv("GEMINI_API_KEY"):
    raise RuntimeError("GEMINI_API_KEY is not set in .env")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

modelname="gemini-2.5-flash"
g_congif=types.GenerateContentConfig(
    temperature=0.2
)
System_context="""You are the "Kuppam Student Portal Assistant," a specialized AI built to help users understand 
a Student Management System database and general educational concepts.

STRICT OPERATING RULES:
1. SUBJECT MATTER: You only answer questions regarding the Student Database (CRUD, SQLite, 
   FastAPI integration), Python programming, Web Development (React), and Education.
2. OUT-OF-SCOPE: If a user asks about anything else (e.g., recipes, celebrities, sports, 
   politics, or general chat), you must politely decline by saying: 
   "I am specialized in the Student Management System and Education. Please ask a question 
   related to your studies or the database."
3. DATABASE CONTEXT: You help teacher understand how their data is stored (ID, Name, Email, 
   Major) and how the FastAPI backend interacts with the SQLite database.
4. TONE: Be professional, encouraging, and concise. Use simple analogies for technical concepts.
5. FORMAT: Use bullet points for steps and wrap code snippets in markdown blocks. 
   Have to give the answer in an detail version """

class AskQuestion(BaseModel):
    question:str
class AskResponse(BaseModel):
    answer:str

@router.post("/ask",response_model=AskResponse)
def ask_ai(request:AskQuestion,current_user=Depends(get_current_user)):
    fullprompt=f"{System_context}\n\n Student Question:{request.question}"
    try:
        res=client.models.generate_content(
        model=modelname,
        contents=fullprompt,
        config=g_congif
         )
        return AskResponse(answer=res.text)
    except ValueError:
        raise HTTPException(status_code=400,detail="This question could not be answered. Please rephrase it.")
    except Exception as e:
        print(f"Gemini error: {e}")  
        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable. Try again in a moment."
        )