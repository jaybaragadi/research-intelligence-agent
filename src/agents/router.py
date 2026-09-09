import re

from src.agents.intents import (
    ResearchIntent,
)

from src.agents.models import (
    ResearchAgentRequest,
    RoutedResearchRequest,
)


PAPER_ALIASES = {
    "testpilot": "01_testpilot",

    "chattester": "02_chattester",
    "chat tester": "02_chattester",

    "mutap": "03_mutap",
    "mu tap": "03_mutap",

    "symprompt": "04_symprompt",
    "sym prompt": "04_symprompt",

    "coverup": "05_coverup",
    "cover up": "05_coverup",

    "chatunitest": "06_chatunitest",
    "chat unitest": "06_chatunitest",
    "chat unit test": "06_chatunitest",

    "codamosa": "07_codamosa",
    "coda mosa": "07_codamosa",

    "telpa": "08_telpa",

    "hits": "09_hits",

    "coding before testing": (
        "10_coding_before_testing"
    ),
}


COMPARE_TERMS = (
    "compare",
    "comparison",
    "versus",
    " vs ",
    " vs. ",
    "difference between",
    "differences between",
    "similarities between",
    "contrast",
)


SUMMARY_TERMS = (
    "summarize",
    "summary",
    "summarise",
    "overview of",
    "give me an overview",
)


EVIDENCE_TERMS = (
    "show evidence",
    "get evidence",
    "validate evidence",
    "verify evidence",
    "evidence for",
)


CITATION_TERMS = (
    "cite",
    "citation",
    "generate citation",
    "show citation",
    "format citation",
)


PAPER_ID_PATTERN = re.compile(
    r"\b\d{2}_[a-z0-9_]+\b",
    flags=re.IGNORECASE,
)


EVIDENCE_ID_PATTERN = re.compile(
    r"\b\d{2}_[a-z0-9_]+"
    r"_chunk_\d{4}\b",
    flags=re.IGNORECASE,
)


