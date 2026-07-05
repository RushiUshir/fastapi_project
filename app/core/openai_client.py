import asyncio

from fastapi import HTTPException, status
from google import genai
from google.genai import errors

from app.core.config import get_settings

_client: genai.Client | None = None


def get_openai_client() -> genai.Client:
    global _client

    settings = get_settings()
    if not settings.gemini_api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="GEMINI_API_KEY is not configured.",
        )

    if _client is None:
        _client = genai.Client(api_key=settings.gemini_api_key)

    return _client


async def create_chat_completion(
    prompt: str,
    *,
    temperature: float = 0.2,
) -> str:
    settings = get_settings()
    client = get_openai_client()

    try:
        response = await asyncio.to_thread(
            client.models.generate_content,
            model=settings.gemini_model,
            contents=prompt,
            config={
                "temperature": temperature,
                "response_mime_type": "application/json",
            },
        )
    except errors.ClientError as exc:
        status_code = getattr(exc, "code", None)
        if status_code == 429:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Gemini rate limit exceeded.",
            ) from exc
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Gemini request failed.",
        ) from exc
    except (errors.ServerError, errors.APIError) as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Gemini service is temporarily unavailable.",
        ) from exc

    content = response.text
    if not content:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Gemini returned an empty response.",
        )
    return content
