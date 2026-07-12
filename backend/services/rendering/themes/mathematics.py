class MathematicsTheme:
    def get_styles(self) -> dict:
        return {
            "colors": {
                "primary": "#1E293B",
                "secondary": "#475569",
                "accent": "#4F46E5",
                "background": "#F5F3FF"
            },
            "typography": {
                "font_family": "Georgia, serif",
                "title_size": "26pt",
                "body_size": "15pt"
            },
            "spacing": {"padding": 12},
            "borders": {"width": 1, "radius": 4},
            "shadows": {"box_shadow": "none"},
            "icons": {"type": "math"},
            "callout": {"style": "mathematical"},
            "header_footer": {"alignment": "right"},
            "table": {"border_color": "#DDD6FE", "header_bg": "#EDE9FE"}
        }
