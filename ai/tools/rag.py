from ai.llm import get_llm_provider
from ai.rag.embedding import embed_chunks
from ai.rag.loader import load_documents
from ai.rag.chunker import chunk_documents
from ai.rag.retriever import retrieve
from ai.rag.vector_store import (
    load_embeddings,
    save_embeddings,
)


def get_project_embeddings(
    embedding_model: str,
) -> list[dict]:

    embedded_chunks = load_embeddings(embedding_model)

    if embedded_chunks:
        return embedded_chunks

    print(
        f"No vector store found for "
        f"{embedding_model}. Generating embeddings..."
    )

    documents = load_documents()

    if not documents:
        raise ValueError(
            "No knowledge documents found in ai/knowledge."
        )

    chunks = chunk_documents(documents)

    if not chunks:
        raise ValueError(
            "Knowledge documents were found, "
            "but no chunks were generated."
        )

    embedded_chunks = embed_chunks(chunks)

    save_embeddings(
        embedded_chunks,
        embedding_model,
    )

    return embedded_chunks


def search_project_knowledge(
    query: str,
    top_k: int = 3,
) -> dict:

    provider = get_llm_provider()
    embedding_model = provider.embedding_model_name

    embedded_chunks = get_project_embeddings(
        embedding_model
    )

    results = retrieve(
        query,
        embedded_chunks,
        top_k=top_k,
    )

    return {
        "results": [
            {
                "source": result["source"],
                "section": result["section"],
                "content": result["content"],
                "similarity": round(
                    result["similarity"],
                    4,
                ),
            }
            for result in results
        ]
    }

if __name__ == "__main__":
    query = "Why do users abandon checkout?"

    result = search_project_knowledge(
        query,
        top_k=3,
    )

    print("\nQuery:")
    print(query)

    print("\nResults:")

    for index, item in enumerate(
        result["results"],
        start=1,
    ):
        print(f"\n--- Result {index} ---")
        print(f"Similarity: {item['similarity']}")
        print(f"Source: {item['source']}")
        print(f"Section: {item['section']}")
        print(f"Content: {item['content'][:500]}")