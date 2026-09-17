import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from detector import detect_news

load_dotenv()

app = FastAPI(title="Reporter AI API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=10, max_length=20000)

@app.get("/health")
def health():
    return {"status": "ok", "service": "Reporter AI"}

@app.post("/api/analyze")
def analyze(request: AnalyzeRequest):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(500, "Falta OPENAI_API_KEY en el backend.")
    try:
        return detect_news(request.text)
    except Exception as exc:
        raise HTTPException(500, f"Error de análisis: {exc}")
