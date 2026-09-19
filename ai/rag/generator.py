from ai.llm import get_llm_provider
from ai.rag.retriever import retrieve
from ai.rag.vector_store import load_embeddings,save_embeddings
from ai.prompts import RAG_CONTEXT_INSTRUCTION
from ai.rag.embedding import embed_chunks
from ai.rag.loader import load_documents
from ai.rag.chunker import chunk_documents

def get_embeddings(embedding_model: str) -> list[dict]:
    embedded_chunks = load_embeddings(embedding_model)

    if embedded_chunks:
        return embedded_chunks

    documents = load_documents()
    chunks = chunk_documents(documents)
    embedded_chunks = embed_chunks(chunks)

    save_embeddings(
        embedded_chunks,
        embedding_model,
    )

    return embedded_chunks

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
    provider = get_llm_provider()
    embedding_model = provider.embedding_model_name

    embedded_chunks = get_embeddings(embedding_model)

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

    return provider.generate(prompt)


if __name__ == "__main__":
    question = "What is the checkout abandonment rate?"

    answer = generate_answer(question)

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(answer)