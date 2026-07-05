import json, pdfplumber, io, easyocr
from pathlib import Path
from docx import Document
from docx import Document
from PIL import Image
import numpy as np
from fastapi import HTTPException, status, UploadFile

from app.core.openai_client import create_chat_completion
from app.models.request import MarriageMatchRequest
from app.models.response import MarriageMatchResponse

reader = easyocr.Reader(['en', 'hi'])
PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


class MarriageService:
    def __init__(self) -> None:
        self.marriage_prompt = self._load_prompt("marriage_prompt.txt")
        self.kundli_prompt = self._load_prompt("kundli_prompt.txt")

    @staticmethod
    def _load_prompt(filename: str) -> str:
        prompt_path = PROMPTS_DIR / filename
        return prompt_path.read_text(encoding="utf-8").strip()

    async def analyze_match(
        self,
        bride_file: UploadFile,
        groom_file: UploadFile,
        kundli_file: UploadFile | None = None
    ) -> MarriageMatchResponse:

        prompt = await self._build_user_message(
            bride_file,
            groom_file,
            kundli_file
        )

        content = await create_chat_completion(prompt)

        return self._parse_response(content)


    async def extract_text(self, file: UploadFile) -> str:
        content = await file.read()

        content_type = file.content_type or ""

        if file.content_type == "text/plain":
            return content.decode("utf-8", errors="ignore")

        elif file.content_type == "application/pdf":
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                return "\n".join([p.extract_text() or "" for p in pdf.pages])

        elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(io.BytesIO(content))
            return "\n".join([p.text for p in doc.paragraphs])

        elif content_type.startswith("image/"):
            try:
                import cv2
                import numpy as np

                image = Image.open(io.BytesIO(content)).convert("RGB")

                # 🔥 Resize (huge speed gain)
                image.thumbnail((1024, 1024))

                img = np.array(image)

                # 🔥 Convert to grayscale
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # 🔥 OCR (optimized)
                result = reader.readtext(
                    gray,
                    detail=0,
                    paragraph=True
                )

                text = " ".join(result)

                return text.strip()

            except Exception as e:
                return f"OCR failed: {str(e)}"

        else:
            return "Unsupported file format"


    async def _build_user_message(
        self,
        bride_file: UploadFile,
        groom_file: UploadFile,
        kundli_file: UploadFile | None
    ) -> str:

        bride_text = await self.extract_text(bride_file)
        groom_text = await self.extract_text(groom_file)

        kundli_text = None
        if kundli_file:
            kundli_text = await self.extract_text(kundli_file)

        sections = [
            # 🔥 ADD THIS BLOCK (IMPORTANT)
            "- Detect the primary language of the bride and groom biodata",
            "- The response MUST be in that SAME language",
            "- If biodata is in Marathi → respond in Marathi",
            "- If biodata is in Hindi → respond in Hindi",
            "- If biodata is in English → respond in English",
            "- Do NOT mix languages",
            self.marriage_prompt,
            "",
            self.kundli_prompt,
            "",
            "Bride biodata:",
            bride_text,
            "",
            "Groom biodata:",
            groom_text,
            "",
            "Kundli details:",
            kundli_text,
            "",
            "Strictly return only JSON."
        ]

        return "\n".join(sections)

    @staticmethod
    def _parse_response(content: str) -> MarriageMatchResponse:
        normalized = content.strip()
        if normalized.startswith("```"):
            normalized = normalized.strip("`")
            normalized = normalized.removeprefix("json").strip()

        try:
            payload = json.loads(normalized)
        except json.JSONDecodeError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Gemini returned invalid JSON.",
            ) from exc

        try:
            return MarriageMatchResponse.model_validate(payload)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Gemini response did not match the expected schema.",
            ) from exc