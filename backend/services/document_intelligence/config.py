from pydantic_settings import BaseSettings

class DIEConfig(BaseSettings):
    # OCR Settings
    min_chars_per_page: int = 50
    ocr_lang: str = "eng"
    
    # Image Filtering
    min_image_width: int = 100
    min_image_height: int = 100
    
    # Table Detection
    min_table_cells: int = 4
    
    # Equation Detection Heuristics
    # Substrings commonly found in LaTeX/Math fonts
    math_font_identifiers: list = ["math", "symbol", "cmsy", "cmmi", "cmex", "msam", "msbm", "euler", "greek", "latex"]
    italic_ratio_threshold: float = 0.6  # If more than 60% of characters in a block are italicized, might be math
    
    # Figure/Vector Density
    # Bounding boxes with more drawings than this are rasterized as single diagrams
    vector_drawing_density_threshold: int = 15

die_config = DIEConfig()
