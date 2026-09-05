from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import yt_dlp
import os
import uuid

app = FastAPI()

DOWNLOAD_KEY = os.getenv("DOWNLOAD_KEY", "")

class DownloadRequest(BaseModel):
    url: str


@app.get("/")
def home():
    return {"status": "online"}


@app.post("/download")
def download_video(
    request: DownloadRequest,
    x_api_key: str = Header(default="")
):
    if DOWNLOAD_KEY and x_api_key != DOWNLOAD_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    file_id = str(uuid.uuid4())
    output = f"/tmp/{file_id}.%(ext)s"

    options = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "merge_output_format": "mp4",
        "outtmpl": output,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([request.url])

        mp4_file = f"/tmp/{file_id}.mp4"

        if not os.path.exists(mp4_file):
            raise HTTPException(
                status_code=500,
                detail="MP4 file was not created"
            )

        return FileResponse(
            mp4_file,
            media_type="video/mp4",
            filename=f"{file_id}.mp4"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
