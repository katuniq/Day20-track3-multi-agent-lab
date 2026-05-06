"""LLM client abstraction.

Production note: agents should depend on this interface instead of importing an SDK directly.
"""

from dataclasses import dataclass
import os
from openai import OpenAI

from multi_agent_research_lab.core.errors import StudentTodoError


@dataclass(frozen=True)
class LLMResponse:
    content: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    cost_usd: float | None = None


class LLMClient:
    """Provider-agnostic LLM client skeleton."""

    def __init__(self, model: str = "gpt-4o-mini", api_key: str | None = None):
        api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
        self.client = OpenAI(api_key=api_key)

    def complete(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Return a model completion."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,
        )
        
        content = response.choices[0].message.content or ""
        input_tokens = response.usage.prompt_tokens if response.usage else 0
        output_tokens = response.usage.completion_tokens if response.usage else 0
        
        return LLMResponse(
            content=content,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=None, # Optional cost calculation
        )
