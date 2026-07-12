class FooterComponent:
    def __init__(self, slide_num: int, total_slides: int):
        self.slide_num = slide_num
        self.total_slides = total_slides
    def to_dict(self) -> dict:
        return {"type": "footer", "slide_num": self.slide_num, "total_slides": self.total_slides}
