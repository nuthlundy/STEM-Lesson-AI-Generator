class EducationTheme:
    def get_styles(self) -> dict:
        return {
            "colors": {
                "primary": "#1E3A8A",
                "secondary": "#6B7280",
                "accent": "#F59E0B",
                "background": "#F9FAFB"
            },
            "typography": {
                "font_family": "Comic Sans MS, sans-serif",
                "title_size": "24pt",
                "body_size": "14pt"
            },
            "spacing": {"padding": 10},
            "borders": {"width": 2, "radius": 8},
            "shadows": {"box_shadow": "0 2px 5px rgba(0,0,0,0.05)"},
            "icons": {"type": "education"},
            "callout": {"style": "educational"},
            "header_footer": {"alignment": "center"},
            "table": {"border_color": "#E5E7EB", "header_bg": "#EFF6FF"}
        }
