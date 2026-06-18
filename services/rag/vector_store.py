from dataclasses import dataclass
from typing import Any

from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class SearchResult:
    document_name: str
    chunk_id: str
    score: float
    text: str


class VectorStore:
    """
    In-memory vector store.

    Today:
    - Stores vectors in process memory.
    - Searches using cosine similarity.

    Later:
    - This will be replaced by OpenSearch Serverless vector search.
    """

    def __init__(self) -> None:
        self.chunks: list[Any] = []
        self.vectors: Any = None

    def index(self, chunks: list[Any], vectors: Any) -> None:
        self.chunks = chunks
        self.vectors = vectors

    def search(self, query_vector: Any, top_k: int = 3) -> list[SearchResult]:
        if self.vectors is None or not self.chunks:
            return []

        similarities = cosine_similarity(query_vector, self.vectors)[0]
        ranked_indices = similarities.argsort()[::-1]

        results: list[SearchResult] = []

        for index in ranked_indices[:top_k]:
            chunk = self.chunks[index]

            results.append(
                SearchResult(
                    document_name=chunk.document_name,
                    chunk_id=chunk.chunk_id,
                    score=float(similarities[index]),
                    text=chunk.text,
                )
            )

        return results