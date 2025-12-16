from abc import ABC, abstractmethod


class BaseLLM(ABC):
  def __init__(self, api_key: str, model: str):
    """Base contract for all LLM implementations

    Args:
      api_key (str): LLM API key
      model (str): LLM model name

    Raises:
      ValueError: API key value error
      ValueError: Model name value error
    """
    if not api_key:
      raise ValueError("API key must be provided for LLM")
    
    if not model:
      raise ValueError("Model name must be provided for LLM")
    
    self.api_key = api_key
    self.model = model

  @abstractmethod
  def generate_content(self, prompt: str, **kwargs) -> str:
    """Concrete class will implement this method. This method should generate
    the content for the specific llm

    Args:
      prompt (str): Prompt to pass to the LLM
      **kwargs: Additional LLM-specific parameters (temperature, max_tokens, etc.)

    Returns:
      str: Generated content from the LLM

    Raises:
      Exception: If the LLM request fails
    """
    pass

  @abstractmethod
  async def generate_content_async(self, prompt: str, **kwargs) -> str:
    """ Async version of generate_content

    Args:
      prompt (str): Prompt to pass to the LLM
      **kwargs: Additional LLM-specific parameters (temperature, max_tokens, etc.)

    Returns:
      str: Generated content from the LLM

    Raises:
      Exception: If the LLM request fails
    """
  
