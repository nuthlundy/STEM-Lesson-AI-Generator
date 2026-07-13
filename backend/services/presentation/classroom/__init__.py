from services.presentation.classroom.questions import ClassroomQuestions
from services.presentation.classroom.polls import ClassroomPolls
from services.presentation.classroom.activities import ClassroomActivities
from services.presentation.classroom.discussions import ClassroomDiscussions
from services.presentation.classroom.feedback import ClassroomFeedback
from services.presentation.classroom.responses import StudentResponses

class ClassroomInteractionManager:
    def __init__(self) -> None:
        self.questions = ClassroomQuestions()
        self.polls = ClassroomPolls()
        self.activities = ClassroomActivities()
        self.discussions = ClassroomDiscussions()
        self.feedback = ClassroomFeedback()
        self.responses = StudentResponses()
