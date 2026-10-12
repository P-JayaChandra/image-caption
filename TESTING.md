# VisionSpeak Testing Guide

## Running Tests Locally

### Python Unit Tests
```bash
# Run all unit tests
pytest tests/unit -v

# Run tests with short traceback
pytest tests/unit --tb=short

# Run a specific test module
pytest tests/unit/test_api_endpoints.py -v
```

### Pytest Coverage
The unit test suite covers:
1. `test_device.py`: Hardware device detection (CPU vs. CUDA).
2. `test_config.py`: Singleton configuration behavior.
3. `test_image_validator.py`: Format, dimensions, and corrupt file rejection.
4. `test_preprocessor.py`: Image normalization and RGB conversion.
5. `test_caption_generator.py`: Multi-style caption generation.
6. `test_database_and_repository.py`: SQLite persistence and edit auditing.
7. `test_exporter.py`: JSON, CSV, and plain text export.
8. `test_api_endpoints.py`: FastAPI routes, health checks, and errors.
