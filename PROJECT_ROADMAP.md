# STEM Lesson AI Generator - Project Roadmap

This document outlines the 10-phase development roadmap for the STEM Lesson AI Generator project. The architecture uses a frozen, modular structure where each phase builds upon the outputs of previous phases. The primary intermediary data contracts are strictly maintained as JSON files within each job's workspace.

```mermaid
gantt
    title Development Roadmap & Phase Status
    dateFormat  YYYY-MM-DD
    section Completed Phases
    Phase 1: Project Foundation        :done, des1, 2026-07-01, 2026-07-03
    Phase 2: Dashboard Foundation      :done, des2, 2026-07-03, 2026-07-05
    Phase 3: Document Intelligence Engine :done, des3, 2026-07-05, 2026-07-09
    Phase 4: Language Intelligence Engine :done, des4, 2026-07-09, 2026-07-11
    section Active & Upcoming Phases
    Phase 5: Subject Intelligence Engine  :active, des5, 2026-07-11, 2026-07-15
    Phase 6: Lesson Planning Engine       :      des6, 2026-07-15, 2026-07-20
    Phase 7: Rendering Engine             :      des7, 2026-07-20, 2026-07-25
    Phase 8: Presentation Engine          :      des8, 2026-07-25, 2026-07-30
    Phase 9: History & Settings           :      des9, 2026-07-30, 2026-08-03
    Phase 10: Optimization & Production   :      des10, 2026-08-03, 2026-08-08
```

---

## Phase 1: Project Foundation
*Status: Completed*

Establish the core application shell, setup configuration files, and setup dependency structures.
- **Milestones**:
  - FastAPI backend configured with base routing.
  - Setup virtual environment structure and central dependency requirements (`requirements.txt`).
  - Database schema initialized with PostgreSQL using Prisma ORM.
  - Configured workspace directory structure under `/uploads/jobs/` for temporary task execution.

---

## Phase 2: Dashboard Foundation
*Status: Completed*

Develop the interactive frontend cockpit to stage, trigger, and monitor pipeline jobs.
- **Milestones**:
  - Single-page dashboard application built in React/TypeScript.
  - Interactive job-staging screen allowing raw PDF uploads.
  - Asynchronous worker loop polling for progress updates and displaying execution steps.
  - Workspace inspection interface to preview outputs.

---

## Phase 3: Document Intelligence Engine (DIE)
*Status: Completed*

Implement the layout-aware parser to extract raw content from PDF documents deterministically.
- **Milestones**:
  - Configured Native PDF text extractor using PyMuPDF.
  - Integrated PyTesseract OCR fallback workflow for scanned documents.
  - Implemented OpenCV bounding-box filters for image and figure extraction.
  - Extracted structural tables and math equation strings.
  - Outputs a canonical `lesson.json` storing structured raw blocks.

---

## Phase 4: Language Intelligence Engine (LIE)
*Status: Completed*

Linguistic cleaning and semantic role assignment using a hybrid deterministic-AI approach.
- **Milestones**:
  - Created `TextCleaner` to fix hyphenation breaks and squash spacing artifacts.
  - Implemented dynamic `ProcessorFactory` supporting pluggable AI providers.
  - Integrated `GeminiProcessor` with complete fail-safe fallback to a `DeterministicProcessor`.
  - Added semantic roles (definitions, theorems, explanations) and keywords.
  - Outputs `lesson_language.json` without modifying `lesson.json`.

---

## Phase 5: Subject Intelligence Engine (SIE)
*Status: Upcoming / Next Phase*

Validate and enrich domain-specific content based on target STEM subjects (Physics, Math, Chemistry, Computer Science).
- **Intermediary Input**: `lesson_language.json`
- **Intermediary Output**: `lesson_subject.json`
- **Milestones**:
  - Subject classification module (tagging blocks by scientific domains).
  - Formula validation (verifying equations in LaTeX format, balancing chemical equations).
  - Deep concept linking (extracting prerequisite topics and target competencies).
  - Validation of diagram labels and metadata.

---

## Phase 6: Lesson Planning Engine (LPE) / Pedagogical Intelligence Engine
*Status: Upcoming*

Transform unstructured, semantic STEM data into structured educational modules.
- **Intermediary Input**: `lesson_subject.json`
- **Intermediary Output**: `lesson_pedagogical.json`
- **Milestones**:
  - Core pedagogical mapping (mapping concepts to standard lesson planning timelines, e.g., 5E framework).
  - Estimation of lesson duration, objectives, and prerequisites.
  - Question and assessment generation aligned with bloom's taxonomy.
  - Interactive activity definition matching extracted diagrams or equations.

---

## Phase 7: Rendering Engine (RE)
*Status: Upcoming*

Convert the logical pedagogical structure into highly formatted printable and web-compatible views.
- **Intermediary Input**: `lesson_pedagogical.json`
- **Intermediary Output**: `lesson_rendered.json`
- **Milestones**:
  - Markdown, HTML, and LaTeX templates styling generation.
  - PDF compilation pipeline integrating extracted assets (images, tables, figures).
  - Interactive responsive web layout generation.

---

## Phase 8: Presentation Engine (PE)
*Status: Upcoming*

Export structured pedagogical plans into visually stunning slide decks for classroom execution.
- **Intermediary Input**: `lesson_rendered.json` or `lesson_pedagogical.json`
- **Intermediary Output**: PPTX file and structured slide models.
- **Milestones**:
  - Slide content generation (summarizing complex sections into bullet-points, matching layout structures).
  - Export system generating editable `.pptx` slides using `python-pptx`.
  - Embedding tables, equations, and images directly into native slide elements.

---

## Phase 9: History, Templates, and Settings
*Status: Upcoming*

Enable customization of template designs, subject standards, and job history management.
- **Milestones**:
  - Historical workspace archival (storing past lessons in PostgreSQL).
  - Custom slide layout template editor.
  - Management of global prompt parameters and API provider settings.

---

## Phase 10: Optimization, Performance, and Testing
*Status: Upcoming*

Ensure system performance is production-ready for scale.
- **Milestones**:
  - Implement caching layers for LLM responses and OCR artifacts.
  - Performance profiling of PDF parsing and parallel processing logic.
  - Execution of rigorous scale testing (concurrency and giant document volumes).
  - System-wide security hardening and API token optimization.
