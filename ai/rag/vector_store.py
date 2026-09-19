import json
from pathlib import Path


VECTOR_STORE_PATH = (
    Path(__file__).resolve().parents[2]
    / "outputs"
    / "rag_embeddings.json"
)


def save_embeddings(embedded_chunks: list[dict]) -> None:
    VECTOR_STORE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        VECTOR_STORE_PATH,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            embedded_chunks,
            file,
            ensure_ascii=False,
        )


def load_embeddings() -> list[dict]:
    if not VECTOR_STORE_PATH.exists():
        raise FileNotFoundError(
            f"Vector store not found: {VECTOR_STORE_PATH}"
        )

    with open(
        VECTOR_STORE_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)