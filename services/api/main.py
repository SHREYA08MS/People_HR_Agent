# services/api/main.py

import os, shutil, json
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from services.api.db import init_db, SessionLocal, Resume, JobDescription
from services.resume_processor import parser
from services.rag_agent.rag_agent import answer_question, init_rag
#from services.rag_agent.rag_agent import rag, local_answer
from services.interview_service.interview import generate_questions, evaluate_answer
#from langchain_openai import OpenAIEmbeddings
from sqlalchemy.orm import Session
#from services.rag_agent.rag_agent import rag
from pathlib import Path

load_dotenv()

app = FastAPI(title="HR Agents API")
init_db()

DATA_DIR = Path("./data")
RESUME_DIR = DATA_DIR / "resumes"
RESUME_DIR.mkdir(parents=True, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup_event():
    init_rag()


@app.get("/")
def home():
    return {"message": "HR Agents API is running"}


# ------------------ HR ASSISTANT ------------------

@app.post("/api/hr/ask")
async def hr_ask(question: str = Form(...)):
    try:
        ans = answer_question(question)
        return {"answer": ans}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# ------------------ RESUME PROCESSING ------------------

@app.post("/api/resumes/upload")
async def upload_resume(file: UploadFile = File(...)):
    try:
        save_path = RESUME_DIR / file.filename
        with open(save_path, "wb") as f:
            f.write(await file.read())

        parsed = parser.parse_and_index(str(save_path), file.filename)

        db = next(get_db())
        r = Resume(filename=file.filename, parsed_json=json.dumps(parsed))
        db.add(r); db.commit(); db.refresh(r)

        return {"status": "ok", "resume_id": r.id, "parsed": parsed}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/api/job/create")
async def create_job(title: str = Form(...), jd_text: str = Form(...)):
    try:
        db = next(get_db())
        job = JobDescription(title=title, jd_text=jd_text)
        db.add(job); db.commit(); db.refresh(job)
        return {"job_id": job.id}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/api/resumes/{job_id}/ranked")
def rank_resumes(job_id: int):
    try:
        db = next(get_db())
        job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
        if not job:
            return JSONResponse({"error": "job not found"}, status_code=404)

        # embeddings
        from langchain.embeddings import OpenAIEmbeddings
        from langchain.vectorstores import Chroma, Pinecone
        emb = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

        use_pine = os.getenv("USE_PINECONE","false").lower() == "true" and os.getenv("PINECONE_API_KEY")

        if use_pine:
            import pinecone
            pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENV"))
            vs = Pinecone.from_existing_index(os.getenv("VECTOR_INDEX_NAME","hr-index"), emb)
        else:
            vs = Chroma(persist_directory="./data/chroma", embedding_function=emb)

        results = vs.similarity_search(job.jd_text, k=10)
        ranked = [{"filename": r.metadata.get("filename"), "metadata": r.metadata} for r in results]

        return {"job_id": job_id, "ranked": ranked}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# ------------------ INTERVIEW MODULE (FIXED) ------------------

@app.post("/api/interview/generate")
def api_generate_interview(
    title: str = Form(...),
    level: str = Form("mid"),
    competencies: str = Form("")
):
    try:
        comps = [c.strip() for c in competencies.split(",")] if competencies else \
                ["problem solving", "communication"]

        q = generate_questions(title, level, comps)
        return {"questions": q}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/api/interview/evaluate")
def api_evaluate(
    answer_text: str = Form(...),
    reference_points: str = Form(...)
):
    try:
        refs = [r.strip() for r in reference_points.split("|")]
        res = evaluate_answer(answer_text, refs)
        return res
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# ------------------ ONBOARDING ------------------

@app.post("/api/onboarding/start")
def start_onboarding(newhire_name: str = Form(...), role: str = Form(...)):
    try:
        plan = [
            {"task":"Submit ID proof", "due":"Day 1"},
            {"task":"Complete benefits enrollment", "due":"Day 3"},
            {"task":"Complete security training", "due":"Day 7"},
        ]
        return {"newhire": newhire_name, "role": role, "plan": plan}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)    
