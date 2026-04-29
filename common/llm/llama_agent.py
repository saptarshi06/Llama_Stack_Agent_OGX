# llama_agent.py
import logging
from typing import Dict, Any, Optional, Tuple
from openai import OpenAI
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# class SafetyShield:
#     """Guardrails for content filtering"""
    
#     # Hateful content patterns
#     HATEFUL_PATTERNS = {
#         'violence': ['kill', 'murder', 'attack', 'assault', 'abuse', 'torture', 'beat', 'hit', 'punch', 'kick'],
#         'crime': ['steal', 'rob', 'burglary', 'theft', 'kidnap', 'hostage', 'ransom'],
#         'self_harm': ['suicide', 'kill myself', 'hurt myself', 'self-harm', 'end my life'],
#         'weapons': ['bomb', 'gun', 'weapon', 'knife', 'pistol', 'rifle', 'shotgun'],
#         'hate_speech': ['hate', 'racist', 'sexist', 'discriminate', 'slur'],
#         'harassment': ['harass', 'bully', 'threat', 'intimidate', 'stalk']
#     }
    
#     # Combine all bad words
#     ALL_BAD_WORDS = [word for category in HATEFUL_PATTERNS.values() for word in category]
    
#     @classmethod
#     def check_message(cls, message: str) -> Tuple[bool, Optional[str], Optional[str]]:
#         """
#         Check if message contains hateful content
#         Returns: (is_violation, category, matched_word)
#         """
#         message_lower = message.lower()
        
#         for category, words in cls.HATEFUL_PATTERNS.items():
#             for word in words:
#                 if word in message_lower:
#                     logger.warning(f"⚠️ Guardrails triggered: '{word}' in category '{category}'")
#                     return True, category, word
        
#         return False, None, None
    
#     @classmethod
#     def get_safe_response(cls, category: str, word: str) -> str:
#         """Get safe response for blocked content"""
#         return f"I cannot process this request as it contains {category} content (trigger: '{word}'). Please keep the conversation respectful and appropriate."


class LlamaAgent:
    """Chatbot using OpenAI client with Llama Stack"""
    
    def __init__(
        self,
        base_url: str = "http://localhost:8321/v1",
        api_key: str = "fake",
        model_id: str = "llama3.2:3b-instruct-fp16",
        enable_guardrails: bool = True
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.model_id = model_id
        self.enable_guardrails = enable_guardrails
        self.client = None
        self.conversations: Dict[str, Dict] = {}
        self._initialize()
    
    def _initialize(self):
        """Initialize OpenAI client"""
        try:
            self.client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key
            )
            logger.info(f"Connected to Llama Stack at {self.base_url}")
            
            # Test connection
            models = self.client.models.list()
            available_models = [m.id for m in models.data]
            logger.info(f"Available models: {available_models}")
            
            # Use correct model ID if needed
            if self.model_id not in available_models:
                # Try alternative model names
                alternatives = ['ollama/llama3.2:3b', 'llama3.2:3b', 'llama3.2']
                for alt in alternatives:
                    if alt in available_models:
                        self.model_id = alt
                        logger.info(f"Using alternative model: {self.model_id}")
                        break
            
        except Exception as e:
            logger.error(f"Failed to initialize: {e}")
            raise Exception(f"Cannot connect to Llama Stack: {e}")
    
    def create_conversation(self) -> str:
        """Create new conversation"""
        conv_id = str(uuid.uuid4())
        self.conversations[conv_id] = {
            "id": conv_id,
            "messages": [],
            "created_at": self._get_timestamp()
        }
        logger.info(f"Created conversation: {conv_id}")
        return conv_id
    
    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _apply_guardrails(self, message: str, role: str = "user") -> Dict[str, Any]:
        """
        Apply guardrails to message
        Returns: { "blocked": bool, "response": str, "category": str, "word": str }
        """
        if not self.enable_guardrails:
            return {"blocked": False}
        
        #is_violation, category, matched_word = SafetyShield.check_message(message)
        
        # if is_violation:
        #     return {
        #         "blocked": True,
        #         #"response": SafetyShield.get_safe_response(category, matched_word),
        #         "category": category,
        #         "word": matched_word
        #     }
        
        return {"blocked": False}
    
    def generate_response(self, message: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate response using OpenAI client with guardrails
        """
        # Apply guardrails to input
        guardrail_result = self._apply_guardrails(message)
        
        if guardrail_result["blocked"]:
            return {
                "success": False,
                "response": guardrail_result["response"],
                "blocked": True,
                "category": guardrail_result.get("category"),
                "message": f"Blocked due to {guardrail_result.get('category')} content"
            }
        
        # Get or create conversation
        if not conversation_id:
            conversation_id = self.create_conversation()
        
        conv = self.conversations.get(conversation_id)
        if not conv:
            conversation_id = self.create_conversation()
            conv = self.conversations[conversation_id]
        
        # Add user message
        conv["messages"].append({
            "role": "user",
            "content": message,
            "timestamp": self._get_timestamp()
        })
        
        try:
            # Prepare messages for API
            messages = [
                {"role": m["role"], "content": m["content"]}
                for m in conv["messages"]
            ]
            
            # Call OpenAI-compatible API
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                stream=False
            )
            
            # Extract response - using the structure from your example
            assistant_message = response.choices[0].message.content
            
            # Apply guardrails to response
            response_guardrail = self._apply_guardrails(assistant_message, role="assistant")
            if response_guardrail["blocked"]:
                assistant_message = response_guardrail["response"]
            
            # Add assistant message
            conv["messages"].append({
                "role": "assistant",
                "content": assistant_message,
                "timestamp": self._get_timestamp()
            })
            
            # Return response with usage info
            return {
                "success": True,
                "response": assistant_message,
                "conversation_id": conversation_id,
                "blocked": False,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0
                },
                "model": response.model,
                "finish_reason": response.choices[0].finish_reason
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "success": False,
                "response": f"Error: {str(e)}",
                "blocked": False,
                "error": str(e)
            }
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict]:
        """Get conversation by ID"""
        return self.conversations.get(conversation_id)
    
    def get_all_conversations(self) -> list:
        """Get all conversations"""
        return [
            {
                "id": conv["id"],
                "created_at": conv["created_at"],
                "message_count": len(conv["messages"])
            }
            for conv in self.conversations.values()
        ]
    
    def clear_conversation(self, conversation_id: str) -> bool:
        """Clear conversation"""
        conv = self.conversations.get(conversation_id)
        if conv:
            conv["messages"] = []
            return True
        return False
    
    def health_check(self) -> Dict[str, Any]:
        """Health check"""
        try:
            models = self.client.models.list()
            return {
                "status": "healthy",
                "model": self.model_id,
                "base_url": self.base_url,
                "guardrails_enabled": self.enable_guardrails,
                "available_models": [m.id for m in models.data][:5]
            }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}