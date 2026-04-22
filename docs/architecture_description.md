
# Architecture Description

**Student:** Emmanuella Uwudia  
**Index Number:** AI_10012200008  
**Date:** April 21, 2026  

---

## System Overview

Brew & Ask follows a three-layer architecture: **User Interface Layer**, **RAG Pipeline Layer**, and **Data Storage Layer**. Each layer is independent and communicates via well-defined interfaces.

---

## Layer 1: User Interface Layer

### Component: Streamlit UI (`ui/app.py`)

**Responsibilities:**
- Display chat interface
- Collect user queries
- Show responses with source attribution
- Provide settings sidebar (k-value, query expansion toggle, debug mode)
- Display similarity scores for retrieved chunks

**Key Functions:**
- `render_header()` - Ghana-themed coffee shop header
- `render_sidebar()` - Settings and statistics
- `render_response_card()` - Formatted response with sources
- `render_feedback_widget()` - User rating collection (1-5 stars)

**Data Flow:**
- Receives user query → forwards to RAG Pipeline
- Receives response → displays with source cards

---

## Layer 2: RAG Pipeline Layer

This layer is implemented **without LangChain or LlamaIndex** (custom code only).

### Component 2.1: Query Processor (`src/retrieval.py`)

**Responsibilities:**
- Query expansion with Ghana-specific synonyms
- Top-K retrieval
- Similarity scoring

**Key Method:**
```python
def expand_query(self, query: str) -> List[str]:
    # Adds synonyms: "NPP" → "New Patriotic Party", "election" → "elections|vote|polls"
Data Flow:

Input: Raw user query

Output: Expanded query (if enabled)

Component 2.2: Embedding Generator (src/embeddings.py)
Responsibilities:

Convert text to vector embeddings

Use Sentence Transformers (all-MiniLM-L6-v2)

Generate 384-dimension vectors

Key Method:

python
def generate_embeddings(self, texts: List[str]) -> np.ndarray:
    # Returns numpy array of shape (len(texts), 384)
Data Flow:

Input: Query text or document chunks

Output: 384-dimension embedding vector

Component 2.3: Vector Search Engine (src/vector_store.py)
Responsibilities:

Build and manage FAISS index

Perform cosine similarity search

Return top-K chunks with scores

Key Method:

python
def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Dict]:
    # Returns top-k chunks with similarity scores
Data Flow:

Input: Query embedding

Output: Top-K chunks with scores (0-1)

Component 2.4: Prompt Builder (src/prompt_builder.py)
Responsibilities:

Inject retrieved context into prompt template

Apply hallucination control rules

Manage context window (truncate/rank)

Key Method:

python
def build_prompt(self, query: str, chunks: List[Dict], conversation_context: str = "") -> str:
    # Returns structured prompt with context and instructions
Data Flow:

Input: Query + retrieved chunks + conversation history

Output: Structured prompt for LLM

Component 2.5: LLM Client (src/llm_client.py)
Responsibilities:

Call Groq API (Llama 3.1 8B)

Handle API errors gracefully

Log responses

Key Method:

python
def generate(self, prompt: str, temperature: float = 0.3) -> Dict:
    # Returns LLM response with metadata
Data Flow:

Input: Structured prompt

Output: Generated answer

Component 2.6: Innovation Feature - Conversation Memory (src/rag_pipeline.py)
Responsibilities:

Store last 10 exchanges (user + assistant)

Resolve pronouns ("it", "that", "they")

Provide clear memory button

Key Method:

python
def build_contextual_query(self, query: str) -> str:
    # Enhances query with conversation context
Layer 3: Data Storage Layer
Component 3.1: Raw Data Storage (data/raw/)
File	Source	Format
Ghana_Election_Result.csv	GitHub	CSV (election results by region/year)
2025-Budget-Statement.pdf	MOFEP	PDF (budget allocations, policies)
Component 3.2: Processed Data Storage (data/processed/)
File	Description	Created By
cleaned_election_data.csv	Cleaned CSV (no duplicates, standardized columns)	data_cleaning.py
extracted_budget_text.txt	Extracted PDF text	data_cleaning.py
all_chunks.json	500-char chunks with 100-char overlap	chunking.py
Component 3.3: Vector Index Storage (data/vectors/)
File	Description	Created By
embeddings.npy	384-dim vectors for all chunks	embeddings.py
faiss_index.bin	FAISS index for similarity search	vector_store.py
chunk_metadata.json	Chunk text + source mapping	vector_store.py
Data Flow (Request Path)
text
1. User → Streamlit UI: "What is the healthcare budget?"
2. UI → Query Processor: User query
3. Query Processor → Embedding Generator: Expanded query
4. Embedding Generator → Vector Search: Query embedding (384d)
5. Vector Search → Prompt Builder: Top-5 chunks with scores
6. Prompt Builder → LLM Client: Structured prompt with context
7. LLM Client → UI: Generated response
8. UI → User: Answer with source cards
Data Flow (Response Path - Upward)
text
1. LLM Client → UI: Raw response
2. UI → User: Formatted response with source attribution
3. User → Feedback Loop: Rating (1-5 stars)
4. Feedback Loop → Vector Search: Adjusts chunk weights
Why This Design is Suitable for the Domain
Ghana Election Data Characteristics:
Tabular data (CSV rows)

200-300 chars per row

500-char chunks fit 1-2 rows perfectly

Ghana Budget Data Characteristics:
Paragraph-based text

400-600 chars per paragraph

500-char chunks with 100 overlap preserve continuity

Requirements Met:
Domain Need	Design Solution
Accurate numbers	FAISS similarity search finds exact matches
Source attribution	Each chunk stores source metadata
No hallucinations	Structured prompt with explicit rules
Fast responses	FAISS index + Groq ultra-fast LLM
Natural conversations	Conversation memory innovation
Component Interaction Summary
text
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│   UI    │────▶│Retrieval│────▶│Embedding│────▶│  FAISS  │
└─────────┘     └─────────┘     └─────────┘     └────┬────┘
      ▲                                               │
      │                                               ▼
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  User   │◀────│   LLM   │◀────│ Prompt  │◀────│ Chunks  │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
      │                                               ▲
      │                                               │
      └──────────────▶ Feedback Loop ────────────────┘
Deployment Architecture
Frontend: Streamlit (runs on port 8501)

Backend: Python RAG pipeline (same process)

Vector Store: FAISS (in-memory, loaded at startup)

LLM: Groq API (external)

Hosting: Hugging Face Spaces (Docker container)

Security & Privacy
API keys stored in .env (not committed to GitHub)

No user data stored permanently

Feedback data stored locally in logs/feedback_data.json

Conclusion
This architecture efficiently handles the specific requirements of Ghana election and budget data while remaining extensible for future improvements (more election years, additional PDFs, etc.). The three-layer separation ensures maintainability, and the custom implementation (no LangChain) demonstrates deep understanding of RAG principles.

