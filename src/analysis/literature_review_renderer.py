from __future__ import annotations

from src.analysis.literature_review_models import (
    LiteratureReview,
)


class LiteratureReviewMarkdownRenderer:
    """
    Render a validated LiteratureReview as Markdown.

    Rendering is presentation-only:
    it does not retrieve evidence,
    generate findings,
    or alter grounding.
    """

    def render(
        self,
        review: LiteratureReview,
    ) -> str:

        lines: list[str] = []

        lines.append(f"# {review.title}")
        lines.append("")

        lines.append(f"**Research question:** {review.query}")
        lines.append("")

        lines.append(f"**Indexed papers:** " f"{len(review.paper_ids)}")
        lines.append("")

        lines.append("**Corpus:** " + ", ".join(review.paper_ids))
        lines.append("")

        for section in review.sections:

            lines.append(f"## {section.title}")
            lines.append("")

            if section.narrative.strip():

                lines.append(section.narrative.strip())
                lines.append("")

            if section.evidence:

                lines.append("### Supporting Evidence")
                lines.append("")

                for evidence in section.evidence:

                    location = f"p. {evidence.page_number}"

                    if evidence.section:
                        location += f", {evidence.section}"

                    lines.append(
                        f"- **[{evidence.evidence_id}]** "
                        f"`{evidence.paper_id}` — "
                        f"{location}"
                    )

                    lines.append(f"  - {self._clean_text(evidence.text)}")

                    lines.append(f"  - Citation: " f"{evidence.citation_text}")

                lines.append("")

        if review.citations:

            lines.append("## Citation Index")
            lines.append("")

            for number, citation in enumerate(
                review.citations,
                start=1,
            ):
                lines.append(f"{number}. {citation}")

            lines.append("")

        lines.append("## Scope Note")
        lines.append("")

        lines.append(review.corpus_scope_note)
        lines.append("")

        if review.validation is not None:

            lines.append("## Grounding Validation")
            lines.append("")

            lines.append(f"**Valid:** " f"{review.validation.valid}")

            lines.append("")

            lines.append(f"**Issues:** " f"{len(review.validation.issues)}")

            lines.append("")

            if review.validation.issues:

                for issue in review.validation.issues:

                    code = (
                        issue.code.value
                        if hasattr(
                            issue.code,
                            "value",
                        )
                        else str(issue.code)
                    )

                    lines.append(f"- `{code}`: " f"{issue.message}")

                lines.append("")

        return "\n".join(lines).rstrip() + "\n"

    def _clean_text(
        self,
        text: str,
    ) -> str:

        return " ".join(text.split())
