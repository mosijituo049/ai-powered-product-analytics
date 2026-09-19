from ai.llm import get_llm_provider
from ai.rag.retriever import retrieve
from ai.rag.vector_store import load_embeddings
from ai.prompts import RAG_CONTEXT_INSTRUCTION


def build_context(results: list[dict]) -> str:
    context_parts = []

    for index, result in enumerate(results, start=1):
        context_parts.append(
            f"""
            [Source {index}]
            Source: {result["source"]}
            Section: {result["section"]}

            {result["content"]}
            """
        )

    return "\n".join(context_parts)


def generate_answer(question: str, top_k: int = 3) -> str:
    embedded_chunks = load_embeddings()

    results = retrieve(
        question,
        embedded_chunks,
        top_k=top_k,
    )

    context = build_context(results)

    prompt = f"""
    {RAG_CONTEXT_INSTRUCTION}

    Context:
    {context}

    User question:
    {question}

    Answer:
    """

    provider = get_llm_provider()

    return provider.generate(prompt)


if __name__ == "__main__":
    question = "What is the checkout abandonment rate?"

    answer = generate_answer(question)

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(answer)