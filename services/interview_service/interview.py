import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
import json
import re

load_dotenv()

print("Loaded KEY:", os.getenv("OPENAI_API_KEY"))

# Initialize LLM
llm = ChatOpenAI(
    temperature=0.0,
    model="gpt-4o-mini",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

def generate_questions(job_title: str, level: str, competencies: list, n=3) -> list:
    """
    Generate interview questions for a given job title, level, and competencies.
    Default number of questions is 3.
    """
    comp_str = ", ".join(competencies)
    prompt = (
        f"Generate {n} interview questions for a {level} {job_title} "
        f"focused on these competencies: {comp_str}. "
        f"Return ONLY the numbered list of questions."
    )
    
    # Use .predict() to get string output
    resp = llm.predict(prompt)

    # Convert numbered list into Python list
    questions = [
        line.strip()[3:].strip()  # remove "1. " etc.
        for line in resp.split("\n") 
        if line.strip() and line.strip()[0].isdigit()
    ]

    return questions

def evaluate_answer(answer_text: str, reference_points: list) -> dict:
    """
    Evaluate a candidate's answer based on reference points.
    Returns JSON with score, breakdown, and explanation.
    """
    refs = "; ".join(reference_points)
    prompt = f"""
You are an expert interviewer. Given reference points: {refs}
Score the candidate answer on a scale of 1-5 for correctness, clarity, and completeness.
Return strictly this JSON structure:
{{
  "score": int,
  "breakdown": {{
      "correctness": int,
      "clarity": int,
      "completeness": int
  }},
  "explanation": "text"
}}
Candidate answer: {answer_text}
"""
    resp = llm.predict(prompt)

    # Parse JSON from response
    match = re.search(r"\{.*\}", resp, re.S)
    if match:
        try:
            return json.loads(match.group(0))
        except:
            return {"raw": resp}

    return {"raw": resp}

# Example usage:
questions = generate_questions(
    job_title="Software Developer",
    level="Junior",
    competencies=["Python", "Problem Solving", "Data Structures"]
)
print(questions)
