import json
import logging
from typing import Optional
from services.subject_intelligence.interfaces.processor import SubjectProcessor
from services.subject_intelligence.schemas import SubjectMetadata, AISubjectEnrichment
from services.subject_intelligence.processors.deterministic import DeterministicSubjectProcessor
from services.subject_intelligence.utils.merge_engine import SubjectMergeEngine
from services.subject_intelligence.utils.cache import SubjectCache
from services.subject_intelligence.constants import STEMSubject
from services.subject_intelligence.config import sie_config
from core.logger import get_logger

logger = get_logger("stem_ai.sie.gemini")

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    genai = None
    HAS_GENAI = False

class GeminiSubjectProcessor(SubjectProcessor):
    """AI Subject Processor using Gemini, integrating local SHA-256 caches and fallback blocks."""
    # Shared class-level caching layer to persist queries across pipeline workers
    _cache = SubjectCache()

    def __init__(self):
        self.deterministic_fallback = DeterministicSubjectProcessor()
        self.api_key = sie_config.gemini_api_key
        self.model_version = sie_config.gemini_model_version
        self.is_configured = HAS_GENAI and bool(self.api_key)

        if self.is_configured:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_version)

    async def process(self, text: str) -> SubjectMetadata:
        """
        Processes block text. Executes deterministic base extraction first,
        calls Gemini for semantic enrichment, and merges results.
        """
        # 1. Mandatory Deterministic Base Extraction (Primary Source of Truth)
        det_result = await self.deterministic_fallback.process(text)

        if not self.is_configured or not text.strip():
            return det_result

        # 2. Check Cache
        cached_data = self._cache.get(text)
        if cached_data:
            logger.info("Cache hit for block classification.")
            try:
                ai_enrichment = AISubjectEnrichment(**cached_data)
                return SubjectMergeEngine.merge(det_result, ai_enrichment, self.model_version)
            except Exception as e:
                logger.warning(f"Failed to load cached AI enrichment: {e}")

        # 3. Call AI Processor
        prompt = f"""
        Analyze the following text block from a STEM educational document.
        Perform semantic tagging to classify the subject, identify specific topic/sub-topic, 
        estimate difficulty, extract vocabulary, and build prerequisites.
        
        Text:
        {text}
        
        Return ONLY a valid JSON object in the following format:
        {{
            "subject": "physics",
            "subject_confidence": 0.95,
            "topic": "Thermodynamics",
            "topic_confidence": 0.90,
            "difficulty": "medium",
            "difficulty_confidence": 0.85,
            "vocabulary": ["entropy", "heat"],
            "vocabulary_confidence": 0.90,
            "prerequisites": ["classical mechanics"],
            "prerequisites_confidence": 0.80
        }}
        """

        try:
            response = await self.model.generate_content_async(prompt)
            raw_json = response.text.strip()
            
            if raw_json.startswith("```json"):
                raw_json = raw_json[7:]
            elif raw_json.startswith("```"):
                raw_json = raw_json[3:]
            if raw_json.endswith("```"):
                raw_json = raw_json[:-3]

            data = json.loads(raw_json.strip())

            # Map subject string to STEMSubject enum
            sub_str = data.get("subject", "").lower()
            try:
                subject_enum = STEMSubject(sub_str)
            except ValueError:
                subject_enum = STEMSubject.OTHER

            ai_enrichment = AISubjectEnrichment(
                subject=subject_enum,
                subject_confidence=data.get("subject_confidence"),
                topic=data.get("topic"),
                topic_confidence=data.get("topic_confidence"),
                difficulty=data.get("difficulty"),
                difficulty_confidence=data.get("difficulty_confidence"),
                vocabulary=data.get("vocabulary", []),
                vocabulary_confidence=data.get("vocabulary_confidence"),
                prerequisites=data.get("prerequisites", []),
                prerequisites_confidence=data.get("prerequisites_confidence")
            )

            # Store raw serializable dict to cache
            self._cache.set(text, ai_enrichment.model_dump())

            # 4. Merge Results (Ensuring Deterministic Primacy)
            return SubjectMergeEngine.merge(det_result, ai_enrichment, self.model_version)

        except Exception as e:
            logger.warning(f"Gemini Subject enrichment failed: {e}. Falling back to deterministic.")
            return det_result
