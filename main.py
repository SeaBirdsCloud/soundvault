from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

songs_db = []

class SongLink(BaseModel):
    url: str

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/songs")
def list_songs():
    return songs_db

@app.post("/add_link")
def add_song(song: SongLink):
    url = song.url.strip()

    if "youtube.com/watch?v=" not in url:
        return {"error": "Somente links do YouTube são suportados."}

    video_id = url.split("v=")[1].split("&")[0]

    song_data = {
        "id": len(songs_db) + 1,
        "title": f"Música {random.randint(1,99)}",
        "artist": "Desconhecido",
        "thumbnail": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
        "video_id": video_id
    }
    songs_db.append(song_data)
    return {"message": "Música adicionada!", "song": song_data}

@app.delete("/songs/{song_id}")
def delete_song(song_id: int):
    global songs_db
    songs_db = [s for s in songs_db if s["id"] != song_id]
    return {"message": "Música removida"}

@app.post("/reorder")
def reorder_songs(new_order: list[int]):
    global songs_db
    reordered = []
    for i in new_order:
        song = next((s for s in songs_db if s["id"] == i), None)
        if song:
            reordered.append(song)
    songs_db = reordered
    return {"message": "Playlist reordenada!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
