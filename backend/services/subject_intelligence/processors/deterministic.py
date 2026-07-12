import re
from typing import List, Dict, Any
from services.subject_intelligence.interfaces.processor import SubjectProcessor
from services.subject_intelligence.schemas import SubjectMetadata
from services.subject_intelligence.constants import STEMSubject
from services.subject_intelligence.config import sie_config
from services.subject_intelligence.validators.formulas import validate_formula_syntax

class DeterministicSubjectProcessor(SubjectProcessor):
    """Deterministic processing layer implementing layout and keyword heuristics."""
    def __init__(self):
        # Keywords for Subject Detection
        self.subject_keywords = {
            STEMSubject.MATH: {
                "equation", "theorem", "proof", "matrix", "integral", "derivative", 
                "function", "algebra", "calculus", "geometry", "arithmetic", "sum", 
                "fraction", "vector", "polynomial", "limit"
            },
            STEMSubject.PHYSICS: {
                "force", "velocity", "acceleration", "gravity", "mass", "energy", 
                "momentum", "quantum", "relativity", "thermodynamics", "optics", 
                "friction", "wave", "speed", "joule", "newton"
            },
            STEMSubject.CHEMISTRY: {
                "reaction", "molecule", "atom", "element", "compound", "bond", 
                "valence", "acid", "base", "solution", "organic", "catalyst", 
                "covalent", "ionic", "periodic", "gas", "liquid", "solid", "stoichiometry"
            },
            STEMSubject.COMPUTER_SCIENCE: {
                "algorithm", "programming", "code", "loop", "variable", "class", 
                "object", "database", "array", "binary", "recursion", "list", 
                "stack", "queue", "string", "integer", "boolean", "compile"
            }
        }
        
        # Vocabulary lists per subject
        self.vocabulary_registry = {
            STEMSubject.MATH: [
                "derivative", "integral", "matrix", "vector", "polynomial", "function", 
                "equation", "theorem", "limit", "proof", "calculus", "algebra", "geometry"
            ],
            STEMSubject.PHYSICS: [
                "gravity", "force", "momentum", "velocity", "acceleration", "entropy", 
                "energy", "mass", "friction", "relativity", "optics", "thermodynamics"
            ],
            STEMSubject.CHEMISTRY: [
                "reaction", "molecule", "atom", "element", "compound", "bond", "valence", 
                "acid", "base", "covalent", "ionic", "stoichiometry", "isotope", "catalyst"
            ],
            STEMSubject.COMPUTER_SCIENCE: [
                "recursion", "complexity", "polymorphism", "encapsulation", "inheritance", 
                "stack", "queue", "algorithm", "loop", "variable", "class", "object", 
                "database", "array", "binary"
            ]
        }

    def _detect_subject(self, text_lower: str) -> STEMSubject:
        scores = {subj: 0 for subj in self.subject_keywords}
        
        words = re.findall(r'\b[a-z]+\b', text_lower)
        for word in words:
            for subj, kw_set in self.subject_keywords.items():
                if word in kw_set:
                    scores[subj] += 1
                    
        max_score = max(scores.values())
        if max_score == 0:
            try:
                return STEMSubject(sie_config.default_subject)
            except ValueError:
                return STEMSubject.MATH
                
        best_subjects = [subj for subj, score in scores.items() if score == max_score]
        return best_subjects[0]

    def _detect_topic(self, text_lower: str, subject: STEMSubject) -> str:
        if subject == STEMSubject.PHYSICS:
            if any(w in text_lower for w in ["force", "velocity", "acceleration", "gravity", "mass", "momentum", "friction", "speed"]):
                return "Mechanics"
            if any(w in text_lower for w in ["thermodynamics", "heat", "temperature", "entropy"]):
                return "Thermodynamics"
            if any(w in text_lower for w in ["quantum", "relativity", "wave", "optics"]):
                return "Quantum & Modern Physics"
            return "General Physics"
            
        elif subject == STEMSubject.MATH:
            if any(w in text_lower for w in ["integral", "derivative", "calculus", "limit"]):
                return "Calculus"
            if any(w in text_lower for w in ["matrix", "vector"]):
                return "Linear Algebra"
            if any(w in text_lower for w in ["geometry", "angle", "triangle", "circle"]):
                return "Geometry"
            if any(w in text_lower for w in ["equation", "algebra", "variable"]):
                return "Algebra"
            return "General Mathematics"
            
        elif subject == STEMSubject.CHEMISTRY:
            if any(w in text_lower for w in ["organic", "carbon", "alkane", "polymer"]):
                return "Organic Chemistry"
            if any(w in text_lower for w in ["inorganic", "metal", "ionic", "acid", "base"]):
                return "Inorganic Chemistry"
            return "General Chemistry"
            
        elif subject == STEMSubject.COMPUTER_SCIENCE:
            if any(w in text_lower for w in ["algorithm", "array", "binary", "recursion", "list", "stack", "queue"]):
                return "Algorithms & Data Structures"
            if any(w in text_lower for w in ["programming", "code", "class", "object"]):
                return "Software Engineering"
            return "General Computer Science"
            
        return "General STEM"

    def _extract_vocabulary(self, text_lower: str, subject: STEMSubject) -> List[str]:
        registry = self.vocabulary_registry.get(subject, [])
        found = []
        for term in registry:
            if re.search(r'\b' + re.escape(term) + r'\b', text_lower):
                found.append(term)
        return found

    def _extract_formulas(self, text: str) -> List[str]:
        formulas = []
        
        # LaTeX syntax checks
        inline_matches = re.findall(r'\$(.+?)\$', text)
        formulas.extend(inline_matches)
        
        block_matches = re.findall(r'\$\$(.+?)\$\$', text)
        formulas.extend(block_matches)
        
        bracket_matches = re.findall(r'\\\[(.+?)\\\]', text)
        formulas.extend(bracket_matches)
        
        paren_matches = re.findall(r'\\\((.+?)\\\)', text)
        formulas.extend(paren_matches)
        
        # Simple math symbols/assignments
        equation_pattern = re.findall(r'\b[A-Za-z]\s*=\s*[A-Za-z0-9\s+\-*^/()]+', text)
        for eq in equation_pattern:
            if len(eq.strip()) > 3 and not eq.strip().endswith("="):
                formulas.append(eq.strip())
                
        return list(set(formulas))

    def _estimate_difficulty(self, text: str, formulas: List[str], vocabulary: List[str]) -> str:
        score = 0
        
        sentences = [s for s in re.split(r'[.!?]', text) if s.strip()]
        if sentences:
            total_words = sum(len(s.split()) for s in sentences)
            avg_len = total_words / len(sentences)
            if avg_len > 20:
                score += 1
                
        score += len(formulas) * 2
        score += len(vocabulary)
        
        if score <= 2:
            return "easy"
        elif score <= 5:
            return "medium"
        else:
            return "hard"

    def _build_relationships(self, text_lower: str) -> List[str]:
        prereqs = []
        if "quantum" in text_lower or "relativity" in text_lower:
            prereqs.append("classical mechanics")
        if any(w in text_lower for w in ["calculus", "derivative", "integral"]):
            prereqs.extend(["algebra", "functions"])
        if "stoichiometry" in text_lower:
            prereqs.extend(["atomic mass", "periodic table"])
        if "recursion" in text_lower:
            prereqs.extend(["functions", "conditionals"])
        if "inheritance" in text_lower or "polymorphism" in text_lower:
            prereqs.append("classes & objects")
            
        return list(set(prereqs))

    async def process(self, text: str) -> SubjectMetadata:
        text_lower = text.lower()
        
        subject = self._detect_subject(text_lower)
        topic = self._detect_topic(text_lower, subject)
        vocabulary = self._extract_vocabulary(text_lower, subject)
        formulas = self._extract_formulas(text)
        difficulty = self._estimate_difficulty(text, formulas, vocabulary)
        prerequisites = self._build_relationships(text_lower)
        
        validated = []
        for formula in formulas:
            report = validate_formula_syntax(formula)
            validated.append({
                "formula": formula,
                "valid": report["valid"],
                "errors": report["errors"],
                "details": report["details"]
            })
            
        return SubjectMetadata(
            subject=subject,
            topic=topic,
            difficulty=difficulty,
            vocabulary=vocabulary,
            confidence=1.0,
            prerequisites=prerequisites,
            extracted_formulas=formulas,
            validated_formulas=validated,
            processing_provider="deterministic",
            model_version=None
        )
