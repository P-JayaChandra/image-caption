# VisionSpeak Lines of Code (LOC) Report

This report provides an honest, reproducible accounting of lines of code across VisionSpeak.

## Measurement Policy
- **Source Code (SLOC)**: Excludes blank lines and comment-only lines.
- **Generated Rules**: Stored in `generated_scale/` and categorized distinctly from handwritten core logic.
- **Excluded**: `node_modules`, `.git`, `dist`, `.pytest_cache`, and virtual environments.

## Current Baseline
Run `python scripts/count_loc.py` to regenerate metrics at any time.
