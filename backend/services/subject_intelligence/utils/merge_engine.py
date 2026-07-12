from typing import Optional
from services.subject_intelligence.schemas import SubjectMetadata, AISubjectEnrichment
from services.subject_intelligence.constants import STEMSubject

class SubjectMergeEngine:
    """Engine responsible for merging deterministic outcomes with AI-derived enrichments."""
    @staticmethod
    def merge(det_meta: SubjectMetadata, ai_enrichment: Optional[AISubjectEnrichment], model_version: Optional[str] = None) -> SubjectMetadata:
        """
        Merges AI predictions into the base deterministic metadata.
        Rules:
        - AI must never overwrite non-empty deterministic core fields (subject).
        - Vocabulary lists and prerequisites are combined (union).
        - Optional fields (topic, difficulty) are filled by AI only if deterministic is empty or placeholder.
        """
        if not ai_enrichment:
            return det_meta

        # Subject: Deterministic primacy (do not overwrite)
        final_subject = det_meta.subject

        # Topic: If deterministic detected a general topic or nothing, we allow AI to specialize it
        final_topic = det_meta.topic
        if not final_topic or "General" in final_topic:
            final_topic = ai_enrichment.topic or final_topic

        # Difficulty: Fill if empty or fallback
        final_difficulty = det_meta.difficulty or ai_enrichment.difficulty

        # Vocabulary: Combined union of unique terms
        vocab_set = set(det_meta.vocabulary)
        if ai_enrichment.vocabulary:
            vocab_set.update(ai_enrichment.vocabulary)
        final_vocabulary = sorted(list(vocab_set))

        # Prerequisites: Combined union
        prereq_set = set(det_meta.prerequisites)
        if ai_enrichment.prerequisites:
            prereq_set.update(ai_enrichment.prerequisites)
        final_prerequisites = sorted(list(prereq_set))

        # Overall confidence estimation
        # We can average the confidence scores or use a baseline
        ai_conf = ai_enrichment.subject_confidence or 0.5
        overall_confidence = (det_meta.confidence + ai_conf) / 2.0 if det_meta.confidence is not None else ai_conf

        return SubjectMetadata(
            subject=final_subject,
            topic=final_topic,
            difficulty=final_difficulty,
            vocabulary=final_vocabulary,
            confidence=round(overall_confidence, 2),
            prerequisites=final_prerequisites,
            extracted_formulas=det_meta.extracted_formulas,
            validated_formulas=det_meta.validated_formulas,
            ai_enrichment=ai_enrichment,
            processing_provider="gemini",
            model_version=model_version
        )
