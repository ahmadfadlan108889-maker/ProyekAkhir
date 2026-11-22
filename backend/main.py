from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dictionary_service import lookup_word

app = FastAPI(title="Asisten Literasi Jurnal Akademik API")

# Izinkan ekstensi Chrome menghubungi server lokal ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LookupRequest(BaseModel):
    word: str
    target_lang: str = "id"
    journal_title: str = "Jurnal Tanpa Judul"


@app.get("/")
def root():
    return {"status": "Server Asisten Literasi Jurnal aktif!"}


@app.post("/lookup")
def lookup(req: LookupRequest):
    hasil = lookup_word(req.word, target_lang=req.target_lang)
    hasil["journal_title"] = req.journal_title
    return hasil