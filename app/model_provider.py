from typing import Optional

from transformers import pipeline
from app.config import settings


class LLMProvider:
    _generator: Optional[object] = None

    def _ensure_loaded(self) -> None:
        if self._generator is None:
            print("Loading pipeline with model:", settings.MODEL_NAME)
            self._generator = pipeline(
                task="text-generation",
                model=settings.MODEL_NAME,  # no device_map here
            )

    def generate(self, prompt: str, max_new_tokens: int | None = None) -> str:
        print("ENTER LLMProvider.generate")
        self._ensure_loaded()

        # Force up to 64 new tokens by default
        max_tokens = max_new_tokens or 64
        print("max_tokens:", max_tokens)

        outputs = self._generator(
            prompt,
            max_new_tokens=max_tokens,
            do_sample=True,
            top_p=0.95,
            temperature=1.0,
        )

        text = outputs[0]["generated_text"]
        text = text.rstrip()
        text = " ".join(text.split())

        print("Generated text:", text[:200])
        return text
