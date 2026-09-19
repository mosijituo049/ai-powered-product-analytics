from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

from ai.rag.loader import load_documents


def chunk_documents(documents: list[dict]) -> list[dict]:
    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("##", "section"),
        ],
        strip_headers=False,
    )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )

    chunks = []

    for document in documents:
        sections = header_splitter.split_text(document["content"])

        for section in sections:
            section_chunks = text_splitter.split_text(section.page_content)

            for text in section_chunks:
                chunks.append(
                    {
                        "source": document["source"],
                        "section": section.metadata.get("section"),
                        "content": text,
                    }
                )

    return chunks


if __name__ == "__main__":
    documents = load_documents()
    chunks = chunk_documents(documents)

    print(f"Loaded documents: {len(documents)}")
    print(f"Created chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks):
        print(
            f"\n--- chunk {index} | "
            f"{chunk['source']} | "
            f"{chunk['section']} ---"
        )
        print(chunk["content"][:500])