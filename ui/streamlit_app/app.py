# ui/streamlit_app/app.py
import streamlit as st
import requests
import os

API_BASE = st.secrets.get("API_BASE") if "API_BASE" in st.secrets else "http://localhost:8000"

st.set_page_config(page_title="HR Agents", layout="wide")
st.title("HR Agents — MVP")

menu = st.sidebar.selectbox("Go to", ["HR Assistant", "Resume Screening", "Interview", "Onboarding"])

if menu == "HR Assistant":
    st.header("HR Assistant (RAG)")
    q = st.text_area("Ask HR anything about policies, leave, benefits etc.")
    if st.button("Ask HR"):
        r = requests.post(f"{API_BASE}/api/hr/ask", data={"question": q})
        st.write(r.json().get("answer"))

if menu == "Resume Screening":
    st.header("Upload Resume")
    uploaded = st.file_uploader("Upload resume (.txt or .pdf)", type=["pdf","txt"])
    if uploaded:
        files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type)}
        r = requests.post(f"{API_BASE}/api/resumes/upload", files=files)
        st.json(r.json())
    st.subheader("Create Job Description (for ranking)")
    with st.form("create_jd"):
        title = st.text_input("Title")
        jd = st.text_area("Job Description")
        submitted = st.form_submit_button("Create Job")
        if submitted:
            r = requests.post(f"{API_BASE}/api/job/create", data={"title": title, "jd_text": jd})
            st.success(f"Job created: {r.json().get('job_id')}")
    st.subheader("Rank for Job ID")
    job_id = st.number_input("Job ID", min_value=1, step=1)
    if st.button("Get ranked resumes"):
        r = requests.get(f"{API_BASE}/api/resumes/{job_id}/ranked")
        st.json(r.json())

if menu == "Interview":
    st.header("Interview — question generation & evaluation")
    with st.form("gen"):
        title = st.text_input("Job Title")
        level = st.selectbox("Level", ["junior","mid","senior"])
        comps = st.text_input("Competencies (comma-separated)", value="problem solving,communication")
        gen = st.form_submit_button("Generate Questions")
        if gen:
            r = requests.post(f"{API_BASE}/api/interview/generate", data={"title": title, "level": level, "competencies": comps})
            st.write(r.json().get("questions"))
    st.subheader("Evaluate an answer")
    with st.form("eval"):
        refs = st.text_area("Reference points (separate with | )", value="use examples|cover edge cases")
        ans = st.text_area("Candidate answer")
        ev = st.form_submit_button("Evaluate")
        if ev:
            r = requests.post(f"{API_BASE}/api/interview/evaluate", data={"answer_text": ans, "reference_points": refs})
            st.json(r.json())

if menu == "Onboarding":
    st.header("Start Onboarding")
    with st.form("onb"):
        name = st.text_input("New hire name")
        role = st.text_input("Role")
        s = st.form_submit_button("Start Onboarding")
        if s:
            r = requests.post(f"{API_BASE}/api/onboarding/start", data={"newhire_name": name, "role": role})
            st.json(r.json())
