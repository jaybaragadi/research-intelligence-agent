from src.metadata.pipeline import (
    run_metadata_extraction,
)


def main() -> None:

    print("=" * 70)
    print("Research Intelligence Agent")
    print("Phase 3 - Metadata and Research Structure Extraction")
    print("=" * 70)

    summary = run_metadata_extraction()

    print("=" * 70)
    print("Metadata Extraction Summary")
    print("=" * 70)

    print(f"Discovered : " f"{summary.discovered}")

    print(f"Successful : " f"{summary.successful}")

    print(f"Failed     : " f"{summary.failed}")


if __name__ == "__main__":
    main()
