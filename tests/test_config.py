from src.config import settings


def test_app_name():
    assert settings.app_name == "Research Intelligence Agent"


def test_chunk_size_is_positive():
    assert settings.chunk_size > 0


def test_chunk_overlap_is_valid():
    assert settings.chunk_overlap >= 0


def test_top_k_is_positive():
    assert settings.top_k > 0
