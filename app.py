from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from rembg import remove, new_session
from PIL import Image
import io

app = FastAPI()

# ✅ Load light model once (important for RAM)
session = new_session("u2netp")

@app.get("/")
def home():
    return {"message": "NEXO AI Backend Running - Optimized Free Version"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):

    input_bytes = await file.read()

    # ✅ 2MB size limit (free server safe)
    if len(input_bytes) > 2 * 1024 * 1024:
        return JSONResponse(
            content={"error": "Image too large. Max 2MB allowed."},
            status_code=400
        )

    try:
        # ✅ Resize image to reduce RAM usage
        image = Image.open(io.BytesIO(input_bytes))
        image.thumbnail((800, 800))  # maintain aspect ratio

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        resized_bytes = buffer.getvalue()

        # ✅ Remove background
        output_bytes = remove(resized_bytes, session=session)

        return StreamingResponse(
            io.BytesIO(output_bytes),
            media_type="image/png"
        )

    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )
