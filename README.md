# 🇬🇭 Brew & Ask - Ghana Elections & Budget Assistant

**Course:** CS4241 - Introduction to Artificial Intelligence  
**Student:** [Your Name]  
**Index Number:** AI_20240001  
**Lecturer:** Godwin N. Danso  
**Date:** April 2026  

---

## 📋 Project Overview

Brew & Ask is a **Retrieval-Augmented Generation (RAG)** chatbot that answers questions about:

- **Ghana Election Results** (from CSV dataset)
- **Ghana 2025 Budget Statement** (from PDF)

The system is built **entirely from scratch** without using LangChain, LlamaIndex, or any pre-built RAG pipelines.

---

## 🎯 Features

| Feature | Implementation |
|---------|----------------|
| Data Cleaning | Pandas + regex for election CSV and budget PDF |
| Chunking | 500 char chunks, 100 char overlap, sentence-aware |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| Vector Store | FAISS with cosine similarity |
| Retrieval | Top-k + query expansion |
| LLM | Groq (Llama 3 8B) - free tier |
| UI | Streamlit with Ghana theme |
| Innovation | Feedback loop for retrieval improvement |

---

## 🏗️ Architecture
