from ai.rag.retriever import retrieve
from ai.rag.vector_store import load_embeddings


def search_project_knowledge(
    query: str,
    top_k: int = 3,
) -> dict:
    embedded_chunks = load_embeddings()

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