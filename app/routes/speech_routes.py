from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File, Form

from app.models.response import VoiceCloneResponse
from app.services.voice_clone_service import VoiceCloneService

router = APIRouter()

def get_voice_clone_service() -> VoiceCloneService:
    return VoiceCloneService()

@router.post("/voice-clone")
async def voice_clone(
    reference_audio: Optional[UploadFile] = File(None),
    reference_text: Optional[str] = Form(None),
    text: Optional[str] = Form(None),
    language: Optional[str] = Form(None),
    speed: Optional[float] = Form(None),
    service: VoiceCloneService = Depends(get_voice_clone_service),
):
    await service.generate_voice(
        reference_audio=reference_audio,
        reference_text=reference_text,
        text=text,
        language=language,
        speed=speed,
    )