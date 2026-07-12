class ModernTheme:
    def get_styles(self) -> dict:
        return {
            "colors": {
                "primary": "#1E293B",
                "secondary": "#64748B",
                "accent": "#0ea5e9",
                "background": "#f8fafc"
            },
            "typography": {
                "font_family": "Inter, sans-serif",
                "title_size": "26pt",
                "body_size": "15pt"
            },
            "spacing": {"padding": 12},
            "borders": {"width": 1, "radius": 8},
            "shadows": {"box_shadow": "0 4px 6px -1px rgb(0 0 0 / 0.1)"},
            "icons": {"type": "modern"},
            "callout": {"style": "modern"},
            "header_footer": {"alignment": "center"},
            "table": {"border_color": "#e2e8f0", "header_bg": "#f1f5f9"}
        }
