from pathlib import Path

from scripts.generate_literature_review import (
    build_parser,
    write_report,
)


def test_parser_accepts_required_arguments():

    parser = build_parser()

    args = parser.parse_args(
        [
            "Review LLM testing.",
            "--papers",
            "03_mutap",
            "05_coverup",
        ]
    )

    assert (
        args.query
        == "Review LLM testing."
    )

    assert args.papers == [
        "03_mutap",
        "05_coverup",
    ]


def test_parser_default_evidence_per_paper():

    parser = build_parser()

    args = parser.parse_args(
        [
            "Review research.",
            "--papers",
            "03_mutap",
            "05_coverup",
        ]
    )

    assert (
        args.evidence_per_paper
        == 8
    )


def test_parser_accepts_custom_title():

    parser = build_parser()

    args = parser.parse_args(
        [
            "Review research.",
            "--papers",
            "03_mutap",
            "05_coverup",
            "--title",
            "Custom Review",
        ]
    )

    assert (
        args.title
        == "Custom Review"
    )


def test_parser_accepts_output_path():

    parser = build_parser()

    args = parser.parse_args(
        [
            "Review research.",
            "--papers",
            "03_mutap",
            "05_coverup",
            "--output",
            "reports/test.md",
        ]
    )

    assert (
        args.output
        == Path(
            "reports/test.md"
        )
    )


def test_write_report_creates_file(
    tmp_path,
):

    output = (
        tmp_path
        / "nested"
        / "review.md"
    )

    result = write_report(
        "# Review\n",
        output,
    )

    assert result == output

    assert (
        output.read_text(
            encoding="utf-8"
        )
        == "# Review\n"
    )