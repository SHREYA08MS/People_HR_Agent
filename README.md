Great! Here is a **clean, professional, fully-explained README.md** for your **People HR Agent (AI-based HR Assistant with FastAPI + Streamlit + RAG + Vector DB + Q/A + Database)**.

If you want, I can also **export this as a file**.

---

# 📌 **README.md — People HR Agent**

---

# **People HR Agent — AI-Powered HR Assistant**

The **People HR Agent** is an end-to-end HR automation system built using **FastAPI**, **Streamlit**, **RAG-based question answering**, **vector search**, and **database-driven employee management**.

It allows employees to interact with an intelligent HR chatbot capable of answering HR-related queries using policy documents, generating responses, and managing various HR tasks.

---

# 🚀 **Features**

### ✅ **1. HR Chatbot (RAG-Based)**

* Employees can ask any HR-related question.
* Uses **Retrieval-Augmented Generation** with vector embeddings.
* Answers are generated using **OpenAI / LLM models**.
* Searches HR documents stored in `/data/policies`.

### ✅ **2. Backend (FastAPI)**

* API endpoints for:

  * Chat responses
  * Document ingestion
  * Database CRUD
  * HR agent actions

### ✅ **3. Interactive UI (Streamlit)**

* User-friendly chat interface.
* Shows conversation history.
* Upload documents to update the RAG database.

### ✅ **4. Database Integration**

* SQLite database `hr_agents.db` used for:

  * Storing conversations
  * Logging queries
  * Agent actions

### ✅ **5. Modular Architecture**

* `services/`: RAG engine, vector DB, API services
* `scripts/`: Utility scripts
* `ui/`: Frontend (Streamlit app)

---

# 🧠 **Tech Stack**

| Component       | Technology                            |
| --------------- | ------------------------------------- |
| Backend         | FastAPI                               |
| Frontend        | Streamlit                             |
| Language Model  | OpenAI GPT                            |
| Vector Database | FAISS / Chroma                        |
| Database        | SQLite                                |
| Environment     | Python 3.10                           |
| Deployment      | GitHub, Streamlit Cloud, Render, etc. |

---

# 📂 **Project Structure**

```
hr_agent/
│── data/
│   └── policies/              # HR policy PDF/text files
│
│── scripts/
│   └── ingest.py              # Creates embeddings and vector store
│
│── services/
│   ├── api/
│   │   └── main.py            # FastAPI backend
│   ├── rag_engine.py          # RAG logic
│   ├── vector_store.py        # FAISS/Chroma vector DB
│   └── utils.py               # Helper functions
│
│── ui/
│   └── streamlit_app/
│       ├── app.py             # Streamlit UI
│       └── .streamlit/
│           └── config.toml
│
│── .gitignore                 # Ignore venv, db, etc.
│── hr_agents.db               # SQLite DB
│── requirements.txt           # Project dependencies
└── README.md
```

---

# ⚙️ **Installation & Setup**

### **1. Clone the repository**

```bash
git clone https://github.com/SHREYA08MS/People_HR_Agent
cd People_HR_Agent
```

### **2. Create a virtual environment**

```bash
python -m venv .venv
.venv\Scripts\activate     # Windows
```

### **3. Install dependencies**

```bash
pip install -r requirements.txt
```

### **4. Set environment variables**

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key
```

---

# 📘 **Run the Project**

### **➡️ Start the FastAPI Backend**

```bash
uvicorn services.api.main:app --reload --port 8000
```

API will be available at:

```
http://127.0.0.1:8000
```

---

### **➡️ Start the Streamlit Frontend**

```bash
streamlit run ui/streamlit_app/app.py
```

UI opens in the browser.

---

# 🧪 **Using the HR Agent**

### **🔹 1. Upload HR documents**

* Upload PDFs or text files
* They are embedded and stored in vector DB

### **🔹 2. Ask HR questions**

Examples:

* "How many casual leaves do employees get?"
* "Explain the notice period policy."
* "What is the work-from-home rule?"

### **🔹 3. Backend RAG Engine**

* Retrieves top-k similar chunks
* LLM generates human-like answers
* Saved to database

---

# 🛠️ **Future Enhancements**

* User authentication
* Admin dashboard
* Email/Slack integration
* Multi-agent HR workflows
* Voice-enabled chat assistant

---

Author

**Shreya MS**
GitHub: *SHREYA08MS*


