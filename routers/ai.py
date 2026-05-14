import os
from dependencies import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types

router = APIRouter(prefix="/ai", tags=["AI"])

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

model_name = "gemini-2.5-flash-lite"

# Fixed typo from g_congif to g_config
g_config = types.GenerateContentConfig(
    temperature=0.2
)

System_context = """Answer any question related to the education"""

class AskQuestion(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str

@router.post("/ask", response_model=AskResponse)
async def ask_ai(request: AskQuestion, current_user=Depends(get_current_user)):
    full_prompt = f"{System_context}\n\n Student Question: {request.question}"
    
    try:
        res = client.models.generate_content(
            model=model_name,
            contents=full_prompt,
            config=g_config
        )
        
        return AskResponse(answer=res.text)

    except Exception as e:
        print(f"Detailed Gemini Error: {str(e)}")  
        raise HTTPException(
            status_code=500,
            detail=f"AI Error: {str(e)}"
        )