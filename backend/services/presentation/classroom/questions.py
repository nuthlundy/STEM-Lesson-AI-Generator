from typing import Dict, Any, List

class ClassroomQuestions:
    def __init__(self) -> None:
        self._questions: Dict[str, Dict[str, Any]] = {}

    def ask(self, question_id: str, text: str, category: str = "conceptual") -> None:
        self._questions[question_id] = {
            "text": text,
            "category": category,
            "answers": [],
            "status": "asked"
        }

    def answer(self, question_id: str, student_id: str, answer_text: str) -> None:
        if question_id in self._questions:
            self._questions[question_id]["answers"].append({
                "student_id": student_id,
                "answer": answer_text
            })

    def get_question(self, question_id: str) -> Dict[str, Any]:
        return self._questions.get(question_id, {})
