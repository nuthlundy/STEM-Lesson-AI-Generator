# STEM Lesson AI Generator - System Architecture

This document provides a comprehensive technical overview of the system architecture, currently implemented components (Phases 1-4), directory-based workspaces, and pipeline contracts.

---

## 1. High-Level Architecture Overview

The application utilizes an asynchronous, stage-gated, file-driven pipeline. Each execution stage consumes the output file of the previous engine, performs specific enhancements, and writes its output as a new file inside an isolated job workspace. This eliminates state mutation and ensures full traceability.

```text
               +-----------------------------+
               |      Client Request         |
               +--------------+--------------+
                              | Upload PDF
                              v
               +--------------+--------------+
               |     FastAPI /pdf/upload     |
               +--------------+--------------+
                              | Stager
                              v
               +--------------+--------------+
               |   Asynchronous Task Worker  |
               +--------------+--------------+
                              |
     +------------------------+------------------------+
     | Stage 1                                         | Stage 2
     v                                                 v
+----+------------------------+                   +----+------------------------+
| Document Intelligence Engine|                   |  Language Intelligence Engine|
| (DIE)                       |                   |  (LIE)                      |
| Inputs: raw_file.pdf        |                   |  Inputs: lesson.json        |
| Outputs: lesson.json, assets|                   |  Outputs: lesson_language.json|
+-----------------------------+                   +-----------------------------+
```

---

## 2. Directory Workspace Lifecycle

All processing artifacts for a given upload are confined to a dedicated workspace folder:
```text
uploads/jobs/{job_id}/
├── raw_file.pdf             # The original uploaded document
├── lesson.json              # Canonical output of Phase 3 (Document Intelligence)
├── lesson_language.json     # Canonical output of Phase 4 (Language Intelligence)
└── assets/                  # Directory for cropped images, figures, and tables
    ├── table_b1_p1.png      # Structured table crop
    ├── figure_b2_p1.png     # Diagram or figure crop
    └── equation_b3_p2.png   # Mathematical formula crop
```

---

## 3. Core Engine Components (Implemented)

### 3.1 Document Intelligence Engine (DIE)
Located in `backend/services/document_intelligence/`. This engine parses structural layout and extracts blocks deterministically without AI.

*   **`DocumentIntelligenceEngine` (`engine.py`)**: The central orchestrator that coordinates extractors, checks document density to decide on native vs. OCR extraction, runs table/image detection, and outputs `lesson.json`.
*   **`NativePDFExtractor` (`extractors/native_pdf.py`)**: Uses PyMuPDF (`fitz`) to extract native PDF characters, fonts, text segments, and geometric bounding boxes.
*   **`OCRExtractor` (`extractors/ocr.py`)**: Wraps PyTesseract to perform optical character recognition on page images when text density is too low or native text is absent.
*   **`ImageFigureExtractor` (`extractors/image_figure.py`)**: Employs OpenCV contour analysis to detect images, charts, and diagrams, cropping and tagging them as standalone visual blocks.
*   **`TableEquationExtractor` (`extractors/table_equation.py`)**: Segregates tabular structures and mathematical formula regions, preserving their coordinate geometries for extraction.
*   **`AssetManager` (`utils/asset_manager.py`)**: Handles the file operations, naming conventions, and validation for saving visual crop files to the `assets/` directory.

### 3.2 Language Intelligence Engine (LIE)
Located in `backend/services/language_intelligence/`. This engine performs text cleanup, language identification, and semantic tagging using a pluggable, hybrid deterministic-AI architecture.

*   **`LanguageIntelligenceEngine` (`engine.py`)**: Orchestrates the language processing pipeline, leveraging concurrent processing (`asyncio.gather`), updating metrics, and writing `lesson_language.json`.
*   **`TextCleaner` (`utils/text_cleaner.py`)**: Normalizes whitespace, cleans layout/OCR artifacts, and resolves word hyphenations spanning across line-breaks (e.g. `kine-\nmatics` -> `kinematics`).
*   **`ProcessorFactory` (`processors/factory.py`)**: Dynamically loads and returns the configured `LanguageProcessor` (e.g. `GeminiProcessor`, `DeterministicProcessor`) based on `active_provider` settings.
*   **`DeterministicProcessor` (`processors/deterministic.py`)**: Executes deterministic text cleaning and basic character-set language analysis (e.g. `en`). Assigns `SemanticRole.UNKNOWN` and a `null` confidence score.
*   **`GeminiProcessor` (`processors/gemini_processor.py`)**: Interacts with the Gemini API using `google.generativeai` to assign semantic roles (`definition`, `theorem`, `example`, `explanation`) and extract technical keywords. Implements a fail-safe strategy: if keys are missing or requests fail, it falls back to the deterministic pipeline.

