import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Web Scraping Chatbot",
    page_icon="🌐",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    st.info(
        "👋 Scrape a website and ask your first question."
    )

if "website_info" not in st.session_state:
    st.session_state.website_info = None

if "website_loaded" not in st.session_state:
    st.session_state.website_loaded = False
# -----------------------------
# Header
# -----------------------------
st.title("🌐 Web Scraping Chatbot")

st.markdown(
    """
Scrape a website, generate embeddings, store them in ChromaDB,
and chat with the content using a local Llama 3.2 model.
"""
)
st.sidebar.title("🌐 Website Status")

if st.session_state.website_loaded:

    info = st.session_state.website_info

    st.sidebar.success("Website Loaded")

    st.sidebar.markdown(f"### {info['title']}")

    st.sidebar.metric("Chunks", info["chunks"])
    st.sidebar.metric("Vectors", info["vectors"])

 

st.sidebar.markdown("### 🛠 Tech Stack")

st.sidebar.markdown("""
- FastAPI
- Streamlit
- BeautifulSoup
- LangChain
- ChromaDB
- Ollama
""")
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.divider()

# -----------------------------
# Website Scraper
# -----------------------------
website_url = st.text_input(
    "Website URL",
    placeholder="https://python.org"
)

if st.button("Scrape Website"):

    if website_url:

        with st.spinner("Scraping website..."):

            response = requests.post(
                f"{API_URL}/scrape",
                json={"url": website_url}
            )

            data = response.json()

            if data.get("title"):
                st.session_state.messages = []
                st.success("Website processed successfully!")

                st.session_state.website_loaded = True

                st.session_state.website_info = {
                    "title": data["title"],
                     "chunks": data["chunks_created"],
                    "vectors": data["vectors_in_db"]
}
               
                st.rerun()
                
            else:
                st.error(data.get("error"))

st.divider()

# -----------------------------
# Chat Section
# -----------------------------
st.subheader("💬 Ask Questions")

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
question = st.chat_input(
    "Ask a question about the website...",
    disabled=not st.session_state.website_loaded
)

if question:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Get AI response
    with st.spinner("Thinking..."):

        response = requests.post(
            f"{API_URL}/chat",
            json={"question": question}
        )

        data = response.json()

    answer = data["answer"]

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(answer)

        with st.expander("Retrieved Context"):
            for i, source in enumerate(data["sources"], start=1):
                st.markdown(f"**Chunk {i}**")
                st.write(source)