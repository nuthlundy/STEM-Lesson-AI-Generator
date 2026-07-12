from services.rendering.themes.default import DefaultTheme
from services.rendering.themes.academic import AcademicTheme
from services.rendering.themes.minimal import MinimalTheme
from services.rendering.themes.stem import StemTheme
from services.rendering.themes.corporate import CorporateTheme
from services.rendering.themes.modern import ModernTheme
from services.rendering.themes.dark import DarkTheme
from services.rendering.themes.light import LightTheme
from services.rendering.themes.education import EducationTheme
from services.rendering.themes.science import ScienceTheme
from services.rendering.themes.mathematics import MathematicsTheme
from services.rendering.themes.technology import TechnologyTheme
from services.rendering.themes.engineering import EngineeringTheme

THEMES = {
    "default": DefaultTheme,
    "academic": AcademicTheme,
    "minimal": MinimalTheme,
    "stem": StemTheme,
    "corporate": CorporateTheme,
    "modern": ModernTheme,
    "dark": DarkTheme,
    "light": LightTheme,
    "education": EducationTheme,
    "science": ScienceTheme,
    "mathematics": MathematicsTheme,
    "technology": TechnologyTheme,
    "engineering": EngineeringTheme
}

def get_theme(name: str):
    return THEMES.get(name.lower(), DefaultTheme)()
