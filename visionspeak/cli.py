"""
VisionSpeak Command Line Interface (CLI)
========================================
Developer and operator CLI for serving the API, running local image captioning,
pre-caching weights, and running system health diagnostics.
"""

import sys
import argparse
from pathlib import Path

# Force UTF-8 stdout and stderr encoding on Windows terminals to support emojis
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(
        prog="visionspeak",
        description="VisionSpeak AI — Local Salesforce BLIP Image Captioning Platform"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: serve
    serve_parser = subparsers.add_parser("serve", help="Start the FastAPI REST server")
    serve_parser.add_argument("--host", default="127.0.0.1", help="Host binding (default: 127.0.0.1)")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port binding (default: 8000)")
    serve_parser.add_argument("--reload", action="store_true", help="Enable live auto-reload")

    # Command: caption
    caption_parser = subparsers.add_parser("caption", help="Generate AI captions for a local image file")
    caption_parser.add_argument("image_path", help="Path to image (JPEG, PNG, WebP)")
    caption_parser.add_argument("--category", default="Other", help="Target category (Nature, Travel, Food, etc.)")
    caption_parser.add_argument("--tone", default="Aesthetic", help="Preferred tone (Aesthetic, Emotional, etc.)")

    # Command: health
    subparsers.add_parser("health", help="Display local model, hardware, and system diagnostics")

    # Command: benchmark
    subparsers.add_parser("benchmark", help="Benchmark local inference speed and latency")

    # Command: download-weights
    subparsers.add_parser("download-weights", help="Pre-download and cache BLIP model weights locally")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "serve":
        import uvicorn
        print(f"============================================================")
        print(f"  Starting VisionSpeak Local AI API on http://{args.host}:{args.port}")
        print(f"  Swagger Docs: http://{args.host}:{args.port}/docs")
        print(f"============================================================")
        uvicorn.run("visionspeak.api.app:app", host=args.host, port=args.port, reload=args.reload)

    elif args.command == "health":
        from visionspeak.models.manager import get_model_manager
        import json
        mgr = get_model_manager()
        print(json.dumps(mgr.get_status(), indent=2))

    elif args.command == "download-weights":
        print("Pre-caching Salesforce BLIP model weights...")
        from visionspeak.models.manager import get_model_manager
        mgr = get_model_manager()
        model = mgr.get_model(auto_load=True)
        print(f"Successfully loaded and cached: {model.status().model_name}")

    elif args.command == "caption":
        path = Path(args.image_path)
        if not path.exists():
            print(f"Error: File not found at '{path}'", file=sys.stderr)
            sys.exit(1)

        from visionspeak.processing.image_validator import ImageValidator
        from visionspeak.processing.preprocessor import ImagePreprocessor
        from visionspeak.models.manager import get_model_manager
        from visionspeak.generation.caption_generator import CaptionGenerator

        validator = ImageValidator()
        with open(path, "rb") as f:
            raw_bytes = f.read()

        pil_img, _ = validator.validate(raw_bytes)
        preprocessed = ImagePreprocessor.preprocess_for_model(pil_img)

        mgr = get_model_manager()
        model = mgr.get_model(auto_load=True)
        generator = CaptionGenerator(model)

        output = generator.generate_all_styles(preprocessed, category=args.category, tone=args.tone)

        print("\n" + "=" * 60)
        print(f"  VISIONSPEAK AI ANALYSIS: {path.name}")
        print("=" * 60)
        print(f"Description: {output.description}")
        print(f"Tags: {', '.join(output.tags)}")
        print(f"Device: {output.device} | Latency: {output.total_latency_ms} ms")
        print("-" * 60)
        for c in output.captions:
            print(f"\n[{c['style'].upper()}]:")
            print(f"  {c['text']}")
            print(f"  Hashtags: {' '.join(c['hashtags'])}")
        print("\n[ACCESSIBILITY ALT-TEXT]:")
        print(f"  {output.alt_text}")
        print("=" * 60 + "\n")

    elif args.command == "benchmark":
        print("Running benchmark...")
        from visionspeak.models.manager import get_model_manager
        from PIL import Image
        import time

        mgr = get_model_manager()
        model = mgr.get_model(auto_load=True)
        test_img = Image.new("RGB", (384, 384), color=(100, 150, 200))
        latencies = []
        for i in range(3):
            t0 = time.perf_counter()
            model.generate(test_img, max_new_tokens=25, num_beams=1)
            ms = (time.perf_counter() - t0) * 1000.0
            latencies.append(ms)
            print(f"  Run {i+1}: {ms:.1f} ms")

        avg_ms = sum(latencies) / len(latencies)
        print(f"\nAverage Latency: {avg_ms:.1f} ms | Approx {1000.0/avg_ms:.2f} images/sec")

if __name__ == "__main__":
    main()
