import math

from ai.rag.embedding import embed_texts
from ai.rag.vector_store import load_embeddings

def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    norm_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    norm_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)

def retrieve(
    query: str,
    embedded_chunks: list[dict],
    top_k: int = 3,
) -> list[dict]:

    query_embedding = embed_texts([query])[0]

    results = []

    for chunk in embedded_chunks:
        similarity = cosine_similarity(
            query_embedding,
            chunk["embedding"],
        )

        results.append(
            {
                **chunk,
                "similarity": similarity,
            }
        )

    results.sort(
        key=lambda x: x["similarity"],
        reverse=True,
    )

    return results[:top_k]

if __name__ == "__main__":
    embedded_chunks = load_embeddings()

    query = "What is the checkout abandonment rate?"

    results = retrieve(
        query,
        embedded_chunks,
        top_k=3,
    )

    print(f"\nQuery: {query}")

    print("\nTop results:")

    for index, result in enumerate(results, start=1):
        print(f"\n--- Result {index} ---")
        print(
            f"Similarity: "
            f"{result['similarity']:.4f}"
        )
        print(
            f"Source: "
            f"{result['source']}"
        )
        print(
            f"Section: "
            f"{result['section']}"
        )
        print(
            f"Content: "
            f"{result['content'][:300]}"
        )