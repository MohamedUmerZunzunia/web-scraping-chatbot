from pydantic import BaseModel


class URLRequest(BaseModel):
    url: str


class ChatRequest(BaseModel):
    question: str