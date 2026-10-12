"""
X / Twitter 280-Character Thread Splitter Adapter
"""
import textwrap

class TwitterThreadAdapter:
    @staticmethod
    def split_into_thread(text: str, hashtags: list = None) -> list:
        if len(text) <= 270:
            tag_str = f" {' '.join(hashtags[:2])}" if hashtags else ""
            return [f"{text}{tag_str}".strip()]

        chunks = textwrap.wrap(text, width=250)
        total = len(chunks)
        thread = []
        for i, c in enumerate(chunks, 1):
            if i == total and hashtags:
                c = f"{c} {' '.join(hashtags[:2])}"
            thread.append(f"{c} ({i}/{total})")
        return thread
