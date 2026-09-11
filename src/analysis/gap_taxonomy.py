from dataclasses import dataclass

from src.analysis.gap_models import (
    GapSignalType,
)


@dataclass(frozen=True)
class GapSignalDefinition:
    """
    Definition of one explicit research-gap
    signal category.

    Strong phrases are preferred over broad
    individual keywords to reduce false positives.
    """

    signal_type: GapSignalType

    description: str

    phrases: tuple[str, ...]

    preferred_sections: tuple[str, ...] = ()


GAP_SIGNAL_DEFINITIONS = (
    GapSignalDefinition(
        signal_type=(GapSignalType.LIMITATION),
        description=(
            "The paper explicitly reports a "
            "limitation, weakness, constraint, "
            "or threat affecting the proposed "
            "method or study."
        ),
        phrases=(
            "limitation of our approach",
            "limitations of our approach",
            "limitation of our method",
            "limitations of our method",
            "limitation of our study",
            "limitations of our study",
            "our approach is limited",
            "our method is limited",
            "our study is limited",
            "threat to validity",
            "threats to validity",
            "drawback of our approach",
            "drawbacks of our approach",
            "drawback of the approach",
            "drawbacks of the approach",
        ),
        preferred_sections=(
            "limitations",
            "discussion",
            "threats",
            "threats_to_validity",
        ),
    ),
    GapSignalDefinition(
        signal_type=(GapSignalType.FUTURE_WORK),
        description=(
            "The paper explicitly identifies "
            "future research or an extension "
            "that remains to be investigated."
        ),
        phrases=(
            "future work",
            "future research",
            "in future work",
            "in future research",
            "left for future work",
            "we plan to investigate",
            "we intend to investigate",
            "we plan to explore",
            "we intend to explore",
            "an area of future work",
            "directions for future work",
        ),
        preferred_sections=(
            "conclusion",
            "conclusions",
            "discussion",
            "future_work",
        ),
    ),
    GapSignalDefinition(
        signal_type=(GapSignalType.UNRESOLVED_PROBLEM),
        description=(
            "The paper explicitly describes an "
            "open, unresolved, or still difficult "
            "research problem."
        ),
        phrases=(
            "remains an open problem",
            "remains a challenge",
            "remains challenging",
            "still remains challenging",
            "has not been addressed",
            "have not been addressed",
            "has not been explored",
            "have not been explored",
            "has not been investigated",
            "have not been investigated",
            "little attention has been paid",
            "few studies have examined",
            "few studies have investigated",
            "underexplored",
            "under-explored",
        ),
        preferred_sections=(
            "introduction",
            "background",
            "discussion",
            "conclusion",
            "conclusions",
        ),
    ),
)


def get_gap_signal_definition(
    signal_type: GapSignalType,
) -> GapSignalDefinition:
    """
    Return the taxonomy definition associated
    with one signal type.
    """

    for definition in GAP_SIGNAL_DEFINITIONS:

        if definition.signal_type == signal_type:

            return definition

    raise ValueError("Unsupported gap signal type: " f"{signal_type}")
