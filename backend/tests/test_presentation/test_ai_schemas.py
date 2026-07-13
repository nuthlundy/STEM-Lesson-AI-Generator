import unittest
from services.presentation.schemas import (
    ConfidenceScore, SpeakingSuggestion, AudienceQuestion,
    DiscussionPrompt, TeachingTip, TransitionSuggestion,
    PresentationAIMetadata, PresentationSessionModel
)

class TestPresentationAISchemas(unittest.TestCase):
    def test_schema_instantiation_and_serialization(self):
        score = ConfidenceScore(score=0.85, method="manual")
        self.assertEqual(score.score, 0.85)
        
        suggestion = SpeakingSuggestion(slide_index=0, suggestion="Focus on definitions", confidence=score)
        self.assertEqual(suggestion.confidence.score, 0.85)
        
        meta = PresentationAIMetadata(
            speaking_suggestions=[suggestion]
        )
        self.assertEqual(len(meta.speaking_suggestions), 1)
        
        session = PresentationSessionModel(
            session_id="test",
            presentation_path="test.pptx",
            duration_seconds=1200,
            ai_metadata=meta
        )
        self.assertEqual(session.ai_metadata.speaking_suggestions[0].suggestion, "Focus on definitions")
        
        serialized = session.model_dump_json()
        deserialized = PresentationSessionModel.model_validate_json(serialized)
        self.assertEqual(deserialized.ai_metadata.speaking_suggestions[0].suggestion, "Focus on definitions")

    def test_confidence_score_validation(self):
        score = ConfidenceScore(score=0.5, method="gemini")
        self.assertEqual(score.score, 0.5)
        
    def test_audience_question_schema(self):
        q = AudienceQuestion(
            slide_index=1,
            question="What is 2+2?",
            suggested_answer="4",
            confidence=ConfidenceScore(score=1.0)
        )
        self.assertEqual(q.question, "What is 2+2?")

    def test_discussion_prompt_schema(self):
        p = DiscussionPrompt(slide_index=2, prompt="Talk about gravity.")
        self.assertEqual(p.prompt, "Talk about gravity.")

    def test_teaching_tip_schema(self):
        t = TeachingTip(slide_index=3, tip="Write on the board.")
        self.assertEqual(t.tip, "Write on the board.")

    def test_transition_suggestion_schema(self):
        tr = TransitionSuggestion(from_slide=0, to_slide=1, suggestion="Use a visual analogy.")
        self.assertEqual(tr.suggestion, "Use a visual analogy.")

if __name__ == "__main__":
    unittest.main()
