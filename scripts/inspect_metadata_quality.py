import json

from src.config import settings


def main() -> None:
    files = sorted(settings.metadata_dir.glob("*.json"))

    print("=" * 100)
    print("METADATA QUALITY REPORT")
    print("=" * 100)

    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))

        print()
        print("-" * 100)
        print(data["paper_id"])
        print("-" * 100)

        print(f"Title       : {data['title']}")

        print(f"Year        : {data['year']}")

        print(f"Authors     : {len(data['authors'])}")

        print(f"Abstract    : " f"{'YES' if data['abstract'] else 'NO'}")

        if data["abstract"]:
            print("Abstract preview:")

            print(data["abstract"][:300])

        print()
        print("Sections:")

        for section in data["sections"]:
            print(
                f"  page {section['page_number']:>2} "
                f"- {section['canonical_name']} "
                f"({section['matched_heading']})"
            )

        print()
        print("Research Questions:")

        for rq in data["research_questions"]:
            print(f"  {rq[:180]}")


if __name__ == "__main__":
    main()
