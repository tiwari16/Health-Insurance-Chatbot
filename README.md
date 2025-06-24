# 🌺 Health Insurance AI Chatbot — Project Documentation

---

## 📁 Project Structure

```
Chatbot_FAISS_Langchain/
├── .streamlit/                     
│   └── secrets.toml               # Streamlit secrets (API keys)
├── app.py                         # Main Streamlit chatbot app
├── chatbot/                       # Modular chatbot logic
│   ├── __init__.py                
│   ├── chatbot_logic.py           # RAG chain setup
│   ├── utils.py                   # Formatting and helper functions
│   └── vectorstore.py             # PDF ingestion and FAISS setup
├── data/                          # Your source PDFs for policy documents
├── faiss_index/                   # FAISS vector index (auto-generated)
├── requirements.txt               # Python dependencies
├── reset_env.sh                   # Quick environment reset script (optional)
├── tests/                         # Chatbot evaluation framework
│   ├── evaluation.py              # Evaluation script with metrics
│   └── evaluation_data/
│       ├── policy_eval.jsonl      # Test questions and expected answers
│       └── policy_eval_results.csv # Evaluation results (auto-generated)
├── Dockerfile                     # Docker container setup
├── docker-compose.yml             # One-command Docker startup
└── README.md                      # Project instructions
```

---

## ✅ Project Overview

This AI-powered chatbot answers health insurance policy questions using:

* 🔍 LangChain Retrieval-Augmented Generation (RAG)
* 🐂 FAISS Vector Search for fast document retrieval
* 🧠 OpenAI GPT models (e.g., GPT-4) for human-like responses
* 📜 PDF document ingestion for grounding in your policies
* 📝 Streamlit web interface for easy chat interaction
* 📦 Docker & Docker Compose for consistent deployment
* 📊 Built-in chatbot evaluation with CSV result output

---

## 🚀 Running the Chatbot Locally

**1️⃣ Clone the repository:**

```bash
git clone https://your-repo-link.git
cd Chatbot_FAISS_Langchain
```

---

**2️⃣ Create a virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

**3️⃣ Install Python dependencies:**

```bash
pip install -r requirements.txt
```

---

**4️⃣ Add your OpenAI key:**

Create `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "your-key-here"
```

---

**5️⃣ Place your policy PDFs in `/data`:**

```bash
data/
├── Easy Extras.pdf
└── Hospital Cover.pdf
```

---

**6️⃣ Run the chatbot locally:**

```bash
streamlit run app.py
```

Visit the chatbot at:

```
http://localhost:8501
```

---

## 🛣️ Running with Docker

**1️⃣ Build the Docker image:**

```bash
docker build -t health-chatbot .
```

---

**2️⃣ Run the container with your API key:**

```bash
docker run -p 8501:8501 -e OPENAI_API_KEY="your-key" health-chatbot
```

---

## ⚡️ One-Command Startup with Docker Compose (Recommended)

**1️⃣ Ensure `docker-compose.yml` exists:**

```yaml
version: "3.9"

services:
  health-chatbot:
    build: .
    container_name: health-chatbot
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=your-key-here
    volumes:
      - ./data:/app/data
      - ./faiss_index:/app/faiss_index
```

---

**2️⃣ Run everything with one command:**

```bash
docker-compose up --build
```

---

**3️⃣ Access the chatbot at:**

```
http://localhost:8501
```

---

## 📊 Evaluating Chatbot Performance

**1️⃣ Place your evaluation questions in:**

```
tests/evaluation_data/policy_eval.jsonl
```

This file contains realistic policy-related questions with expected answers.

---

**2️⃣ Run the evaluation script:**

```bash
python -m tests.evaluation
```

---

**3️⃣ Review the results:**

```
tests/evaluation_data/policy_eval_results.csv
```

This CSV contains:

| Column            | Description                                              |
| ----------------- | -------------------------------------------------------- |
| `question`        | The test question asked to the chatbot                   |
| `expected`        | The expected correct answer (ground truth)               |
| `actual`          | The chatbot's generated response                         |
| `rougeL_f1`       | ROUGE-L text similarity score (higher = better)          |
| `sources`         | Retrieved document sources for grounding transparency    |
| `exact_match`     | Whether expected keywords appear in the chatbot's answer |
| `llm_judge_score` | AI quality score (1 = poor, 5 = excellent)               |
| `llm_reason`      | Short explanation from AI judge on answer quality        |

Open the CSV with Excel, Google Sheets, or any text editor.

---

## 🛠️ Common Issues & Fixes

| Issue                 | Solution                                           |
| --------------------- | -------------------------------------------------- |
| API key errors        | Check `.streamlit/secrets.toml` or Docker env vars |
| Poor chatbot answers  | Delete `/faiss_index`, rerun to rebuild the index  |
| PDF processing issues | Ensure readable, non-password-protected PDFs       |
| Docker build errors   | Check Docker version, rebuild with `--no-cache`    |


```
