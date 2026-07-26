from langchain_ollama import OllamaEmbeddings


class EmbeddingModel:

    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            model="nomic-embed-text"
        )

    def get_embeddings(self):
        return self.embeddings