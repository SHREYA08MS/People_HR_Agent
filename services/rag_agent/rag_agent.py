import os
from dotenv import load_dotenv

load_dotenv()

# API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USE_PINECONE = os.getenv("USE_PINECONE", "false").lower() == "true"
INDEX_NAME = os.getenv("VECTOR_INDEX_NAME", "hr-index")

# LangChain (old compatible imports)
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma, Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA


# ----------------------------
# Load Vector Store
# ----------------------------
def get_vectorstore():
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    if USE_PINECONE and os.getenv("PINECONE_API_KEY"):
        import pinecone

        pinecone.init(
            api_key=os.getenv("PINECONE_API_KEY"),
            environment=os.getenv("PINECONE_ENV"),
        )

        return Pinecone.from_existing_index(INDEX_NAME, embeddings)

    # Local Chroma
    persist_dir = "./data/chroma"
    return Chroma(persist_directory=persist_dir, embedding_function=embeddings)


# ----------------------------
# Build QA Chain
# ----------------------------
def build_qa_chain():
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model="gpt-4o-mini",
        temperature=0.0
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False   # avoid failures
    )

    return qa


# Global chain instance
qa_chain = None


def init_rag():
    global qa_chain
    qa_chain = build_qa_chain()


def answer_question(question: str) -> str:
    global qa_chain
    if qa_chain is None:
        init_rag()

    try:
        result = qa_chain.run(question)
    except Exception as e:
        print("RAG ERROR:", e)
        return "Sorry, I couldn't find any HR information."

    return result
