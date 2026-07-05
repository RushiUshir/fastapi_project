import os
import shutil
from uuid import uuid4
from typing import Optional

from fastapi import UploadFile

from app.models.response import VoiceCloneResponse

class VoiceCloneService:
    OUTPUT_DIR = "uploads/generated"

    def __init__(self):
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)

    async def generate_voice(
        self,
        reference_audio: Optional[UploadFile],
        reference_text: Optional[str],
        text: Optional[str],
        language: Optional[str],
        speed: Optional[float],
    ) -> VoiceCloneResponse:
        """
        Generate cloned voice and return response.
        Replace the placeholder logic with your TTS model.
        """

        # Save uploaded reference audio (optional)
        reference_audio_path = None

        if reference_audio:
            ext = os.path.splitext(reference_audio.filename)[1]
            reference_audio_path = os.path.join(
                self.OUTPUT_DIR,
                f"{uuid4()}{ext}"
            )

            with open(reference_audio_path, "wb") as buffer:
                shutil.copyfileobj(reference_audio.file, buffer)

        output_path = voice_clone_model.generate(
            reference_audio=reference_audio_path,
            reference_text=reference_text,
            text=text,
            language=language,
            speed=speed,
        )

        # Placeholder output
        output_file = os.path.join(self.OUTPUT_DIR, "output.wav")

        return VoiceCloneResponse(
            file_name=os.path.basename(output_file),
            file_path=output_file,
            content_type="audio/wav",
            message="Voice cloned successfully."
        )