class PresentationPromptRepository:
    SPEAKING_SUGGESTION_TEMPLATE = (
        "Generate slide presentation delivery speaking points and cues for slide: {slide_title}."
    )
    AUDIENCE_QUESTION_TEMPLATE = (
        "Formulate active recall questions and key answers for the topic: {slide_title}."
    )
    TEACHING_TIP_TEMPLATE = (
        "Provide classroom management and visual pedagogy guidelines for slide: {slide_title}."
    )
