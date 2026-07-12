class StemTheme:
    def get_styles(self) -> dict:
        return {
            "colors": {
                "primary": "#0A2540",
                "secondary": "#639FAB",
                "accent": "#00D4B2",
                "background": "#F4F6F8"
            },
            "typography": {
                "font_family": "Segoe UI, sans-serif",
                "title_size": "26pt",
                "body_size": "15pt"
            },
            "spacing": {"padding": 12},
            "borders": {"width": 1, "radius": 6},
            "shadows": {"box_shadow": "0 2px 4px rgba(0,0,0,0.1)"},
            "icons": {"type": "stem"},
            "callout": {"style": "vibrant"},
            "header_footer": {"alignment": "center"},
            "table": {"border_color": "#D3D3D3", "header_bg": "#E6F0FA"}
        }
