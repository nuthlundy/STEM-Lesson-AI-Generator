class NavigationJump:
    def __init__(self, max_slides: int = 100) -> None:
        self.max_slides = max_slides

    def jump_to_slide(self, slide_index: int) -> int:
        if 0 <= slide_index < self.max_slides:
            return slide_index
        raise ValueError(f"Invalid slide index: {slide_index}")
