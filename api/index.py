from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TextRequest(BaseModel):
    text: str

@app.post("/api/count")
async def count_words(request: TextRequest):
    words = [w for w in request.text.split() if w.strip()]
    return {"count": len(words)}

# Vercel looks for 'app' in api/index.py
