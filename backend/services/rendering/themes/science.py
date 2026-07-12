class ScienceTheme:
    def get_styles(self) -> dict:
        return {
            "colors": {
                "primary": "#065F46",
                "secondary": "#047857",
                "accent": "#34D399",
                "background": "#ECFDF5"
            },
            "typography": {
                "font_family": "Calibri, sans-serif",
                "title_size": "25pt",
                "body_size": "14pt"
            },
            "spacing": {"padding": 10},
            "borders": {"width": 1, "radius": 4},
            "shadows": {"box_shadow": "none"},
            "icons": {"type": "science"},
            "callout": {"style": "scientific"},
            "header_footer": {"alignment": "left"},
            "table": {"border_color": "#A7F3D0", "header_bg": "#D1FAE5"}
        }
