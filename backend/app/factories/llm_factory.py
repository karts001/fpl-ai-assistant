import os

from backend.app.llm.base_llm import BaseLLM
from backend.app.llm.gemini_llm import GeminiLLM


def get_llm() -> BaseLLM:

  provider = os.getenv("LLM_PROVIDER", "gemini").lower()

  if provider == 'gemini':

    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    return GeminiLLM(api_key=api_key, model=model)
  
  else:
    raise NotImplementedError(f"LLM provider '{provider}' is not supported.")