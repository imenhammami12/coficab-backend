from app.rag.scraper import crawl
from app.rag.vectorstore import build_vectorstore

if __name__ == "__main__":
    print("Démarrage du scraping de coficab.com...")
    pages = crawl()
    print(f"\n{len(pages)} pages récupérées.")

    if pages:
        print("Indexation dans ChromaDB...")
        count = build_vectorstore(pages)
        print(f"\n✅ {count} chunks indexés avec succès dans la base vectorielle.")
    else:
        print("❌ Aucune page récupérée, vérifie ta connexion internet.")