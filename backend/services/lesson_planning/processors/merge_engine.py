from typing import Dict, Any, List
from services.lesson_planning.schemas import LessonPlan, Transition

class AIMergeEngine:
    """Merges deterministic lesson plans with AI enrichment while enforcing deterministic primacy."""
    
    @staticmethod
    def merge(det_plan: LessonPlan, ai_data: Dict[str, Any]) -> LessonPlan:
        teacher_notes = ai_data.get("teacher_notes", {})
        engagement = ai_data.get("engagement_suggestions", {})
        pacing = ai_data.get("pacing_recommendations", {})
        enhanced_trans = ai_data.get("enhanced_transitions", {})
        
        merged_notes = {}
        merged_engagement = {}
        merged_pacing = {}
        
        for sec in det_plan.lesson_sections:
            title = sec.title
            merged_notes[title] = teacher_notes.get(title, f"Default notes for {title}.")
            merged_engagement[title] = engagement.get(title, f"Default engagement tips for {title}.")
            merged_pacing[title] = pacing.get(title, f"Standard pacing: {sec.duration_minutes} minutes.")
            
        merged_transitions = []
        for trans in det_plan.transitions:
            key = f"{trans.from_section} -> {trans.to_section}"
            note = enhanced_trans.get(key, trans.transition_notes)
            merged_transitions.append(Transition(
                from_section=trans.from_section,
                to_section=trans.to_section,
                transition_notes=note
            ))
            
        confidence = ai_data.get("confidence", 0.90)
        
        # 1. Merge differentiation fields
        ai_accommodations = ai_data.get("accommodations", {})
        ai_interventions = ai_data.get("intervention_strategies", {})
        ai_enrichment = ai_data.get("enrichment_recommendations", {})
        
        # Fallback to deterministic profiles if AI output is sparse
        from services.lesson_planning.schemas import DifferentiationBlock
        merged_accommodations = {}
        merged_interventions = {}
        merged_enrichment = {}
        
        profiles = det_plan.learner_profiles if det_plan.learner_profiles else []
        for profile in profiles:
            merged_accommodations[profile] = ai_accommodations.get(profile, det_plan.accommodations.get(profile, f"Default accommodations for {profile}"))
            merged_interventions[profile] = ai_interventions.get(profile, det_plan.intervention_strategies.get(profile, f"Default interventions for {profile}"))
            merged_enrichment[profile] = ai_enrichment.get(profile, det_plan.enrichment_recommendations.get(profile, f"Default enrichment for {profile}"))
            
        diff_block = DifferentiationBlock(
            learner_profiles=profiles,
            accommodations=merged_accommodations,
            intervention_strategies=merged_interventions,
            enrichment_recommendations=merged_enrichment
        )

        # 2. Merge assessment plan
        from services.lesson_planning.schemas import AssessmentPlan, AssessmentBlueprintItem
        from services.lesson_planning.assessment.taxonomy import BloomTaxonomy
        from services.lesson_planning.assessment.weighting import AssessmentWeighting
        
        ai_blueprint = ai_data.get("assessment_blueprint", [])
        ai_item_map = {item.get("assessment_type"): item for item in ai_blueprint if isinstance(item, dict)}
        
        merged_blueprint = []
        det_blueprint = det_plan.assessment_blueprint if det_plan.assessment_blueprint else []
        for det_item in det_blueprint:
            ai_item = ai_item_map.get(det_item.assessment_type, {})
            weight = ai_item.get("weight", det_item.weight)
            q_count = ai_item.get("target_questions_count", det_item.target_questions_count)
            merged_blueprint.append(AssessmentBlueprintItem(
                assessment_type=det_item.assessment_type,
                topic=ai_item.get("topic", det_item.topic),
                weight=weight,
                target_questions_count=q_count,
                alignment=det_item.alignment
            ))
            
        merged_alignments = []
        for item in merged_blueprint:
            merged_alignments.extend(item.alignment)
            
        bloom_dist = BloomTaxonomy.calculate_distribution(merged_alignments)
        question_dist = AssessmentWeighting.calculate_question_distribution(merged_blueprint)
        
        assessment_block = AssessmentPlan(
            assessment_blueprint=merged_blueprint,
            bloom_distribution=bloom_dist,
            question_distribution=question_dist,
            assessment_alignment=merged_alignments
        )

        # 3. Merge teacher guidance and readiness
        ai_guidance = ai_data.get("teacher_guidance", det_plan.teacher_guidance)
        ai_materials = ai_data.get("materials", det_plan.materials)
        ai_preparation = ai_data.get("preparation", det_plan.preparation)
        ai_management = ai_data.get("classroom_management", det_plan.classroom_management)
        ai_misconceptions = ai_data.get("misconceptions", det_plan.misconceptions)
        ai_reflection = ai_data.get("reflection_prompts", det_plan.reflection_prompts)
        
        from services.lesson_planning.guidance.validator import LessonReadinessValidator
        has_objectives = bool(det_plan.objective_mapping)
        has_assessment = bool(assessment_block.assessment_blueprint)
        is_timing_valid = det_plan.validation_report.valid
        has_materials = len(ai_materials) > 0
        
        readiness_report = LessonReadinessValidator.evaluate_readiness(
            has_objectives=has_objectives,
            has_assessment=has_assessment,
            is_timing_valid=is_timing_valid,
            has_materials=has_materials,
            extra_details={
                "validation_errors": det_plan.validation_report.errors,
                "sections_count": len(det_plan.lesson_sections)
            }
        )

        ai_enrichment_block = {
            "teacher_notes": merged_notes,
            "engagement_suggestions": merged_engagement,
            "pacing_recommendations": merged_pacing,
            "enhanced_transitions": enhanced_trans,
            "confidence": confidence,
            "differentiation": {
                "accommodations": merged_accommodations,
                "intervention_strategies": merged_interventions,
                "enrichment_recommendations": merged_enrichment
            },
            "assessment": {
                "question_distribution": question_dist,
                "bloom_distribution": bloom_dist
            },
            "guidance": {
                "teacher_guidance": ai_guidance,
                "materials": ai_materials,
                "preparation": ai_preparation,
                "classroom_management": ai_management,
                "misconceptions": ai_misconceptions,
                "reflection_prompts": ai_reflection
            }
        }
        
        return LessonPlan(
            engine_name=det_plan.engine_name,
            engine_version=det_plan.engine_version,
            schema_version=det_plan.schema_version,
            generated_at=det_plan.generated_at,
            source_artifacts=det_plan.source_artifacts,
            subject=det_plan.subject,
            title=det_plan.title,
            lesson_structure=det_plan.lesson_structure,
            lesson_sections=det_plan.lesson_sections,
            timeline=det_plan.timeline,
            transitions=merged_transitions,
            objective_mapping=det_plan.objective_mapping,
            validation_report=det_plan.validation_report,
            
            ai_enrichment=ai_enrichment_block,
            teacher_notes=merged_notes,
            engagement_suggestions=merged_engagement,
            pacing_recommendations=merged_pacing,
            confidence=confidence,
            
            # Differentiation fields
            differentiation=diff_block,
            learner_profiles=profiles,
            accommodations=merged_accommodations,
            intervention_strategies=merged_interventions,
            enrichment_recommendations=merged_enrichment,
            
            # Assessment fields
            assessment_plan=assessment_block,
            assessment_blueprint=merged_blueprint,
            bloom_distribution=bloom_dist,
            question_distribution=question_dist,
            assessment_alignment=merged_alignments,
            
            # Guidance fields
            teacher_guidance=ai_guidance,
            materials=ai_materials,
            preparation=ai_preparation,
            classroom_management=ai_management,
            misconceptions=ai_misconceptions,
            reflection_prompts=ai_reflection,
            lesson_readiness=readiness_report
        )
