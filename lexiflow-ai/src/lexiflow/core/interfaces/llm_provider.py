# src/lexiflow/core/interfaces/llm_provider.py
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any


class LLMProvider(ABC):
    """Abstract interface for LLM chat completion."""
    
    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        stop_sequences: Optional[List[str]] = None,
    ) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The user/content prompt.
            system_prompt: Optional system instruction.
            temperature: Randomness (0.0 = deterministic).
            max_tokens: Max output length.
            stop_sequences: Optional list of stop strings.
            
        Returns:
            The generated text response.
        """
        pass
    
    @abstractmethod
    def generate_with_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.0,
    ) -> Dict[str, Any]:
        """
        Generate a response that is guaranteed to be valid JSON.
        (Uses function calling or JSON mode under the hood).
        """
        pass