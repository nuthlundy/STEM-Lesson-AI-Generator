from services.presentation.schemas import PresentationSessionModel, PresentationAIMetadata

class PresentationAIMergeEngine:
    @staticmethod
    def merge(session: PresentationSessionModel, ai_data: PresentationAIMetadata) -> PresentationSessionModel:
        if not session.ai_metadata:
            session.ai_metadata = PresentationAIMetadata()
            
        def merge_list(det_list, ai_list):
            merged = list(det_list)
            existing = set()
            for item in merged:
                existing.add(item.model_dump_json())
            for item in ai_list:
                dump = item.model_dump_json()
                if dump not in existing:
                    merged.append(item)
                    existing.add(dump)
            return merged

        session.ai_metadata.speaking_suggestions = merge_list(
            session.ai_metadata.speaking_suggestions, ai_data.speaking_suggestions
        )
        session.ai_metadata.audience_questions = merge_list(
            session.ai_metadata.audience_questions, ai_data.audience_questions
        )
        session.ai_metadata.discussion_prompts = merge_list(
            session.ai_metadata.discussion_prompts, ai_data.discussion_prompts
        )
        session.ai_metadata.teaching_tips = merge_list(
            session.ai_metadata.teaching_tips, ai_data.teaching_tips
        )
        session.ai_metadata.transition_suggestions = merge_list(
            session.ai_metadata.transition_suggestions, ai_data.transition_suggestions
        )
        
        return session
