class BackgroundLibrary:
    @staticmethod
    def get_background(theme: str) -> str:
        backgrounds = {
            "dark": "dark_particles.png",
            "stem": "grid_background.png",
            "science": "cells_pattern.png"
        }
        return backgrounds.get(theme.lower(), "solid_flat_background.png")
