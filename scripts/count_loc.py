"""
Reproducible Lines of Code (LOC) Measurement Tool for VisionSpeak
"""
import os
import sys

EXTENSIONS = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "React JSX",
    ".ts": "TypeScript",
    ".tsx": "React TSX",
    ".css": "CSS",
    ".html": "HTML",
    ".md": "Markdown",
    ".json": "JSON"
}

IGNORE_DIRS = {
    "node_modules", ".git", ".pytest_cache", "__pycache__", "dist", "build",
    ".vscode", ".idea", "venv", ".venv", "model_weights", "temp"
}

def analyze_file(filepath):
    total = 0
    blank = 0
    comments = 0
    code = 0
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                total += 1
                s = line.strip()
                if not s:
                    blank += 1
                elif s.startswith("#") or s.startswith("//") or s.startswith("/*") or s.startswith("*"):
                    comments += 1
                else:
                    code += 1
    except Exception:
        pass
    return total, blank, comments, code

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results = {}
    total_lines = 0
    total_blank = 0
    total_comments = 0
    total_code = 0

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            if ext in EXTENSIONS:
                lang = EXTENSIONS[ext]
                path = os.path.join(dirpath, f)
                t, b, c, cd = analyze_file(path)
                if lang not in results:
                    results[lang] = {"files": 0, "total": 0, "blank": 0, "comments": 0, "code": 0}
                results[lang]["files"] += 1
                results[lang]["total"] += t
                results[lang]["blank"] += b
                results[lang]["comments"] += c
                results[lang]["code"] += cd
                total_lines += t
                total_blank += b
                total_comments += c
                total_code += cd

    print("=" * 60)
    print("  VISIONSPEAK REPRODUCIBLE LOC REPORT")
    print("=" * 60)
    print(f"{'Language':<15} | {'Files':<6} | {'Total':<8} | {'Blank':<6} | {'Code (SLOC)':<10}")
    print("-" * 60)
    for lang, data in sorted(results.items()):
        print(f"{lang:<15} | {data['files']:<6} | {data['total']:<8} | {data['blank']:<6} | {data['code']:<10}")
    print("=" * 60)
    print(f"TOTAL LINES: {total_lines:,} | SLOC: {total_code:,}")
    print("=" * 60)

if __name__ == "__main__":
    main()
