from pathlib import Path
import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field


# Project root:
# research-intelligence-agent/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load environment variables from .env
load_dotenv(PROJECT_ROOT / ".env")


class Settings(BaseModel):
    """Central configuration for the application."""

    app_name: str = os.getenv(
        "APP_NAME",
        "Research Intelligence Agent",
    )

    app_env: str = os.getenv(
        "APP_ENV",
        "development",
    )

    openai_api_key: str | None = os.getenv(
        "OPENAI_API_KEY"
    )

    papers_dir: Path = PROJECT_ROOT / os.getenv(
        "PAPERS_DIR",
        "data/papers",
    )

    processed_dir: Path = PROJECT_ROOT / os.getenv(
        "PROCESSED_DIR",
        "data/processed",
    )

    vector_store_dir: Path = PROJECT_ROOT / os.getenv(
        "VECTOR_STORE_DIR",
        "data/vector_store",
    )

    reports_dir: Path = PROJECT_ROOT / os.getenv(
        "REPORTS_DIR",
        "reports",
    )

    llm_model: str = os.getenv(
        "LLM_MODEL",
        "gpt-4.1-mini",
    )

    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2",
    )

    chunk_size: int = Field(
        default=int(os.getenv("CHUNK_SIZE", "1000")),
        gt=0,
    )

    chunk_overlap: int = Field(
        default=int(os.getenv("CHUNK_OVERLAP", "200")),
        ge=0,
    )

    top_k: int = Field(
        default=int(os.getenv("TOP_K", "5")),
        gt=0,
    )


settings = Settings()


def ensure_directories() -> None:
    """Create runtime directories if they do not already exist."""

    directories = [
        settings.papers_dir,
        settings.processed_dir,
        settings.vector_store_dir,
        settings.reports_dir,
    ]

    for directory in directories:
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )