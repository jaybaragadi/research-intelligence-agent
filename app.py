from src.config import ensure_directories, settings


def print_banner() -> None:
    """Print basic project information."""

    print("=" * 70)
    print(settings.app_name)
    print("=" * 70)

    print(f"Environment       : {settings.app_env}")
    print(f"LLM model         : {settings.llm_model}")
    print(f"Embedding model   : {settings.embedding_model}")
    print(f"Chunk size        : {settings.chunk_size}")
    print(f"Chunk overlap     : {settings.chunk_overlap}")
    print(f"Top K             : {settings.top_k}")

    print()

    print(f"Papers directory  : {settings.papers_dir}")
    print(f"Processed data    : {settings.processed_dir}")
    print(f"Vector store      : {settings.vector_store_dir}")
    print(f"Reports directory : {settings.reports_dir}")


def main() -> None:
    """Application entry point."""

    ensure_directories()

    print_banner()

    print()
    print("Project setup successful.")
    print("Research Intelligence Agent is ready for Phase 2.")


if __name__ == "__main__":
    main()