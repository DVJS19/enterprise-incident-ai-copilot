from sklearn.feature_extraction.text import TfidfVectorizer


class EmbeddingModel:
    """
    Lightweight local embedding model.

    This avoids PyTorch issues on Windows and gives us a vector-search-like
    workflow. Later to replace this with Titan Embeddings or sentence-transformers.
    """

    def __init__(self) -> None:
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
        )

    def embed_corpus(self, texts: list[str]):
        return self.vectorizer.fit_transform(texts)

    def embed_query(self, query: str):
        return self.vectorizer.transform([query])