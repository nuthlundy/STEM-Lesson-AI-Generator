# Document Intelligence Engine (DIE)

The Document Intelligence Engine (DIE) represents **Phase 3** of the STEM Lesson AI Generator project. It forms the entry point of the ingestion pipeline, transforming unstructured educational PDF documents into a structured, deterministic intermediate JSON format (`lesson.json`).

---

## Ingestion Pipeline Position
```text
[PDF Upload]
     │
     ▼
┌─────────────────────────────────┐
│  Document Intelligence Engine   │  ◄── (Phase 3 - Current Module)
└─────────────────────────────────┘
     │
     ▼
[lesson.json (Intermediate Representation)]
     │
     ▼
[Language Intelligence Engine]       ◄── (Phase 4)
     │
     ▼
[Subject Intelligence Engine]        ◄── (Phase 5)
```

---

## 1. Architecture Overview
The DIE is built on five core architectural principles:
1. **Deterministic Execution**: The engine uses **zero AI**. It operates entirely via algorithmic rules, layout heuristics, and OCR libraries. All AI reasoning is deferred to subsequent pipeline phases.
2. **Single Source of Truth**: The output file `lesson.json` is the sole source of truth for downstream engines. Downstream engines never parse the raw PDF.
3. **Plug-in Extractor Pattern**: Every extraction task (native text, OCR, image, table, figure, equation) is isolated into a dedicated class implementing the `BaseExtractor` interface. They are decoupled and fully swappable.
4. **Fail-Safe Design**: Document processing is isolated at the page level. If an unhandled parser exception occurs on one page, it is caught, recorded as a warning/recoverable error, and the engine continues processing remaining pages.
5. **Observability**: Execution timings, processing progress, warnings, and error logs are buffered and serialized within the final JSON output.

---

## 2. Processing Pipeline
1. **Initialize Workspace**: The `AssetManager` allocates a job directory (`uploads/jobs/{job_id}/`).
2. **Open Document**: The `DocumentIntelligenceEngine` opens the PDF file using a context manager.
3. **Loop Over Pages**:
   - **OCR Check**: Evaluates if the page contains extractable native text. If below 50 characters, routes the page to the **OCR Fallback** pipeline.
   - **Text Extraction**: Uses either **Native PDF Parser** or **OCR Fallback**.
   - **Graphic Extraction**: Dispatches **Image** and **Figure** extractors to pull raster images and vector diagrams.
   - **Structure Extraction**: Dispatches **Table** and **Equation** extractors.
4. **Deduplication**: Runs bounding-box and text substring comparisons to filter out paragraphs duplicated by tables or math equations.
5. **Compile Metrics**: Measures total processing time, progress, and buffered logging output.
6. **Serialize Output**: Writes the aggregated result conforming to `DocumentIntelligenceResult` schemas into `lesson.json`.

---

## 3. Extractor Responsibilities
- **Native PDF Extractor (`native_pdf.py`)**: Parses PDF text streams. Classifies layout blocks as `heading` (based on font sizing relative to the heading threshold), `list` (detecting bullet glyphs or numbering), or `paragraph`.
- **OCR Extractor (`ocr.py`)**: Renders pages into PIL Images, extracts structured words using Tesseract's `image_to_data`, reconstructs blocks, maps coordinates back to PDF points, and tracks word-level confidence averages.
- **Image Extractor (`image.py`)**: Pulls raw binary images. Ignores spacer graphics and icons under 100x100 pixels.
- **Figure Extractor (`figure.py`)**: Inspects vector drawings. If drawing density is high (>= 15 paths), calculates the boundary cluster, rasterizes the clipped region to a high-res PNG, and registers a single figure asset.
- **Table Extractor (`table.py`)**: Uses PyMuPDF's grid detection algorithms, parses cell data, and formats the structure into a Markdown table representation.
- **Equation Extractor (`equation.py`)**: Scans for standard math fonts and mathematical character clusters (e.g., integrals, Greek symbols, LaTeX strings) to classify specialized equation blocks.

---

## 4. Execution Order (Page Loop)
For every page in the PDF, extractors are invoked in the following sequence:

```text
[Page Ingestion]
       │
       ├─► (Check Character Density)
       │         │
       │         ├──► [Density < 50 Chars] ──► [OCR Extractor]
       │         │
       │         └──► [Density >= 50 Chars] ─► [Native PDF Extractor]
       │                                      [Table Extractor]
       │                                      [Equation Extractor]
       │
       ├─► [Image Extractor] (All pages)
       ├─► [Figure Extractor] (All pages)
       │
       ▼
[Deduplication / Paragraph Overlaps]
```

---

## 5. `lesson.json` Schema
Downstream engines consume the serialized JSON output of the DIE. Below is an example structured payload:

