class CodeComponent:
    def __init__(self, code: str, language: str = "python"):
        self.code = code
        self.language = language
    def to_dict(self) -> dict:
        return {"type": "code", "code": self.code, "language": self.language}
