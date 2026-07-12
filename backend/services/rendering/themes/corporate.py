class CorporateTheme:
    def get_styles(self) -> dict:
        return {
            "colors": {
                "primary": "#0F172A",
                "secondary": "#475569",
                "accent": "#2563EB",
                "background": "#F8FAFC"
            },
            "typography": {
                "font_family": "Helvetica, Arial, sans-serif",
                "title_size": "25pt",
                "body_size": "14pt"
            },
            "spacing": {"padding": 10},
            "borders": {"width": 1, "radius": 4},
            "shadows": {"box_shadow": "0 1px 3px rgba(0,0,0,0.1)"},
            "icons": {"type": "corporate"},
            "callout": {"style": "corporate"},
            "header_footer": {"alignment": "left"},
            "table": {"border_color": "#CBD5E1", "header_bg": "#E2E8F0"}
        }