class ResearchIntentRouter:
    """
    Deterministic router for research-agent
    requests.

    The router does not execute research tools.

    Its responsibilities are:

    1. identify research intent
    2. extract paper IDs
    3. resolve known paper aliases
    4. extract evidence IDs
    5. identify missing required information
    """

    def _normalize(
        self,
        text: str,
    ) -> str:
        """
        Normalize whitespace and case for
        deterministic matching.
        """

        return re.sub(
            r"\s+",
            " ",
            text.strip().lower(),
        )

    def _extract_explicit_paper_ids(
        self,
        text: str,
    ) -> list[str]:
        """
        Extract canonical IDs such as:

        03_mutap
        05_coverup
        08_telpa
        """

        matches = (
            PAPER_ID_PATTERN.findall(
                text
            )
        )

        return list(
            dict.fromkeys(
                match.lower()
                for match in matches
            )
        )

    

    def _extract_alias_paper_ids(
        self,
        text: str,
    ) -> list[str]:
        """
        Resolve human-friendly corpus names
        such as:

        MuTAP
        CoverUp
        TELPA

        Paper IDs are returned in the same order
        that their aliases appear in the query.
        """

        normalized = (
            self._normalize(
                text
            )
        )

        matches: list[
            tuple[int, str]
        ] = []

        # Long aliases are still checked first so
        # overlapping aliases such as
        # "chat unit test" and "chatunitest"
        # are handled safely.
        sorted_aliases = sorted(
            PAPER_ALIASES.items(),
            key=lambda item: len(
                item[0]
            ),
            reverse=True,
        )

        for alias, paper_id in (
            sorted_aliases
        ):

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(
                    alias
                )
                + r"(?![a-z0-9])"
            )

            match = re.search(
                pattern,
                normalized,
            )

            if match is not None:
                matches.append(
                    (
                        match.start(),
                        paper_id,
                    )
                )

        # Restore the order used in the user's
        # actual query.
        matches.sort(
            key=lambda item: item[0]
        )

        ordered_ids = [
            paper_id
            for _, paper_id
            in matches
        ]

        return list(
            dict.fromkeys(
                ordered_ids
            )
        )


    def _extract_paper_ids(
        self,
        request: ResearchAgentRequest,
    ) -> list[str]:
        """
        Combine explicitly supplied IDs,
        IDs mentioned in text, and known
        paper-name aliases.
        """

        supplied = [
            paper_id.strip().lower()

            for paper_id
            in request.paper_ids

            if paper_id.strip()
        ]

        explicit = (
            self._extract_explicit_paper_ids(
                request.query
            )
        )

        aliases = (
            self._extract_alias_paper_ids(
                request.query
            )
        )

        return list(
            dict.fromkeys(
                supplied
                + explicit
                + aliases
            )
        )

    def _extract_evidence_id(
        self,
        request: ResearchAgentRequest,
    ) -> str | None:
        """
        Resolve an explicitly supplied evidence
        ID or extract one from the natural-
        language query.
        """

        if (
            request.evidence_id
            and request.evidence_id.strip()
        ):
            return (
                request.evidence_id
                .strip()
                .lower()
            )

        match = (
            EVIDENCE_ID_PATTERN.search(
                request.query
            )
        )

        if match is None:
            return None

        return (
            match.group(0)
            .lower()
        )

    def _contains_any(
        self,
        text: str,
        terms: tuple[str, ...],
    ) -> bool:
        """
        Return True if any routing phrase is
        present.
        """

        normalized = (
            self._normalize(
                text
            )
        )

        return any(
            term.strip()
            in normalized

            for term
            in terms
        )

    def route(
        self,
        request: ResearchAgentRequest,
    ) -> RoutedResearchRequest:
        """
        Convert one raw request into a
        structured routing decision.
        """

        query = (
            request.query.strip()
        )

        if not query:

            return RoutedResearchRequest(
                original_query=(
                    request.query
                ),

                intent=(
                    ResearchIntent.UNKNOWN
                ),

                confidence=0.0,

                reason=(
                    "The research query is empty."
                ),

                needs_clarification=True,

                missing_fields=[
                    "query"
                ],
            )

        paper_ids = (
            self._extract_paper_ids(
                request
            )
        )

        evidence_id = (
            self._extract_evidence_id(
                request
            )
        )

        # -------------------------------------------------
        # Citation intent
        # -------------------------------------------------

        if self._contains_any(
            query,
            CITATION_TERMS,
        ):

            if evidence_id is None:

                return RoutedResearchRequest(
                    original_query=query,

                    intent=(
                        ResearchIntent.CITATION
                    ),

                    paper_ids=paper_ids,

                    confidence=0.95,

                    reason=(
                        "Citation language was "
                        "detected, but no evidence "
                        "ID was supplied."
                    ),

                    needs_clarification=True,

                    missing_fields=[
                        "evidence_id"
                    ],
                )

            return RoutedResearchRequest(
                original_query=query,

                intent=(
                    ResearchIntent.CITATION
                ),

                paper_ids=paper_ids,

                evidence_id=(
                    evidence_id
                ),

                confidence=0.99,

                reason=(
                    "Citation language and an "
                    "evidence ID were detected."
                ),
            )

        # -------------------------------------------------
        # Evidence intent
        # -------------------------------------------------

        if self._contains_any(
            query,
            EVIDENCE_TERMS,
        ):

            if evidence_id is None:

                return RoutedResearchRequest(
                    original_query=query,

                    intent=(
                        ResearchIntent.EVIDENCE
                    ),

                    paper_ids=paper_ids,

                    confidence=0.95,

                    reason=(
                        "Evidence language was "
                        "detected, but no evidence "
                        "ID was supplied."
                    ),

                    needs_clarification=True,

                    missing_fields=[
                        "evidence_id"
                    ],
                )

            return RoutedResearchRequest(
                original_query=query,

                intent=(
                    ResearchIntent.EVIDENCE
                ),

                paper_ids=paper_ids,

                evidence_id=(
                    evidence_id
                ),

                confidence=0.99,

                reason=(
                    "Evidence language and an "
                    "evidence ID were detected."
                ),
            )

        # -------------------------------------------------
        # Comparison intent
        # -------------------------------------------------

        if self._contains_any(
            query,
            COMPARE_TERMS,
        ):

            missing_fields: list[
                str
            ] = []

            if len(paper_ids) < 2:

                missing_fields.append(
                    "at_least_two_paper_ids"
                )

            return RoutedResearchRequest(
                original_query=query,

                intent=(
                    ResearchIntent.COMPARE
                ),

                paper_ids=paper_ids,

                evidence_id=(
                    evidence_id
                ),

                confidence=0.98,

                reason=(
                    "Comparison language was "
                    "detected."
                ),

                needs_clarification=bool(
                    missing_fields
                ),

                missing_fields=(
                    missing_fields
                ),
            )

        # -------------------------------------------------
        # Summary intent
        # -------------------------------------------------

        if self._contains_any(
            query,
            SUMMARY_TERMS,
        ):

            missing_fields = []

            if not paper_ids:

                missing_fields.append(
                    "paper_id"
                )

            return RoutedResearchRequest(
                original_query=query,

                intent=(
                    ResearchIntent.SUMMARIZE
                ),

                paper_ids=paper_ids,

                evidence_id=(
                    evidence_id
                ),

                confidence=0.98,

                reason=(
                    "Summary language was "
                    "detected."
                ),

                needs_clarification=bool(
                    missing_fields
                ),

                missing_fields=(
                    missing_fields
                ),
            )

        # -------------------------------------------------
        # Explicit evidence ID by itself
        # -------------------------------------------------

        if evidence_id is not None:

            return RoutedResearchRequest(
                original_query=query,

                intent=(
                    ResearchIntent.EVIDENCE
                ),

                paper_ids=paper_ids,

                evidence_id=(
                    evidence_id
                ),

                confidence=0.90,

                reason=(
                    "An evidence ID was detected "
                    "without another explicit "
                    "research intent."
                ),
            )

        # -------------------------------------------------
        # Default research behavior
        # -------------------------------------------------

        return RoutedResearchRequest(
            original_query=query,

            intent=(
                ResearchIntent.SEARCH
            ),

            paper_ids=paper_ids,

            confidence=0.80,

            reason=(
                "No specialized command was "
                "detected, so the request is "
                "treated as a research search."
            ),
        )


def route_research_request(
    query: str,
) -> RoutedResearchRequest:
    """
    Convenience wrapper for simple callers.
    """

    router = (
        ResearchIntentRouter()
    )

    request = (
        ResearchAgentRequest(
            query=query
        )
    )

    return router.route(
        request
    )