import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
COLLECTION_NAME = "coficab_knowledge"

_embeddings = None


def get_embeddings():
    global _embeddings
    if _embeddings is None:
        # Modèle léger, multilingue (gère bien le français et l'anglais)
        _embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    return _embeddings


def get_vectorstore() -> Chroma:
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=CHROMA_DIR,
    )

def build_vectorstore(pages: list[dict]) -> int:
    """Découpe les pages scrapées en chunks et les indexe dans ChromaDB, par lots."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)

    documents = []
    for page in pages:
        chunks = splitter.split_text(page["content"])
        for chunk in chunks:
            documents.append(
                Document(
                    page_content=chunk,
                    metadata={"source": page["url"], "title": page["title"]},
                )
            )

    vectorstore = get_vectorstore()

    BATCH_SIZE = 4000
    total = 0
    for i in range(0, len(documents), BATCH_SIZE):
        batch = documents[i : i + BATCH_SIZE]
        vectorstore.add_documents(batch)
        total += len(batch)
        print(f"  → {total}/{len(documents)} chunks indexés...")

    return total