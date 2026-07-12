from typing import List, Dict, Any

class ObjectiveMapper:
    """Maps learning objectives to one or more lesson sections based on cognitive levels or indices."""
    
    @staticmethod
    def map_objectives(objectives: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        mapping = {}
        for obj in objectives:
            obj_id = obj.get("id")
            if not obj_id:
                continue
                
            bloom = obj.get("bloom_level", "Understand")
            
            # Every objective maps to 'Learning Objectives'
            sections = ["Learning Objectives"]
            
            if bloom in ["Remember", "Understand"]:
                sections.extend(["Prior Knowledge", "Lesson Development"])
            elif bloom in ["Apply", "Analyze"]:
                sections.extend(["Guided Practice", "Independent Practice"])
            elif bloom in ["Evaluate", "Create"]:
                sections.extend(["Review", "Reflection"])
            else:
                sections.extend(["Lesson Development"])
                
            mapping[obj_id] = sections
            
        return mapping
