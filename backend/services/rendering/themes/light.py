class LightTheme:
    def get_styles(self) -> dict:
        return {
            "colors": {
                "primary": "#0F172A",
                "secondary": "#475569",
                "accent": "#0ea5e9",
                "background": "#FFFFFF"
            },
            "typography": {
                "font_family": "Segoe UI, sans-serif",
                "title_size": "24pt",
                "body_size": "14pt"
            },
            "spacing": {"padding": 10},
            "borders": {"width": 1, "radius": 4},
            "shadows": {"box_shadow": "none"},
            "icons": {"type": "light"},
            "callout": {"style": "light"},
            "header_footer": {"alignment": "center"},
            "table": {"border_color": "#CBD5E1", "header_bg": "#F8FAFC"}
        }
