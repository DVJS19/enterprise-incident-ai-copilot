from pathlib import Path

from services.rag.chunker import load_knowledge_base_chunks
from services.rag.embeddings import EmbeddingModel
from services.rag.vector_store import SearchResult, VectorStore


class LocalRAGRetriever:
    def __init__(self, knowledge_base_dir: Path) -> None:
        self.knowledge_base_dir = knowledge_base_dir
        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore()
        self._is_indexed = False

    def build_index(self) -> None:
        chunks = load_knowledge_base_chunks(self.knowledge_base_dir)

        if not chunks:
            self._is_indexed = True
            return

        vectors = self.embedding_model.embed_corpus(
            [chunk.text for chunk in chunks]
        )

        self.vector_store.index(
            chunks=chunks,
            vectors=vectors,
        )

        self._is_indexed = True

    def search(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[SearchResult]:
        if not self._is_indexed:
            self.build_index()

        query_vector = self.embedding_model.embed_query(query)

        return self.vector_store.search(
            query_vector=query_vector,
            top_k=top_k,
        )