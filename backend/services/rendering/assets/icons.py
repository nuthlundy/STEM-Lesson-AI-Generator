class IconLibrary:
    @staticmethod
    def lookup_icon(topic: str) -> str:
        mapping = {
            "math": "calculator-icon",
            "physics": "atom-icon",
            "chemistry": "beaker-icon",
            "biology": "dna-icon",
            "computer": "terminal-icon"
        }
        return mapping.get(topic.lower(), "question-icon")
