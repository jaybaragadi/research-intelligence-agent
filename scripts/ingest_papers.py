from src.ingestion.pipeline import run_ingestion


def main() -> None:
    print("=" * 70)
    print("Research Intelligence Agent")
    print("Phase 2 - PDF Ingestion")
    print("=" * 70)

    summary = run_ingestion()

    print("=" * 70)
    print("Ingestion Summary")
    print("=" * 70)

    print(f"Discovered : {summary.discovered}")

    print(f"Successful : {summary.successful}")

    print(f"Failed     : {summary.failed}")


if __name__ == "__main__":
    main()
