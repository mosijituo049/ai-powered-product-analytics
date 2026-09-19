import requests

from ai.rag.loader import load_documents
from ai.rag.chunker import chunk_documents
from ai.rag.vector_store import save_embeddings


OLLAMA_URL = "http://localhost:11434/api/embed"
MODEL_NAME = "nomic-embed-text"


def embed_texts(texts: list[str]) -> list[list[float]]:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "input": texts,
        },
        timeout=120,
    )

    response.raise_for_status()

    data = response.json()

    return data["embeddings"]


def embed_chunks(chunks: list[dict]) -> list[dict]:
    texts = [chunk["content"] for chunk in chunks]

    embeddings = embed_texts(texts)

    embedded_chunks = []

    for chunk, embedding in zip(chunks, embeddings):
        embedded_chunks.append(
            {
                **chunk,
                "embedding": embedding,
            }
        )

    return embedded_chunks

if __name__ == "__main__":
    documents = load_documents()
    chunks = chunk_documents(documents)

    embedded_chunks = embed_chunks(chunks)

    save_embeddings(embedded_chunks)

    print(f"Chunks: {len(embedded_chunks)}")
    print(
        f"Vector dimensions: "
        f"{len(embedded_chunks[0]['embedding'])}"
    )
    print(
        f"Saved to: "
        f"rag_embeddings.json"
    )