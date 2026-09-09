from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from src.analysis.literature_review_renderer import (
    LiteratureReviewMarkdownRenderer,
)

from src.analysis.literature_review_service import (
    LiteratureReviewService,
)


DEFAULT_REPORTS_DIR = Path(
    "reports"
)


def build_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        description=(
            "Generate an evidence-grounded "
            "literature review from indexed papers."
        )
    )

    parser.add_argument(
        "query",
        help=(
            "Research question or literature-review topic."
        ),
    )

    parser.add_argument(
        "--papers",
        nargs="+",
        required=True,
        help=(
            "Paper IDs to include in the review."
        ),
    )

    parser.add_argument(
        "--title",
        default=(
            "Evidence-Grounded Literature Review"
        ),
        help="Title for the generated review.",
    )

    parser.add_argument(
        "--evidence-per-paper",
        type=int,
        default=8,
        help=(
            "Maximum comparative evidence "
            "requested per paper."
        ),
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help=(
            "Optional Markdown output path. "
            "If omitted, a timestamped file is "
            "created under reports/."
        ),
    )

    return parser


def default_output_path() -> Path:

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    return (
        DEFAULT_REPORTS_DIR
        / (
            "literature_review_"
            f"{timestamp}.md"
        )
    )


def write_report(
    content: str,
    output_path: Path,
) -> Path:

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        content,
        encoding="utf-8",
    )

    return output_path


def main() -> None:

    parser = build_parser()

    args = parser.parse_args()

    service = (
        LiteratureReviewService()
    )

    review = service.generate(
        query=args.query,
        paper_ids=args.papers,
        title=args.title,
        evidence_per_paper=(
            args.evidence_per_paper
        ),
    )

    renderer = (
        LiteratureReviewMarkdownRenderer()
    )

    markdown = renderer.render(
        review
    )

    output_path = (
        args.output
        if args.output is not None
        else default_output_path()
    )

    saved_path = write_report(
        content=markdown,
        output_path=output_path,
    )

    print("=" * 70)
    print(
        "Evidence-Grounded Literature Review"
    )
    print("=" * 70)

    print(
        f"Query: {review.query}"
    )

    print(
        f"Papers: {len(review.paper_ids)}"
    )

    print(
        "Grounding valid: "
        f"{review.validation.valid if review.validation else 'Not run'}"
    )

    print(
        f"Sections: {len(review.sections)}"
    )

    print(
        f"Report: {saved_path}"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()