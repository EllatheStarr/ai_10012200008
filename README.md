# ☕ Brew & Ask - GH RAG Bot

**Student:** Emmanuella Uwudia  
**Index Number:** AI_10012200008  
**Course:** CS4241 - Introduction to Artificial Intelligence  

---

## Table of Contents

1. [Live Demo](#live-demo)
2. [Overview](#overview)
3. [Features](#features)
4. [Tech Stack](#tech-stack)
5. [Project Structure](#project-structure)
6. [Local Setup](#local-setup)
7. [Sample Questions](#sample-questions)
8. [Statistics](#statistics)
9. [Links](#links)

---

## Live Demo

🔗 **[https://ai-10012200008.streamlit.app](https://ai-10012200008.streamlit.app)**

> *Note: The app may take 10-15 seconds to wake up after inactivity (free tier limitation).*

---

## Overview

Brew & Ask is a **Retrieval-Augmented Generation (RAG)** chatbot that answers questions about:

- 📊 **Ghana Election Results** (2000, 2004, 2016, 2020)
- 📄 **Ghana 2025 Budget Statement**

The system is built entirely from scratch without LangChain, LlamaIndex, or any pre-built RAG pipelines. All components including chunking, embeddings, vector search, prompt construction, and LLM integration were manually implemented.

---

## Features

| Feature | Description |
|---------|-------------|
| Custom RAG | No frameworks - fully manual implementation |
| Query Expansion | Ghana-specific synonyms (NPP → New Patriotic Party) |
| Hallucination Control | Structured prompt with explicit rules |
| Source Attribution | Shows document names and similarity scores |
| Conversation Memory | Remembers last 10 exchanges for follow-up questions |
| Feedback Loop | User ratings (1-5 stars) improve retrieval over time |

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| UI Framework | Streamlit |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| Vector Store | FAISS (Facebook AI Similarity Search) |
| LLM Provider | Groq (free tier, 560 tokens/sec) |
| LLM Model | Llama 3.1 8B Instant |
| Data Processing | Pandas, PyPDF2 |
| Language | Python 3.10+ |

---

## Project Structure
```text
ai_10012200008/
│
├── data/
│ ├── raw/ # Original CSV and PDF files
│ │ ├── Ghana_Election_Result.csv
│ │ └── 2025-Budget-Statement-and-Economic-Policy_v4.pdf
│ ├── processed/ # Cleaned and chunked data
│ │ ├── cleaned_election_data.csv
│ │ ├── extracted_budget_text.txt
│ │ └── all_chunks.json
│ └── vectors/ # FAISS index and metadata
│ ├── faiss_index.bin
│ ├── chunk_metadata.json
│ └── embeddings.npy
│
├── src/ # Source code modules
│ ├── data_cleaning.py
│ ├── chunking.py
│ ├── embeddings.py
│ ├── vector_store.py
│ ├── retrieval.py
│ ├── prompt_builder.py
│ ├── llm_client.py
│ ├── rag_pipeline.py
│ ├── innovation_feedback.py
│ └── adversarial_tests.py
│
├── ui/ # Streamlit interface
│ ├── app.py
│ ├── components.py
│ └── style.css
│
├── tests/ # Test files
│ ├── test_retrieval.py
│ ├── test_rag_vs_llm.py
│ └── test_failure_cases.py
│
├── logs/ # Auto-generated logs
│ ├── retrieval_logs.json
│ ├── prompt_logs.json
│ ├── pipeline_logs.json
│ ├── feedback_data.json
│ ├── adversarial_results.json
│ └── experiment_logs.md
│
├── docs/ # Documentation
│ ├── architecture_diagram.png
│ ├── architecture_description.md
│ ├── chunking_justification.md
│ ├── prompt_iterations.md
│ └── final_documentation.md
│
├── requirements.txt
├── .env (not committed - API keys)
├── .gitignore
├── main.py
└── README.md
```


---

## Local Setup

### Prerequisites

- Python 3.10 or higher
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/EllatheStarr/ai_10012200008.git
cd ai_10012200008

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Groq API key
echo GROQ_API_KEY=your_key_here > .env

# 4. Download datasets to data/raw/
#    - Ghana_Election_Result.csv
#    - 2025-Budget-Statement-and-Economic-Policy_v4.pdf

# 5. Run data preparation (creates chunks and FAISS index)
python main.py --prepare

# 6. Launch the application
python main.py --ui
```

The app will open at http://localhost:8501

## Sample Questions

### Election Questions

1. "What parties contested the 2020 election?"
2. "What did the election results show for Greater Accra?"
3. "Tell me about the 2020 presidential election"

### Budget Questions

1. "What did the budget say about healthcare?"
2. "Tell me about the LEAP programme"
3. "What are the key health initiatives in the 2025 budget?"

## Statistics

| Metric | Value |
|--------|-------|
| Total lines of code | 3,614 |
| Total chunks indexed | 1,909 |
| Embedding dimension | 384 |
| FAISS index size | 2.9 MB |
| Average response time | ~2 seconds |
| LLM speed | Up to 560 tokens/sec |
| Chunk size | 500 characters |
| Chunk overlap | 100 characters (20%) |

## Links

| Item | Link |
|------|------|
| GitHub Repository | [github.com/EllatheStarr/ai_10012200008](https://github.com/EllatheStarr/ai_10012200008) |
| Deployed Application | [ai-10012200008.streamlit.app](https://ai-10012200008.streamlit.app) |

Made with ❤️ by Emmanuella Uwudia