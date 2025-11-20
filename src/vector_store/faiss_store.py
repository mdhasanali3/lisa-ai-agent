import os
from pathlib import Path
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

from src.knowledge_base.insurance_data import get_knowledge_base


class InsuranceVectorStore:
    """Manages FAISS vector store for life insurance knowledge base."""

    def __init__(self, embedding_model: str = "text-embedding-3-small", persist_directory: str = "./data/vector_store"):
        """
        Initialize the vector store.

        Args:
            embedding_model: OpenAI embedding model name
            persist_directory: Directory to persist the FAISS index
        """
        self.embedding_model = embedding_model
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.vector_store = None

    def initialize_store(self) -> FAISS:
        """
        Initialize or load the FAISS vector store.

        Returns:
            FAISS vector store instance
        """
        # Check if persisted store exists
        if os.path.exists(self.persist_directory):
            print(f"Loading existing vector store from {self.persist_directory}")
            self.vector_store = FAISS.load_local(
                self.persist_directory,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            print("Creating new vector store from knowledge base...")
            self._create_and_persist_store()

        return self.vector_store

    def _create_and_persist_store(self):
        """Create a new vector store from the knowledge base and persist it."""
        # Load knowledge base
        knowledge_data = get_knowledge_base()

        # Convert to LangChain documents
        documents = [
            Document(
                page_content=item["content"],
                metadata={"category": item["category"]}
            )
            for item in knowledge_data
        ]

        # Create FAISS vector store
        self.vector_store = FAISS.from_documents(documents, self.embeddings)

        # Persist to disk
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
        self.vector_store.save_local(self.persist_directory)
        print(f"Vector store created and saved to {self.persist_directory}")

    def search(self, query: str, top_k: int = 3) -> List[Document]:
        """
        Search the vector store for relevant documents.

        Args:
            query: User query
            top_k: Number of top results to return

        Returns:
            List of relevant documents
        """
        if self.vector_store is None:
            self.initialize_store()

        return self.vector_store.similarity_search(query, k=top_k)

    def search_with_scores(self, query: str, top_k: int = 3) -> List[tuple[Document, float]]:
        """
        Search the vector store and return documents with relevance scores.

        Args:
            query: User query
            top_k: Number of top results to return

        Returns:
            List of (document, score) tuples
        """
        if self.vector_store is None:
            self.initialize_store()

        return self.vector_store.similarity_search_with_score(query, k=top_k)

    def rebuild_store(self):
        """Rebuild the vector store from scratch (useful for updates)."""
        print("Rebuilding vector store...")
        self._create_and_persist_store()
        print("Vector store rebuilt successfully")
