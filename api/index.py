from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

@app.post("/api/count")
async def count_words(request: TextRequest):
    words = [w for w in request.text.split() if w.strip()]
    return {"count": len(words)}

# Vercel looks for 'app' in api/index.py
