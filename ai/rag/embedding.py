from ai.llm import get_llm_provider
from ai.rag.loader import load_documents
from ai.rag.chunker import chunk_documents
from ai.rag.vector_store import save_embeddings


def embed_texts(texts: list[str]) -> list[list[float]]:
    provider = get_llm_provider()
    return provider.embed(texts)


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

    provider = get_llm_provider()
    embedding_model = provider.embedding_model_name

    save_embeddings(
        embedded_chunks,
        embedding_model,
    )

    print(f"Chunks: {len(embedded_chunks)}")
    print(
        f"Vector dimensions: "
        f"{len(embedded_chunks[0]['embedding'])}"
    )
    print(
        f"Saved to: "
        f"rag_embeddings_{embedding_model}.json"
    )