from pathlib import Path

from services.rag.retrieval import LocalRAGRetriever


class RAGService:
    """
    
    A simple RAG (Retrieval-Augmented Generation) service that allows searching
    through a knowledge base of markdown files. It uses a local retriever to  
    index and search the documents based on their content.
    
    This builds only once when the service is initialized, and then serves search requests using the
    in-memory index.
    """
    def __init__(self) -> None:
        self.retriever = LocalRAGRetriever(
            Path("sample_data/knowledge_base")
        )

        self.retriever.build_index()

    def search(
        self,
        query: str,
        top_k: int = 3,
    ):
        return self.retriever.search(
            query=query,
            top_k=top_k,
        )


rag_service = RAGService()