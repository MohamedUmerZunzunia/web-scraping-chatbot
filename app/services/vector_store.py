from langchain_chroma import Chroma

from app.ai.embeddings import EmbeddingModel


class VectorStore:

    def __init__(self):

        embeddings = EmbeddingModel().get_embeddings()

        self.db = Chroma(
            persist_directory="chroma_db",
            embedding_function=embeddings
        )

    def add_documents(self, chunks):

        self.db.add_texts(chunks)

    def similarity_search(self, question, k=5):

        return self.db.similarity_search_with_score(
            question,
            k=k
        )

    def count(self):

        return self.db._collection.count()