### 3.3 Subject Intelligence Engine (SIE)
Located in `backend/services/subject_intelligence/`. This engine extracts domain-specific concepts (e.g. mathematical physics, chemistry) and establishes relational learning taxonomies.
*   **`SubjectIntelligenceEngine` (`engine.py`)**: Coordinates the processing steps, outputting `lesson_subject.json`, `lesson_learning_objectives.json`, and `lesson_instructional_model.json`.

### 3.4 Lesson Planning Engine (LPE)
Located in `backend/services/lesson_planning/`. Maps concepts to pedagogically sound lesson plans based on structures like the 5E Instructional Model.
*   **`LessonPlanningEngine` (`engine.py`)**: Orchestrates the generation of assessment plans, teaching blueprints, and learning sequences, outputting `lesson_plan.json`.

### 3.5 Rendering Engine (RE)
Located in `backend/services/rendering/`. Converts lesson plans into interactive slide layouts.
*   **`RenderingEngine` (`engine.py`)**: Renders layout structures and themes, writing `lesson_render.json` and `lesson_themed.json`.

### 3.6 Presentation Engine (PE)
Located in `backend/services/presentation/`. Transforms themed layouts into clean interactive slide decks and exports them.
*   **`PresentationEngine` (`engine.py`)**: Validates slides content and generates physical deliverables like `presentation_session.json` and `lesson.pdf`.

### 3.7 Workspace Engine
Located in `backend/services/workspace/`. Implements templates library, project registries, settings, profiles, search indexes, autosaves, and automated workspace recovery repairs.
*   **`WorkspaceEngine` (`engine.py`)**: Coordinates all lifecycle actions (initialize, load, save, close, shutdown, recovery) and registers cross-module event dispatching.


---

## 4. Canonical Schema Contracts

Data contracts are enforced strictly using Pydantic (v2) models to ensure absolute schema compliance across development phases.

### 4.1 Document Intelligence Schemas (`document_intelligence/interfaces.py`)
*   **`DocumentMetadata`**: Metadata about the job execution (total pages, original filename, processing duration, OCR indicators).
*   **`DocumentBlock`**: A structural segment of the document (text, bounding box `bbox`, page number, block ID, source tag, confidence score).
*   **`ExtractedAsset`**: Metadata representing a saved physical file inside the workspace assets folder.
*   **`ProcessingMetrics`**: Tracks performance timings, page counts, and logging of recoverable errors.
*   **`DocumentIntelligenceResult`**: The structure serialized into `lesson.json`.

### 4.2 Language Intelligence Schemas (`language_intelligence/interfaces.py`)
*   **`SemanticRole`**: Enum containing `definition`, `theorem`, `example`, `explanation`, and `unknown`.
*   **`LinguisticMetadata`**: Stores the semantic taxonomy (`cleaned_text`, `original_text`, `language`, `semantic_role`, `confidence`, `keywords`, `processing_provider`, `model_version`).
*   **`EnrichedDocumentBlock`**: Embeds a `LinguisticMetadata` object into the original `DocumentBlock` schema.
*   **`LanguageIntelligenceResult`**: The structure serialized into `lesson_language.json`.

---

## 5. System Dependency Diagram

```text
[pdf_worker.py]
      │
      ├──────► [DocumentIntelligenceEngine]
      │              │
      │              ├──────► [NativePDFExtractor]
      │              ├──────► [OCRExtractor] (Tesseract)
      │              ├──────► [ImageFigureExtractor] (OpenCV)
      │              ├──────► [TableEquationExtractor]
      │              └──────► [AssetManager]  ──► Writes to disk (assets/)
      │
      └──────► [LanguageIntelligenceEngine]
                     │
                     └──────► [ProcessorFactory]
                                    │
                                    ├──► [GeminiProcessor]  ──► (Optional Gemini API)
                                    └──► [DeterministicProcessor] ──► [TextCleaner]
```
