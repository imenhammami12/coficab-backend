from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from app.rag.vectorstore import get_vectorstore

SYSTEM_PROMPT = """Tu es l'assistant virtuel officiel de Coficab, une entreprise leader dans la fabrication de câbles automobiles.
Réponds aux questions en te basant UNIQUEMENT sur le contexte fourni ci-dessous, extrait du site web de Coficab.
Si l'information n'est pas dans le contexte, dis clairement que tu ne disposes pas de cette information.
Réponds en français, de manière claire et professionnelle.

Contexte :
{context}

Question : {question}
"""

_llm = None


def get_llm():
    global _llm
    if _llm is None:
        _llm = ChatOllama(model="llama3.2", temperature=0.3)
    return _llm


def ask_chatbot(question: str, k: int = 4) -> dict:
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search(question, k=k)

    context = "\n\n".join([f"[{doc.metadata.get('title', 'Source')}]: {doc.page_content}" for doc in results])

    prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)
    chain = prompt | get_llm()

    response = chain.invoke({"context": context, "question": question})

    sources = list({doc.metadata.get("source") for doc in results})

    return {
        "answer": response.content,
        "sources": sources,
    }