from typing import List, Dict, Any
from services.lesson_planning.schemas import AssessmentBlueprintItem, AssessmentAlignment
from services.lesson_planning.assessment.taxonomy import BloomTaxonomy

class AssessmentBlueprintBuilder:
    @staticmethod
    def build_default(subject: str, objectives_list: List[Dict[str, Any]], lesson_sections: List[Any]) -> List[AssessmentBlueprintItem]:
        blueprint = []
        alignments = []
        
        for i, obj in enumerate(objectives_list):
            obj_id = obj.get("id", f"obj_{i}")
            desc = obj.get("description", "objective")
            bloom = obj.get("bloom_level", BloomTaxonomy.UNDERSTANDING)
            standard = obj.get("standard", "NGSS.PS1" if "math" not in subject else "CCSS.MATH")
            
            sec_title = "Lesson Development"
            if lesson_sections:
                sec_title = lesson_sections[min(i, len(lesson_sections)-1)].title
                
            concept = obj.get("concept", "general STEM concept")
            
            align = AssessmentAlignment(
                assessment_objective=f"Evaluate understanding of: {desc}",
                lesson_objective_id=obj_id,
                bloom_level=bloom,
                curriculum_standard=standard,
                lesson_section=sec_title,
                concept=concept
            )
            alignments.append(align)
            
        if not alignments:
            alignments.append(AssessmentAlignment(
                assessment_objective="Evaluate core STEM competency",
                lesson_objective_id="OBJ-01",
                bloom_level=BloomTaxonomy.UNDERSTANDING,
                curriculum_standard="NGSS.PS1",
                lesson_section="Lesson Development",
                concept="STEM core"
            ))
            
        blueprint.append(AssessmentBlueprintItem(
            assessment_type="Exit Ticket",
            topic=f"{subject.capitalize()} Exit Check",
            weight=0.10,
            target_questions_count=3,
            alignment=alignments[:min(2, len(alignments))]
        ))
        
        blueprint.append(AssessmentBlueprintItem(
            assessment_type="Formative",
            topic=f"{subject.capitalize()} Mid-Lesson Check",
            weight=0.30,
            target_questions_count=5,
            alignment=alignments
        ))

        blueprint.append(AssessmentBlueprintItem(
            assessment_type="Summative",
            topic=f"{subject.capitalize()} End-of-Unit Exam",
            weight=0.60,
            target_questions_count=10,
            alignment=alignments
        ))
        
        return blueprint
