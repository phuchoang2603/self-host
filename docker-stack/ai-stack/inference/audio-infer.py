from fastapi import FastAPI, Request
from fastapi.responses import Response
import logging
from xinference.client import Client

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()
client = Client("http://192.168.69.121:9997")
model_tts = client.get_model("F5-TTS")
model_stt = client.get_model("SenseVoiceSmall")

def transcribe_audio(model, audio_bytes):
    logging.info("Transcribing audio")
    response = model.transcriptions(audio=audio_bytes)
    logging.info("Transcription completed")
    return response["text"]

def generate_speech(model, text, prompt_text, prompt_speech_bytes):
    logging.info("Generating speech")
    response = model.speech(
        text,
        prompt_text=prompt_text,
        prompt_speech=prompt_speech_bytes
    )
    logging.info("Speech generation completed")
    return response

@app.post("/clone-voice/")
async def generate_speech_file(request: Request, text: str):
    prompt_speech_bytes: bytes = await request.body()
    prompt_text = transcribe_audio(model_stt, prompt_speech_bytes)
    speech_bytes = generate_speech(model_tts, text, prompt_text, prompt_speech_bytes)
    return Response(content=speech_bytes, media_type="audio/mpeg")

# Run the FastAPI app with Uvicorn
# $ uvicorn audio-infer-fastapi:app --reload
