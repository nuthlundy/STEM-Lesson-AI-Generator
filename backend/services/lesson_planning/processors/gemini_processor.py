import json
import hashlib
from typing import Dict, Any, Optional
from services.lesson_planning.interfaces.planner import LessonPlanner
from services.lesson_planning.schemas import LessonPlan
from services.lesson_planning.processors.deterministic import DeterministicLessonPlanner
from services.lesson_planning.processors.merge_engine import AIMergeEngine
from services.lesson_planning.utils.cache import LessonCache
from services.lesson_planning.config import lpe_config
from services.lesson_planning.prompts.repository import LESSON_ENRICHMENT_PROMPT
from core.logger import get_logger

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    genai = None
    HAS_GENAI = False

logger = get_logger("stem_ai.lpe.gemini_processor")

class GeminiLessonPlanner(LessonPlanner):
    """AI-enriched Lesson Planner using Gemini with a cache layer and deterministic fallback."""
    _cache = LessonCache()
    
    def __init__(self):
        self.deterministic_planner = DeterministicLessonPlanner()
        self.is_configured = HAS_GENAI and bool(lpe_config.gemini_api_key)
        if self.is_configured:
            genai.configure(api_key=lpe_config.gemini_api_key)
            
    async def plan(self, subject: str, context_data: Dict[str, Any]) -> LessonPlan:
        det_plan = await self.deterministic_planner.plan(subject, context_data)
        
        if not self.is_configured:
            logger.warning("Gemini API key not configured. Falling back directly to deterministic baseline.")
            return det_plan
            
        cache_key = f"{subject}:{det_plan.timeline}"
        
        cached = self._cache.get(cache_key)
        if cached:
            logger.info("Cache hit for lesson plan enrichment.")
            return AIMergeEngine.merge(det_plan, cached)
            
        try:
            prompt = LESSON_ENRICHMENT_PROMPT.format(
                subject=subject,
                sections=", ".join(det_plan.timeline),
                objectives=str(det_plan.objective_mapping)
            )
            
            model = genai.GenerativeModel(lpe_config.gemini_model_version)
            
            import asyncio
            loop = asyncio.get_event_loop()
            
            def make_call():
                response = model.generate_content(
                    prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                return response.text
                
            response_text = await loop.run_in_executor(None, make_call)
            ai_data = json.loads(response_text)
            
            self._cache.set(cache_key, ai_data)
            return AIMergeEngine.merge(det_plan, ai_data)
            
        except Exception as e:
            logger.error(f"Gemini API enrichment failed: {e}. Falling back to deterministic plan.")
            return det_plan
