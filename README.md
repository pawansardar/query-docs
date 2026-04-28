# 📄 QueryDocs

QueryDocs is a Retrieval-Augmented Generation (RAG) system designed to enable intelligent querying over documents using modern vector search and LLM-based reasoning. It allows users to extract meaningful insights from large datasets by combining semantic search with generative AI.

---

## 🚀 Overview

QueryDocs leverages vector embeddings and similarity search to retrieve relevant context from documents, which can then be used by large language models (LLMs) to generate accurate, context-aware responses.

This project is built with scalability and extensibility in mind, making it easy to integrate newer models and frameworks as they evolve.

---

## 🧠 Key Features

* 🔍 Semantic search over documents using vector embeddings
* ⚡ FastAPI-powered backend for high-performance APIs
* 📦 Qdrant vector database for efficient similarity search
* 🤖 Gemini models for embeddings and future LLM integration
* 🔗 Designed for future integration with LangChain
* 🧩 Modular and extensible architecture

---

## 🏗️ Tech Stack

| Component       | Technology          |
| --------------- | ------------------- |
| Backend API     | FastAPI             |
| Language        | Python              |
| Vector Database | Qdrant              |
| Embeddings      | Gemini Models       |
| LLM (Planned)   | Gemini Models       |
| Orchestration   | LangChain (Planned) |

---

## 📁 Project Structure

```
query-docs/
│
├── app/
│   ├── api/                    # FastAPI routes
│   ├── core/                   # Configurations and settings
│   ├── db/                     # Qdrant integration
│   ├── services/               # Business logic
│   └── main.py                 # Application entry point
│
├── docker-compose.yaml         # Docker services configuration
├── .env.example                # Environment variables template
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/pawansardar/query-docs.git

# Navigate into the project directory
cd query-docs

# Create virtual environment
python -m venv .venv

# Activate environment
source .venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🔐 Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

---

## ▶️ Running the Application

```bash
uvicorn app.main:app --reload
```

API will be available at:

```
http://127.0.0.1:8000
```

---

## 🔄 Workflow

1. **Document Ingestion**

   * Load and preprocess documents
   * Generate embeddings using Gemini models
   * Store vectors in Qdrant

2. **Query Processing (Planned)**

   * Convert user query into embedding
   * Perform similarity search in Qdrant
   * Retrieve relevant context

3. **Response Generation (Planned)**

   * Pass retrieved context to LLM
   * Generate final answer

---

## 🔮 Future Enhancements

* ✅ Integration with Gemini LLM for answer generation
* 🔗 LangChain pipeline for better orchestration
* 🧠 Hybrid search (keyword + vector)
* 📊 UI dashboard for querying and visualization
* 🔐 Authentication and multi-user support

---

## 📜 License

This project is licensed under the Apache-2.0 License.
