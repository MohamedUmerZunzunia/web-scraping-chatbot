from fastapi import APIRouter
from pydantic import BaseModel
from app.services.text_splitter import TextChunker
from app.services.scraper import WebScraper
from app.services.vector_store import VectorStore
from app.ai.chatbot import WebChatbot
from app.models.schemas import URLRequest, ChatRequest

router = APIRouter()


class URLRequest(BaseModel):
    url: str


@router.get("/health")
def health():
    return {"status": "OK"}



@router.post("/scrape")
def scrape_website(request: URLRequest):

    scraper = WebScraper()

    result = scraper.scrape(request.url)

    if not result["success"]:
        return result

    chunker = TextChunker()

    chunks = chunker.split(result["content"])

    vector_store = VectorStore()

    vector_store.add_documents(chunks)

    return {
        "title": result["title"],
        "chunks_created": len(chunks),
        "vectors_in_db": vector_store.count()
    }

@router.post("/chat")
def chat(request: ChatRequest):

    chatbot = WebChatbot()

    return chatbot.ask(request.question)