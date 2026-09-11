import json
from statistics import mean

from src.config import settings


def main() -> None:

    files = sorted(settings.chunks_dir.glob("*.json"))

    print(
        f"{'Paper':30}"
        f"{'Chunks':10}"
        f"{'Avg Size':12}"
        f"{'Min':8}"
        f"{'Max':8}"
        f"{'Sections':10}"
    )

    print("-" * 78)

    corpus_sizes: list[int] = []

    for path in files:

        data = json.loads(path.read_text(encoding="utf-8"))

        chunks = data["chunks"]

        sizes = [chunk["character_count"] for chunk in chunks]

        sections = {chunk["section"] for chunk in chunks if chunk["section"]}

        corpus_sizes.extend(sizes)

        average = mean(sizes) if sizes else 0

        minimum = min(sizes) if sizes else 0

        maximum = max(sizes) if sizes else 0

        print(
            f"{data['paper_id'][:29]:30}"
            f"{len(chunks):10}"
            f"{average:12.0f}"
            f"{minimum:8}"
            f"{maximum:8}"
            f"{len(sections):10}"
        )

    print()
    print("=" * 78)

    if corpus_sizes:

        print(f"Corpus chunks : " f"{len(corpus_sizes)}")

        print(f"Average size  : " f"{mean(corpus_sizes):.0f} chars")

        print(f"Minimum size  : " f"{min(corpus_sizes)} chars")

        print(f"Maximum size  : " f"{max(corpus_sizes)} chars")


if __name__ == "__main__":
    main()
