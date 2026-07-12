class TitleComponent:
    def __init__(self, text: str):
        self.text = text
    def to_dict(self) -> dict:
        return {"type": "title", "text": self.text}
