from src.chunking.pipeline import (
    run_chunking,
)


def main() -> None:

    print("=" * 70)
    print("Research Intelligence Agent")
    print("Phase 4 - Structure-Aware Chunking")
    print("=" * 70)

    summary = run_chunking()

    print("=" * 70)
    print("Chunking Summary")
    print("=" * 70)

    print(f"Discovered   : " f"{summary.discovered}")

    print(f"Successful   : " f"{summary.successful}")

    print(f"Failed       : " f"{summary.failed}")

    print(f"Total chunks : " f"{summary.total_chunks}")


if __name__ == "__main__":
    main()
