from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

class ChromaVectorStore:
    def __init__(self, persist_dir="chroma_store", embedding_model="all-MiniLM-L6-v2"):
        self.persist_dir = persist_dir
        os.makedirs(self.persist_dir, exist_ok=True)

        self.embedding = HuggingFaceEmbeddings(
            model_name=embedding_model
        )

        self.db = None

    def build_from_documents(self, documents):
        print(f"[INFO] Building ChromaDB from {len(documents)} docs...")

        texts = [doc.page_content for doc in documents]

        self.db = Chroma.from_texts(
            texts=texts,
            embedding=self.embedding,
            persist_directory=self.persist_dir
        )

        self.db.persist()
        print("[INFO] ChromaDB saved.")

    def load(self):
        self.db = Chroma(
            persist_directory=self.persist_dir,
            embedding_function=self.embedding
        )
        print("[INFO] ChromaDB loaded.")

    def query(self, query_text, top_k=5):
        docs = self.db.similarity_search(query_text, k=top_k)

        results = []
        for doc in docs:
            results.append({
                "metadata": {"text": doc.page_content}
            })

        return results