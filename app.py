from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
import io

app = FastAPI()

@app.get("/")
def home():
    return {"message": "NEXO AI Backend Running"}

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    input_bytes = await file.read()
    output_bytes = remove(input_bytes)

    return StreamingResponse(
        io.BytesIO(output_bytes),
        media_type="image/png"
    )
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image
import io

app = FastAPI()

@app.get("/")
def home():
    return {"message": "NEXO AI Backend Running"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    input_bytes = await file.read()
    output = remove(input_bytes)
    return StreamingResponse(io.BytesIO(output), media_type="image/png")
