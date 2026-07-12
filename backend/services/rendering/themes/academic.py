class AcademicTheme:
    def get_styles(self) -> dict:
        return {
            "colors": {
                "primary": "#002060",
                "secondary": "#595959",
                "accent": "#C00000",
                "background": "#F2F2F2"
            },
            "typography": {
                "font_family": "Times New Roman, serif",
                "title_size": "26pt",
                "body_size": "15pt"
            },
            "spacing": {"padding": 12},
            "borders": {"width": 2, "radius": 0},
            "shadows": {"box_shadow": "none"},
            "icons": {"type": "formal"},
            "callout": {"style": "bordered"},
            "header_footer": {"alignment": "left"},
            "table": {"border_color": "#000000", "header_bg": "#EAEAEA"}
        }
