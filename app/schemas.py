from pydantic import BaseModel


class PromptRequest(BaseModel):
    prompt: str
    max_new_tokens: int | None = None


class LLMResponse(BaseModel):
    generated_text: str
