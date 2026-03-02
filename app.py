from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image
import io

app = FastAPI()

# CORS allow (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "NEXO AI Backend Running (CPU Mode)"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    try:
        input_bytes = await file.read()
        output_bytes = remove(input_bytes)

        return StreamingResponse(
            io.BytesIO(output_bytes),
            media_type="image/png"
        )
    except Exception as e:
        return {"error": str(e)}
