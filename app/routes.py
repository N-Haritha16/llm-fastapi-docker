import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.concurrency import run_in_threadpool

from app.schemas import PromptRequest, LLMResponse
from app.model_provider import LLMProvider
from app.auth import verify_token

logger = logging.getLogger(__name__)

router = APIRouter()
llm = LLMProvider()

@router.post(
    "/generate",
    response_model=LLMResponse,
    dependencies=[Depends(verify_token)],
)
async def generate_text(request: PromptRequest) -> LLMResponse:
    """Generate text from the LLM in a thread pool for CPU-bound work."""

    def _run():
        return llm.generate(request.prompt, request.max_new_tokens)

    try:
        result = await run_in_threadpool(_run)
    except Exception as e:
        logger.exception("Error in /generate")
        # Return a JSON 500 instead of plain text
        raise HTTPException(status_code=500, detail=str(e))

    return LLMResponse(generated_text=result)
