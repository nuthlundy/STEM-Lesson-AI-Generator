from enum import Enum

class STEMSubject(str, Enum):
    MATH = "math"
    PHYSICS = "physics"
    CHEMISTRY = "chemistry"
    COMPUTER_SCIENCE = "computer_science"
    OTHER = "other"

ENGINE_NAME = "Subject Intelligence Engine"
ENGINE_VERSION = "1.0.0"
SCHEMA_VERSION = "1.0.0"
