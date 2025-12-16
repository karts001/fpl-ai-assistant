from google import genai

from backend.app.llm.base_llm import BaseLLM


class GeminiLLM(BaseLLM):
  def __init__(self, api_key: str, model: str):
    super().__init__(api_key, model)
    self.client = genai.Client(api_key=api_key)

  def generate_content(self, prompt: str) -> str:
    """Generate content implementation for Gemini LLM

    Args:
        prompt (str): Prompt to pass to the LLM

    Raises:
        Exception: If the LLM request fails

    Returns:
        str: Generated content from the LLM
    """
    try:
      response = self.client.models.generate_content(
        model=self.model,
        contents=prompt,
      )
      return response.text
    
    except Exception as e:
      raise Exception(f"LLM request failed: {str(e)}")
  
  async def generate_content_async(self, prompt: str) -> str:
    """Async version of generate_content

    Args:
        prompt (str): Prompt to pass to the LLM

    Raises:
        Exception: If the LLM request fails

    Returns:
        str: Generated content from the LLM
    """
    try:
      response = await self.client.aio.models.generate_content(
        model=self.model,
        contents=prompt,
      )
      return response

    except Exception as e:
      raise Exception(f"LLM request failed: {str(e)}")