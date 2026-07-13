import unittest
from services.presentation.schemas import (
    PresentationSessionModel, PresentationAIMetadata, SpeakingSuggestion, 
    AudienceQuestion, DiscussionPrompt, TeachingTip, TransitionSuggestion, ConfidenceScore
)
from services.presentation.utils.merge_engine import PresentationAIMergeEngine

class TestPresentationAIMergeEngine(unittest.TestCase):
    def setUp(self):
        self.session = PresentationSessionModel(
            session_id="session-1",
            presentation_path="lesson.pptx",
            duration_seconds=3600,
            slides=[]
        )

    def test_merge_union(self):
        ai_data = PresentationAIMetadata(
            speaking_suggestions=[
                SpeakingSuggestion(
                    slide_index=0,
                    suggestion="Intro tip",
                    confidence=ConfidenceScore(score=0.9, method="test")
                )
            ]
        )
        merged = PresentationAIMergeEngine.merge(self.session, ai_data)
        self.assertEqual(len(merged.ai_metadata.speaking_suggestions), 1)
        
        merged2 = PresentationAIMergeEngine.merge(merged, ai_data)
        self.assertEqual(len(merged2.ai_metadata.speaking_suggestions), 1)

    def test_merge_audience_questions(self):
        ai_data = PresentationAIMetadata(
            audience_questions=[
                AudienceQuestion(
                    slide_index=1,
                    question="What is gravity?",
                    suggested_answer="A force",
                    confidence=ConfidenceScore(score=0.8, method="test")
                )
            ]
        )
        merged = PresentationAIMergeEngine.merge(self.session, ai_data)
        self.assertEqual(len(merged.ai_metadata.audience_questions), 1)

    def test_merge_discussion_prompts(self):
        ai_data = PresentationAIMetadata(
            discussion_prompts=[
                DiscussionPrompt(
                    slide_index=2,
                    prompt="Discuss friction.",
                    confidence=ConfidenceScore(score=0.85, method="test")
                )
            ]
        )
        merged = PresentationAIMergeEngine.merge(self.session, ai_data)
        self.assertEqual(len(merged.ai_metadata.discussion_prompts), 1)

    def test_merge_teaching_tips(self):
        ai_data = PresentationAIMetadata(
            teaching_tips=[
                TeachingTip(
                    slide_index=3,
                    tip="Keep it interactive.",
                    confidence=ConfidenceScore(score=0.95, method="test")
                )
            ]
        )
        merged = PresentationAIMergeEngine.merge(self.session, ai_data)
        self.assertEqual(len(merged.ai_metadata.teaching_tips), 1)

    def test_merge_transition_suggestions(self):
        ai_data = PresentationAIMetadata(
            transition_suggestions=[
                TransitionSuggestion(
                    from_slide=0,
                    to_slide=1,
                    suggestion="Move smoothly",
                    confidence=ConfidenceScore(score=0.75, method="test")
                )
            ]
        )
        merged = PresentationAIMergeEngine.merge(self.session, ai_data)
        self.assertEqual(len(merged.ai_metadata.transition_suggestions), 1)

if __name__ == "__main__":
    unittest.main()
