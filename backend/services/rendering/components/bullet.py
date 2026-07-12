class BulletComponent:
    def __init__(self, items: list):
        self.items = items
    def to_dict(self) -> dict:
        return {"type": "bullet", "items": self.items}
