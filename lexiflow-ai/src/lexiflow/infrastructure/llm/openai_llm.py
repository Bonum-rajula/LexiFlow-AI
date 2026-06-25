# src/lexiflow/infrastructure/llm/openai_llm.py
import json
from typing import Optional, List, Dict, Any
from openai import OpenAI

from ...core.interfaces import LLMProvider
from ...core.config import settings


class OpenAILLM(LLMProvider):
    """Concrete LLM provider using OpenAI's chat completion API."""

    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        stop_sequences: Optional[List[str]] = None,
    ) -> str:
        """Generate a plain text response from the LLM."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop_sequences,
        )
        return response.choices[0].message.content

    def generate_with_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.0,
    ) -> Dict[str, Any]:
        """Generate a structured JSON response using OpenAI's JSON mode."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            response_format={"type": "json_object"},  # Forces valid JSON
        )
        return json.loads(response.choices[0].message.content)