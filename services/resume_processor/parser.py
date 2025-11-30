# services/resume_processor/parser.py
import os, re, json
from pdfminer.high_level import extract_text
import spacy
from langchain.embeddings import OpenAIEmbeddings
#from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma, Pinecone
from dotenv import load_dotenv

nlp = spacy.load("en_core_web_sm")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USE_PINECONE = os.getenv("USE_PINECONE","false").lower()=="true"
INDEX_NAME = os.getenv("VECTOR_INDEX_NAME","hr-index")

def extract_text_from_file(path: str) -> str:
    if path.lower().endswith(".pdf"):
        return extract_text(path)
    else:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

def simple_extract(text: str) -> dict:
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    emails = re.findall(r"[\w\.-]+@[\w\.-]+", text)
    phones = re.findall(r"\+?\d[\d\-\s]{7,}\d", text)
    # naive skill matching from a small skill list
    skill_bank = ["python","sql","pytorch","tensorflow","aws","docker","react","node","java","c++"]
    skills = []
    for s in skill_bank:
        if re.search(r"\b"+re.escape(s)+r"\b", text, flags=re.I):
            skills.append(s)
    return {"names": list(dict.fromkeys(names))[:3], "emails": list(dict.fromkeys(emails))[:3], "phones": list(dict.fromkeys(phones))[:3], "skills": skills, "raw": text}

# Index resume text into vectorstore
def index_resume_text(text: str, metadata: dict):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    if USE_PINECONE and os.getenv("PINECONE_API_KEY"):
        import pinecone
        pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENV"))
        vs = Pinecone.from_existing_index(INDEX_NAME, embeddings)
    else:
        vs = Chroma(persist_directory="./data/chroma", embedding_function=embeddings)
    # store as one document per resume
    vs.add_texts([text], metadatas=[metadata])

def parse_and_index(file_path: str, filename: str):
    txt = extract_text_from_file(file_path)
    parsed = simple_extract(txt)
    index_resume_text(parsed["raw"], {"filename": filename, "names": parsed["names"], "skills": parsed["skills"]})
    return parsed
