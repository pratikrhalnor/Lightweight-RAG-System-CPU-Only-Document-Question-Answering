from src.data_loader import load_all_documents
from src.vectorstore import ChromaVectorStore
#from src.vectorstore import FaissVectorStore
from src.search import RAGSearch
import os

if __name__ == "__main__":

    docs = load_all_documents("data")
    store = ChromaVectorStore("chroma_store")
    #store = FaissVectorStore("faiss_store")

    faiss_path = os.path.join("faiss_store", "faiss.index")

    if os.path.exists(faiss_path):
        print("[INFO] Loading existing FAISS index...")
        store.load()
    else:
        print("[INFO] Building FAISS index...")
        store.build_from_documents(docs)

    rag_search = RAGSearch()
    query = "How to connect input card"
    summary = rag_search.search_and_summarize(query, top_k=3)

    print("Summary:", summary)