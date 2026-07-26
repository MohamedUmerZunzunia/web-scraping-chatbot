import ollama

from app.services.vector_store import VectorStore


class WebChatbot:

    def __init__(self):

        self.vector_store = VectorStore()

    def ask(self, question: str):

        docs = self.vector_store.similarity_search(
        question
)

        context = "\n\n".join(
            [doc.page_content for doc, score in docs]
        )

        prompt = f"""
You are an AI assistant.

Answer the user's question using ONLY the context below.

If the answer exists in the context, answer it directly.

If the answer is not present, reply exactly:

I couldn't find that information on the website.

Context:
{context}

Question:
{question}
"""

        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return {
            "answer": response["message"]["content"],
            "sources": [doc.page_content for doc, score in docs]
        }