from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

app = FastAPI()

# Enable CORS (still useful if developing, though less critical if serving from same origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

@app.post("/count")
async def count_words(request: TextRequest):
    # Simple word count logic: split by whitespace and filter empty strings
    words = [w for w in request.text.split() if w.strip()]
    return {"count": len(words)}

# Mount the static directory (after API routes to avoid conflicts)
# We assume 'frontend/dist' is at the sibling level relative to 'backend/'
# Construct path relative to this file
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dist = os.path.join(current_dir, "../frontend/dist")

if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Serve index.html for any other path (SPA routing)
        # Check if the file exists in dist, otherwise serve index
        potential_path = os.path.join(frontend_dist, full_path)
        if os.path.isfile(potential_path):
            return FileResponse(potential_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))
else:
    print(f"Warning: Frontend build directory not found at {frontend_dist}")

@app.get("/api/health")
async def health():
    return {"message": "Word Counter API is running"}
