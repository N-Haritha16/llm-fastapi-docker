from fastapi import APIRouter, Depends
from fastapi.concurrency import run_in_threadpool

from app.schemas import PromptRequest, LLMResponse
from app.model_provider import LLMProvider
from app.auth import verify_token

router = APIRouter()
llm = LLMProvider()


@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "service is running"}


@router.post(
    "/generate",
    response_model=LLMResponse,
    dependencies=[Depends(verify_token)],
)
async def generate_text(request: PromptRequest) -> LLMResponse:
    print("ENTER /generate, prompt:", request.prompt)

    def _run():
        print("ENTER _run")
        return llm.generate(request.prompt, request.max_new_tokens)

    result = await run_in_threadpool(_run)
    print("RESULT:", result)
    return LLMResponse(generated_text=result)
