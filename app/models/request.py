from pydantic import BaseModel, Field
from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional

class MarriageMatchRequest(BaseModel):
    bride_biodata: UploadFile = File(...),
    groom_biodata: UploadFile = File(...),
    kundli: Optional[UploadFile] = File(None)

class VoiceCloneRequest(BaseModel):
    reference_audio: Optional[UploadFile] = File(None),
    reference_text: Optional[str] = Form(None),
    text: Optional[str] = Form(None),
    language: Optional[str] = Form(None),
    speed: Optional[float] = Form(None)
