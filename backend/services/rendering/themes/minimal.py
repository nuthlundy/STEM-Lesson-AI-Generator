class MinimalTheme:
    def get_styles(self) -> dict:
        return {
            "colors": {
                "primary": "#111111",
                "secondary": "#888888",
                "accent": "#000000",
                "background": "#FDFDFD"
            },
            "typography": {
                "font_family": "Courier New, monospace",
                "title_size": "22pt",
                "body_size": "13pt"
            },
            "spacing": {"padding": 8},
            "borders": {"width": 1, "radius": 2},
            "shadows": {"box_shadow": "none"},
            "icons": {"type": "minimal"},
            "callout": {"style": "clean"},
            "header_footer": {"alignment": "right"},
            "table": {"border_color": "#888888", "header_bg": "#FFFFFF"}
        }
