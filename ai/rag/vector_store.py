import json
from pathlib import Path


OUTPUT_DIR = Path("outputs")


def get_vector_store_path(embedding_model: str) -> Path:
    safe_model_name = embedding_model.replace("/", "_")
    return OUTPUT_DIR / f"rag_embeddings_{safe_model_name}.json"


def save_embeddings(
    embedded_chunks: list[dict],
    embedding_model: str,
) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    path = get_vector_store_path(embedding_model)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(embedded_chunks, f, ensure_ascii=False)

    print(f"Saved to: {path}")


def load_embeddings(embedding_model: str) -> list[dict]:
    path = get_vector_store_path(embedding_model)

    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)