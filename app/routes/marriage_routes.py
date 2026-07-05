from fastapi import APIRouter, Depends, UploadFile, File
from typing import Optional

from app.models.request import MarriageMatchRequest
from app.models.response import MarriageMatchResponse
from app.services.marriage_service import MarriageService

router = APIRouter()


def get_marriage_service() -> MarriageService:
    return MarriageService()

@router.post("/match", response_model=MarriageMatchResponse)
async def match_biodata(
    bride_biodata: UploadFile = File(...),
    groom_biodata: UploadFile = File(...),
    kundli: Optional[UploadFile] = File(None),
    service: MarriageService = Depends(get_marriage_service),
):
    return await service.analyze_match(
        bride_biodata,
        groom_biodata,
        kundli
    )
