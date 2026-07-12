class EngineeringTheme:
    def get_styles(self) -> dict:
        return {
            "colors": {
                "primary": "#7C2D12",
                "secondary": "#EA580C",
                "accent": "#F97316",
                "background": "#FFF7ED"
            },
            "typography": {
                "font_family": "Trebuchet MS, sans-serif",
                "title_size": "25pt",
                "body_size": "14pt"
            },
            "spacing": {"padding": 10},
            "borders": {"width": 1, "radius": 4},
            "shadows": {"box_shadow": "none"},
            "icons": {"type": "engineering"},
            "callout": {"style": "industrial"},
            "header_footer": {"alignment": "center"},
            "table": {"border_color": "#FED7AA", "header_bg": "#FFEDD5"}
        }
