class DarkTheme:
    def get_styles(self) -> dict:
        return {
            "colors": {
                "primary": "#F8FAFC",
                "secondary": "#94A3B8",
                "accent": "#F59E0B",
                "background": "#0F172A"
            },
            "typography": {
                "font_family": "Segoe UI, sans-serif",
                "title_size": "24pt",
                "body_size": "14pt"
            },
            "spacing": {"padding": 10},
            "borders": {"width": 1, "radius": 4},
            "shadows": {"box_shadow": "none"},
            "icons": {"type": "dark"},
            "callout": {"style": "dark"},
            "header_footer": {"alignment": "center"},
            "table": {"border_color": "#334155", "header_bg": "#1E293B"}
        }
