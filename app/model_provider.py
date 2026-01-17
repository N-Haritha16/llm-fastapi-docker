from typing import Optional
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from app.config import settings

class LLMProvider:
    _model: Optional[AutoModelForCausalLM] = None
    _tokenizer: Optional[AutoTokenizer] = None

    def _ensure_loaded(self) -> None:
        if self._model is None or self._tokenizer is None:
            self._tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_NAME)
            self._model = AutoModelForCausalLM.from_pretrained(settings.MODEL_NAME)

    def generate(self, prompt: str, max_new_tokens: int | None = None) -> str:
        self._ensure_loaded()

        # Cap tokens so it stays fast
        requested = max_new_tokens or settings.MAX_NEW_TOKENS
        max_tokens = min(requested, settings.MAX_NEW_TOKENS)

        inputs = self._tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = self._model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                do_sample=True,
                top_p=0.9,
                temperature=0.8,
            )

        text = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
        text = text.rstrip()
        text = " ".join(text.split())
        return text
