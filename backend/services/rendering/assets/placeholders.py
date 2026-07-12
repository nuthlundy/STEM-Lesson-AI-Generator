class PlaceholderGenerator:
    @staticmethod
    def generate_placeholder(width: int = 400, height: int = 300, label: str = "Image Placeholder") -> str:
        return f"https://placehold.co/{width}x{height}?text={label.replace(' ', '+')}"
