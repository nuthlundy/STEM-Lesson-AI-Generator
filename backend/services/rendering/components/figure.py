class FigureComponent:
    def __init__(self, url: str, caption: str = ""):
        self.url = url
        self.caption = caption
    def to_dict(self) -> dict:
        return {"type": "figure", "url": self.url, "caption": self.caption}
