from pathlib import Path


KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"


def load_documents() -> list[dict]:
    documents = []

    for file_path in KNOWLEDGE_DIR.glob("*.md"):
        text = file_path.read_text(encoding="utf-8")

        documents.append(
            {
                "source": file_path.name,
                "content": text,
            }
        )

    return documents


if __name__ == "__main__":
    documents = load_documents()

    print(f"Loaded {len(documents)} documents")

    for document in documents:
        print(f"\n--- {document['source']} ---")
        print(document["content"][:300])