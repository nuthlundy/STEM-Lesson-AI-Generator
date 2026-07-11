import json
from services.language_intelligence.processors.base import LanguageProcessor
from services.language_intelligence.interfaces import LinguisticMetadata, SemanticRole
from services.language_intelligence.processors.deterministic import DeterministicProcessor
from services.language_intelligence.config import lie_config
from core.logger import get_logger

logger = get_logger("stem_ai.lie.gemini")

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    genai = None
    HAS_GENAI = False

class GeminiProcessor(LanguageProcessor):
    def __init__(self):
        self.deterministic_fallback = DeterministicProcessor()
        self.api_key = lie_config.gemini_api_key
        self.model_version = lie_config.gemini_model_version
        self.is_configured = HAS_GENAI and bool(self.api_key)
        
        if self.is_configured:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_version)
    
    async def process(self, original_text: str, cleaned_text: str = "") -> LinguisticMetadata:
        """
        Uses Gemini to semantically tag the text.
        Falls back to deterministic processor if API is not configured or fails.
        """
        # Run deterministic cleanup to get base language and clean text
        det_result = await self.deterministic_fallback.process(original_text, cleaned_text)
        
        if not self.is_configured or not det_result.cleaned_text.strip():
            return det_result
            
        prompt = f"""
        Analyze the following text from an educational STEM lesson.
        Categorize its semantic role into exactly one of these categories:
        definition, theorem, example, explanation, unknown.
        Also extract a list of 0-5 key technical keywords.
        
        Text:
        {det_result.cleaned_text}
        
        Return ONLY a valid JSON object in the following format:
        {{
            "semantic_role": "definition",
            "keywords": ["keyword1", "keyword2"],
            "confidence": 0.95
        }}
        """
        
        try:
            response = await self.model.generate_content_async(prompt)
            
            # Parse JSON, cleaning possible markdown formatting
            raw_json = response.text.strip()
            if raw_json.startswith("```json"):
                raw_json = raw_json[7:]
            elif raw_json.startswith("```"):
                raw_json = raw_json[3:]
            if raw_json.endswith("```"):
                raw_json = raw_json[:-3]
                
            data = json.loads(raw_json.strip())
            
            role_str = data.get("semantic_role", "unknown").lower()
            try:
                role = SemanticRole(role_str)
            except ValueError:
                role = SemanticRole.UNKNOWN
                
            confidence = float(data.get("confidence", 0.5))
            keywords = data.get("keywords", [])
            if not isinstance(keywords, list):
                keywords = []
                
            return LinguisticMetadata(
                original_text=det_result.original_text,
                cleaned_text=det_result.cleaned_text,
                semantic_role=role,
                keywords=keywords,
                language=det_result.language,
                confidence=confidence,
                processing_provider="gemini",
                model_version=self.model_version
            )
            
        except Exception as e:
            logger.warning(f"Gemini API processing failed: {e}. Falling back to deterministic.")
            return det_result
