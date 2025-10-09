# File: tts_server.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from TTS.api import TTS
import uuid

app = FastAPI()

# Load pre-trained Bengali TTS model (Tacotron2)
tts = TTS(model_name="tts_models/bn/bengali/tacotron2-DDC", progress_bar=False, gpu=False)

class TextInput(BaseModel):
    text: str

@app.post("/generate")
def generate_audio(data: TextInput):
    audio_path = f"outputs/{uuid.uuid4().hex}.wav"
    tts.tts_to_file(text=data.text, file_path=audio_path)
    return { "audioUrl": f"http://localhost:8000/{audio_path}" }

