from src.generation.evidence_package import (
    EvidencePackageBuilder,
)
from src.tools.compare_papers import (
    ComparisonEvidence,
    PaperComparisonEntry,
    PaperComparisonResponse,
)
from src.tools.evidence_tool import (
    EvidenceRecord,
)
from src.tools.search_papers import (
    PaperSearchResponse,
    PaperSearchResult,
)


class FakeEvidenceTool:

    def get(
        self,
        evidence_id: str,
    ):

        return EvidenceRecord(
            evidence_id=evidence_id,
            chunk_id=evidence_id,
            paper_id=(evidence_id.split("_chunk_")[0]),
            page_number=3,
            section="methodology",
            text=(f"Validated text for " f"{evidence_id}"),
        )


class FakeCitation:

    def __init__(
        self,
        citation_text: str,
    ):
        self.citation_text = citation_text


class FakeCitationTool:

    def cite(
        self,
        evidence_id: str,
    ):

        return FakeCitation(citation_text=(f"Citation for {evidence_id}"))


def build_builder():

    return EvidencePackageBuilder(
        evidence_tool=(FakeEvidenceTool()),
        citation_tool=(FakeCitationTool()),
    )


def make_search_result(
    chunk_id: str,
    rank: int,
):

    return PaperSearchResult(
        rank=rank,
        paper_id=(chunk_id.split("_chunk_")[0]),
        page_number=3,
        section="methodology",
        score=0.9,
        raw_score=0.8,
        lexical_score=0.7,
        chunk_id=chunk_id,
        text="retrieval copy",
    )


def test_builds_package_from_search():

    response = PaperSearchResponse(
        query="feedback",
        result_count=2,
        results=[
            make_search_result(
                "08_telpa_chunk_0040",
                1,
            ),
            make_search_result(
                "05_coverup_chunk_0017",
                2,
            ),
        ],
    )

    package = build_builder().from_search(response)

    assert package.query == "feedback"

    assert len(package.evidence) == 2

    assert package.evidence[0].label == "E1"

    assert package.evidence[1].label == "E2"


def test_search_package_uses_validated_text():

    response = PaperSearchResponse(
        query="feedback",
        result_count=1,
        results=[
            make_search_result(
                "08_telpa_chunk_0040",
                1,
            )
        ],
    )

    package = build_builder().from_search(response)

    assert package.evidence[0].text == ("Validated text for " "08_telpa_chunk_0040")


def test_search_package_removes_duplicates():

    result = make_search_result(
        "08_telpa_chunk_0040",
        1,
    )

    response = PaperSearchResponse(
        query="feedback",
        result_count=2,
        results=[
            result,
            result,
        ],
    )

    package = build_builder().from_search(response)

    assert len(package.evidence) == 1


def test_builds_package_from_comparison():

    evidence_one = ComparisonEvidence(
        rank=1,
        paper_id="03_mutap",
        page_number=3,
        section="methodology",
        score=0.9,
        raw_score=0.8,
        lexical_score=0.7,
        chunk_id=("03_mutap_chunk_0001"),
        text="MuTAP evidence",
    )

    evidence_two = ComparisonEvidence(
        rank=1,
        paper_id="05_coverup",
        page_number=4,
        section="methodology",
        score=0.9,
        raw_score=0.8,
        lexical_score=0.7,
        chunk_id=("05_coverup_chunk_0017"),
        text="CoverUp evidence",
    )

    response = PaperComparisonResponse(
        query=("Compare feedback"),
        requested_papers=[
            "03_mutap",
            "05_coverup",
        ],
        matched_papers=[
            "03_mutap",
            "05_coverup",
        ],
        missing_papers=[],
        comparisons=[
            PaperComparisonEntry(
                paper_id="03_mutap",
                evidence=[evidence_one],
            ),
            PaperComparisonEntry(
                paper_id="05_coverup",
                evidence=[evidence_two],
            ),
        ],
    )

    package = build_builder().from_comparison(response)

    assert len(package.evidence) == 2

    assert package.evidence[0].paper_id == "03_mutap"

    assert package.evidence[1].paper_id == "05_coverup"
