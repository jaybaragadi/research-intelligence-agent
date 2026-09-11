import json

from src.config import settings


def main() -> None:

    files = sorted(settings.metadata_dir.glob("*.json"))

    print(
        f"{'Paper':30}"
        f"{'Year':8}"
        f"{'Abstract':10}"
        f"{'Sections':10}"
        f"{'RQs':6}"
        f"{'Signals':8}"
    )

    print("-" * 72)

    for path in files:

        data = json.loads(path.read_text(encoding="utf-8"))

        print(
            f"{data['paper_id'][:29]:30}"
            f"{str(data['year']):8}"
            f"{str(bool(data['abstract'])):10}"
            f"{len(data['sections']):10}"
            f"{len(data['research_questions']):6}"
            f"{len(data['research_signals']):8}"
        )


if __name__ == "__main__":
    main()
