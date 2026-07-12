LESSON_ENRICHMENT_PROMPT = """
You are an expert STEM educator. Enhance the following deterministic lesson plan with teaching details.
Subject: {subject}
Timeline / Sections: {sections}
Objectives: {objectives}

Provide:
1. Detailed teacher notes for each section.
2. Engagement suggestions for each section.
3. Pacing recommendations for each section.
4. Rich connecting statements (transition note) between consecutive sections.

Return output in JSON format matching this schema:
{{
  "teacher_notes": {{
     "Section Title": "notes"
  }},
  "engagement_suggestions": {{
     "Section Title": "suggestions"
  }},
  "pacing_recommendations": {{
     "Section Title": "pacing advice"
  }},
  "enhanced_transitions": {{
     "Section A -> Section B": "transition note"
  }},
  "confidence": 0.95
}}
"""

DIFFERENTIATION_ENRICHMENT_PROMPT = """
You are an expert STEM educator. Enrich the differentiation recommendations for the following lesson:
Subject: {subject}
Timeline: {sections}

For each of the following learner profiles:
- Below Grade Level
- On Grade Level
- Above Grade Level
- English Language Learners (ELL)
- Students with Special Educational Needs (SEN)
- Gifted Learners

Provide:
1. Customized accommodations.
2. Intervention strategies.
3. Enrichment recommendations.

Return output in JSON matching this schema:
{{
  "accommodations": {{
     "Profile Name": "accommodation text"
  }},
  "intervention_strategies": {{
     "Profile Name": "intervention text"
  }},
  "enrichment_recommendations": {{
     "Profile Name": "enrichment text"
  }}
}}
"""