```json
{
  "metadata": {
    "job_id": "job_123",
    "original_filename": "kinematics_notes.pdf",
    "total_pages": 3,
    "processing_time_sec": 0.45,
    "requires_ocr": false,
    "schema_version": "1.0.0"
  },
  "blocks": [
    {
      "block_id": "blk_89f07a21",
      "block_type": "heading",
      "text": "1. Introduction to Motion",
      "page_number": 1,
      "bbox": {
        "x0": 50.0,
        "y0": 50.0,
        "x1": 250.0,
        "y1": 70.0
      },
      "confidence": 1.0,
      "source": "native_pdf",
      "metadata": {
        "font_name": "hebo",
        "font_size": 20.0
      }
    }
  ],
  "assets": [
    {
      "asset_id": "img_f901c23a",
      "asset_type": "image",
      "file_path": "assets/job_123_page3_image_0.png",
      "page_number": 3,
      "bbox": {
        "x0": 50.0,
        "y0": 50.0,
        "x1": 200.0,
        "y1": 200.0
      },
      "confidence": 1.0,
      "source": "image",
      "metadata": {
        "width": 150,
        "height": 150
      }
    }
  ],
  "metrics": {
    "progress": 100.0,
    "execution_time": 0.45,
    "warnings": [],
    "recoverable_errors": [],
    "fatal_errors": []
  }
}
```

---

## 6. AssetManager & Job Workspace Lifecycle
The `AssetManager` (`utils/asset_manager.py`) is the centralized unit managing filesystem workspaces.

### Directory Structure
```text
uploads/jobs/
└── {job_id}/
    ├── lesson.json
    └── assets/
        ├── {job_id}_page3_image_0.png
        └── {job_id}_page5_figure_0.png
```

### Lifecycle Stages
1. **Creation**: When the engine process starts, `create_job_workspace()` ensures `uploads/jobs/{job_id}/assets/` directories exist on disk.
2. **Persistence**: Extracted images/rasterized figures are written to the `assets/` subfolder. `save_asset()` returns the relative path (e.g. `assets/...`) for DB/JSON references.
3. **Tear-Down**: The `clean_job_workspace()` method clears the directory. The DIE does *not* invoke this automatically; cleanup is deferred to the history manager in Phase 9.

---

## 7. Extension Guide: Adding a Custom Extractor
To introduce a new extraction type (e.g., custom charts or barcodes):
1. **Define the Extractor**: Create a file in `extractors/` (e.g., `chart_extractor.py`) inheriting from `BaseExtractor`:
   ```python
   from services.document_intelligence.extractors.base import BaseExtractor
   
   class ChartExtractor(BaseExtractor):
       def extract(self, page, page_number):
           # Custom detection logic
           return []
   ```
2. **Register in Interfaces**: If the extractor introduces a new block/asset type, update the `Literal` fields in `interfaces.py`.
3. **Register in Engine**: Import and append the extractor to the extraction pipeline inside `engine.py`.

---

## 8. Testing Strategy
Our testing strategy enforces high reliability via dynamic, self-contained mocked PDF generation:
- **No External Test Fixture Files**: We generate test PDF data in-memory using PyMuPDF and write them to temp directories, ensuring 100% deterministic test isolation.
- **Test Categories**:
  - `test_interfaces.py`: Validates Pydantic schema typing and confidence constraints.
  - `test_asset_manager.py`: Tests relative path mappings and I/O.
  - `test_native_pdf.py`: Tests font-based layout tags.
  - `test_ocr.py`: Verifies word grouping, OCR coordinates, and mock Tesseract outputs.
  - `test_image_figure.py`: Validates binary writes and vector drawings density detection.
  - `test_table_equation.py`: Tests line-drawn grids and math equation tag heuristics.
  - `test_engine.py`: Integration test checking complete end-to-end execution and JSON serialization.

---

## 9. Dependency List
- `PyMuPDF` (fitz): Core PDF parser.
- `pytesseract`: OCR engine binding.
- `Pillow`: Image file reading and writing.
- `numpy` & `opencv-python-headless`: OpenCV image buffers manipulation.
- `pydantic` & `pydantic-settings`: Types and settings configuration.

---

## 10. Troubleshooting
### `ModuleNotFoundError: No module named 'pydantic'`
Make sure the Python virtual environment is activated and the requirements are installed:
```powershell
venv\Scripts\pip install -r backend/requirements.txt
```

### `pytesseract.pytesseract.TesseractError: Could not initialize tesseract`
Tesseract needs language pack files inside its data directory. DIE automatically sets `TESSDATA_PREFIX` on Windows if Tesseract is located at `C:\Program Files\Tesseract-OCR\`. Verify Tesseract installation or ensure your system environment variables point to the correct `tessdata` directory.

### `NameError: name 'Protocol' is not defined`
Ensure you are using Python 3.8+ and importing `Protocol` from `typing`:
```python
from typing import Protocol
```
