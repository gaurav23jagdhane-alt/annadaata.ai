import os
import google.generativeai as genai
from dotenv import load_dotenv
 
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# "flash-lite" answers faster. For smarter but slower answers, change to "gemini-2.5-flash".
MODEL_NAME = "gemini-2.5-flash-lite"
model = genai.GenerativeModel(
    MODEL_NAME,
    generation_config={"max_output_tokens": 500, "temperature": 0.4},
)
 
SYSTEM_RULES = (
    "You are Annadaata, a friendly farming assistant for Kerala farmers. "
    "Always reply in simple Malayalam (the farmer may write in Malayalam or Manglish). "
    "Keep answers short (under 100 words), practical, step by step. "
    "If you are not sure, tell the farmer to contact the nearest Krishi Bhavan."
)
 
 
def ask_text(question, context=""):
    prompt = f"{SYSTEM_RULES}\n\nExtra info: {context}\n\nFarmer asks: {question}"
    return model.generate_content(prompt).text
 
 
def ask_audio(audio_bytes, mime_type="audio/ogg", context=""):
    # WhatsApp voice notes are .ogg. Gemini can listen to them directly (speech-to-text + answer).
    prompt = f"{SYSTEM_RULES}\n\nExtra info: {context}\n\nListen to the farmer's voice note and answer."
    audio = {"mime_type": mime_type, "data": audio_bytes}
    return model.generate_content([prompt, audio]).text
 
 
def explain_disease(disease_name, confidence, crop_context=""):
    prompt = (
        f"{SYSTEM_RULES}\n\nOur leaf scan says: {disease_name} "
        f"(confidence {confidence:.0%}). {crop_context}\n"
        "Explain in Malayalam: what it is, 3 simple treatment steps, and prevention tips."
    )
    return model.generate_content(prompt).text
 
 
def diagnose_with_gemini_vision(image):
    # Backup when our CNN is not trained yet (good for first demo).
    prompt = SYSTEM_RULES + "\n\nLook at this leaf photo. Name the likely disease and give treatment in Malayalam."
    return model.generate_content([prompt, image]).text
 
