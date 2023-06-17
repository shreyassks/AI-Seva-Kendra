from fastapi import (
    FastAPI,
    Response,
    status,
    Request,
    Header,
    UploadFile,
    Form,
    File,
    HTTPException,
)
from fastapi.middleware.cors import CORSMiddleware
import logging

import uuid
from dotenv import load_dotenv
from tools import Tools
import os
from fastapi.responses import StreamingResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from langchain.chat_models import ChatOpenAI
import time
import chardet


import torch
from transformers import pipeline

import openai


from ttsmms import download, TTS

dir_path = download("hin", "./data")
tts = TTS(dir_path)

tools_obj = Tools(llm=ChatOpenAI(temperature=0, model_name="gpt-4"))
device = "cuda:0" if torch.cuda.is_available() else "cpu"
# transcribe = pipeline(
#     task="automatic-speech-recognition",
#     model="vasista22/whisper-hindi-small",
#     chunk_length_s=30,
#     device=device,
# )
# transcribe.model.config.forced_decoder_ids = (
#     transcribe.tokenizer.get_decoder_prompt_ids(language="hi", task="transcribe")
# )
load_dotenv()

# setting logging
logging.basicConfig(
    level=(logging.DEBUG if os.getenv("LOG_MODE") == "DEBUG" else logging.INFO)
)

openai.api_key = os.getenv("OPENAI_API_KEY")

# Handling envs
origins = os.getenv("FRONTEND_ORIGINS")
if not origins:
    raise Exception("FRONTEND_ORIGINS env not found. Exiting...")

# Setting up app
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
]

app = FastAPI(middleware=middleware)

from pydantic import BaseModel


###################### SIGN IN/ SIGN UP ##########################
global USER_NAME
global USER_ADDRESS
global USER_PINCODE


class LoginRequest(BaseModel):
    user_name: str
    user_address: str
    user_pincode: int


@app.post("/signin")
async def signin(req: LoginRequest, resp: Response):
    USER_NAME = (req.user_name,)
    USER_ADDRESS = (req.user_address,)
    USER_PINCODE = req.user_pincode
    return "OK"


######################## CONVERSATION #######################

# def speechToText(audio):
#     return transcribe(audio)["text"]


def textToSpeech(txt, audio_path):
    tts.synthesis(txt, wav_path=audio_path)


def make_header_safe(header_value):
    # Escape special characters
    header_value = header_value.replace("\\", "")
    header_value = header_value.replace('"', "")
    header_value = header_value.replace("\n", "")
    header_value = header_value.replace("\r", "")
    header_value = header_value.replace("\t", "")

    # Wrap the string in single quotes
    header_value = f"'{header_value}'"

    return header_value


@app.post("/conversation/submit-audio")
async def submit_audio(resp: Response, audio: UploadFile = File(...)):
    # file_location = (
    #     f"audio_files/{audio.filename}"  # saving file for now - TODO: remove this line
    # )
    # with open(file_location, "wb") as file:
    #     file.write(await audio.read())

    # stt_transcript = "मैं आधार पर अपना पता बदलना चाहता हूं, लेकिन मेरे पास एड्रेस प्रूफ नहीं है। निकटतम आधार केंद्र कौन सा है जहां मैं जा सकता हूं। मैं Indiranagar, bangalore में रहता हूँ"  # speechToText(file_location)
    stt_transcript = "What is the process I need to follow to my Aadhaar address. After this my location is Indiranagar bangalore, where is the nearest aadhaar center?"

    ai_response = tools_obj.aadhar_uadai_tool(stt_transcript)

    message_list = [
        {
            "role": "system",
            "content": "Conclude the text in under 20 words. Then translate English to hindi. GIve output in devnagari script.",
        },
        {
            "role": "user",
            "content": ai_response,
        },
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=message_list,
        temperature=0.7,
    )

    system_message = response["choices"][0]["message"]["content"]

    # setting the answer in header
    headers = {
        "X-Response-Answer-ai": make_header_safe(ai_response),
        "X-Response-Answer-you": make_header_safe(stt_transcript),
    }

    # streaming audio
    audio_path = "audio_files/mySound.wav"
    textToSpeech(system_message, audio_path)

    def stream_audio():
        with open(audio_path, mode="rb") as audio_file:
            while chunk := audio_file.read(65536):
                yield chunk

    # time.sleep(5)

    # response = StreamingResponse(stream_audio(), media_type="audio/wav")

    # response.headers["X-Response-Answer"] = header_val.encode()

    return StreamingResponse(stream_audio(), media_type="audio/wav", headers=headers)


#################### EXCEPTION HANDLERS ##################


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logging.error(f"{request}: {exc_str}")
    content = {"status_code": 10422, "message": exc_str, "data": None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )
