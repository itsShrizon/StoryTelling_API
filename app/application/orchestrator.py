from app.models.schemas import ChatRequest, ChatResponse
from app.infrastructure.llm_client import LLMClient
from app.infrastructure.tts_client import TTSClient
from app.domain.prompt_builder import PromptBuilder
from app.domain.conversation import ConversationManager
from app.domain.grammar.grammar_service import GrammarService
from app.guardrails.guardrails import Guardrails
from app.output.response_formatter import ResponseFormatter

class Orchestrator:
    def __init__(self):
        # Initialize all services
        self.llm_client = LLMClient()
        self.tts_client = TTSClient()
        self.prompt_builder = PromptBuilder()
        self.conversation_manager = ConversationManager()
        self.grammar_service = GrammarService()
        self.guardrails = Guardrails()
        self.response_formatter = ResponseFormatter()

    def process_request(self, request: ChatRequest) -> ChatResponse:
        # 1. Orchestrate Flow
        # Construct System Prompt
        system_prompt = self.prompt_builder.build_system_prompt(request.context)
        
        # Format History
        formatted_history = self.prompt_builder.format_conversation_history(request.conversation_history)
        
        # Combine into complete user message context
        full_user_message = f"{formatted_history}\nUser: {request.word}"
        
        # 2. Call LLM
        raw_response = self.llm_client.generate_chat_response(system_prompt, full_user_message)
        
        # 3. Apply Grammar Correction (Optional/Future)
        corrected_response = self.grammar_service.correct_grammar(raw_response)
        
        # 4. Apply Guardrails
        safe_response = self.guardrails.validate_response(corrected_response)
        
        # 5. Generate Metadata (Description)
        description = self.llm_client.generate_description(safe_response)
        
        # 6. Generate Speech
        audio_bytes = self.tts_client.text_to_speech(safe_response)
        
        # 7. Format Output
        return self.response_formatter.format_response(safe_response, description, audio_bytes)
