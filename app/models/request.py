from pydantic import BaseModel, Field
from fastapi import FastAPI, UploadFile, File
from typing import Optional

class MarriageMatchRequest(BaseModel):
    bride_biodata: UploadFile = File(...),
    groom_biodata: UploadFile = File(...),
    kundli: Optional[UploadFile] = File(None)
