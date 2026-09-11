import pytest

from src.analysis.gap_models import (
    GapSignalType,
)
from src.analysis.gap_taxonomy import (
    GAP_SIGNAL_DEFINITIONS,
    get_gap_signal_definition,
)


def test_taxonomy_contains_explicit_signal_types():

    signal_types = {definition.signal_type for definition in GAP_SIGNAL_DEFINITIONS}

    assert GapSignalType.LIMITATION in signal_types

    assert GapSignalType.FUTURE_WORK in signal_types

    assert GapSignalType.UNRESOLVED_PROBLEM in signal_types


def test_future_work_has_strong_phrases():

    definition = get_gap_signal_definition(GapSignalType.FUTURE_WORK)

    assert "future work" in definition.phrases

    assert "we plan to investigate" in definition.phrases


def test_limitation_has_preferred_sections():

    definition = get_gap_signal_definition(GapSignalType.LIMITATION)

    assert "limitations" in definition.preferred_sections

    assert "discussion" in definition.preferred_sections


def test_unknown_taxonomy_type_raises():

    with pytest.raises(ValueError):

        get_gap_signal_definition("unsupported")  # type: ignore[arg-type]
