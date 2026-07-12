class TechnologyTheme:
    def get_styles(self) -> dict:
        return {
            "colors": {
                "primary": "#0F172A",
                "secondary": "#38BDF8",
                "accent": "#00F5FF",
                "background": "#020617"
            },
            "typography": {
                "font_family": "Consolas, monospace",
                "title_size": "24pt",
                "body_size": "14pt"
            },
            "spacing": {"padding": 10},
            "borders": {"width": 1, "radius": 4},
            "shadows": {"box_shadow": "none"},
            "icons": {"type": "tech"},
            "callout": {"style": "tech_style"},
            "header_footer": {"alignment": "center"},
            "table": {"border_color": "#0F172A", "header_bg": "#1E293B"}
        }
