class DefaultTheme:
    def get_styles(self) -> dict:
        return {
            "colors": {
                "primary": "#1A1A1A",
                "secondary": "#7F7F7F",
                "accent": "#0066CC",
                "background": "#FFFFFF"
            },
            "typography": {
                "font_family": "Arial, sans-serif",
                "title_size": "24pt",
                "body_size": "14pt"
            },
            "spacing": {"padding": 10},
            "borders": {"width": 1, "radius": 4},
            "shadows": {"box_shadow": "none"},
            "icons": {"type": "standard"},
            "callout": {"style": "simple"},
            "header_footer": {"alignment": "center"},
            "table": {"border_color": "#CCCCCC", "header_bg": "#F0F0F0"}
        }
