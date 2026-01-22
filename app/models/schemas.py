from pydantic import BaseModel, Field
from typing import Optional, List

# Input Layer Models
class ChatRequest(BaseModel):
    word: str = Field(..., description="User input text")
    context: Optional[str] = Field(None, description="Optional context")
    conversation_history: List[str] = Field(default_factory=list, description="List of previous messages")

# Output Layer Models
class ChatResponse(BaseModel):
    chat_response: str = Field(..., description="The text response from the system")
    description: str = Field(..., description="OpenAI generated explanation")
    speech_output: Optional[bytes] = Field(None, description="Binary audio data")

    # Helper to prevent binary dump in JSON logs if needed
    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        if d.get("speech_output"):
            d["speech_output"] = "<audio_bytes>"
        return d
