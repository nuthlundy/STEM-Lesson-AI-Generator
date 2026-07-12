class TextComponent:
    def __init__(self, content: str):
        self.content = content
    def to_dict(self) -> dict:
        return {"type": "text", "content": self.content}
