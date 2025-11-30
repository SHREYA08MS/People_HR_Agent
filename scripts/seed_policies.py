# scripts/seed_policies.py
import os
from pathlib import Path
#from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma, Pinecone
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USE_PINE = os.getenv("USE_PINECONE","false").lower()=="true"

emb = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

if USE_PINE and os.getenv("PINECONE_API_KEY"):
    import pinecone
    pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENV"))
    vs = Pinecone.from_existing_index(os.getenv("VECTOR_INDEX_NAME","hr-index"), emb)
else:
    vs = Chroma(persist_directory="./data/chroma", embedding_function=emb)

policies_dir = Path("./data/policies")
docs = []
metas = []
for p in policies_dir.glob("*.txt"):
    text = p.read_text(encoding="utf-8")
    docs.append(text)
    metas.append({"source": p.name})

if docs:
    vs.add_texts(docs, metadatas=metas)
    print("Seeded policies into vectorstore.")
else:
    print("No policy docs found in ./data/policies")
