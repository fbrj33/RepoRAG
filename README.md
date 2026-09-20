# RepoRAG — AI Codebase Understanding & Debugging Assistant

> A code-aware RAG system that helps developers understand and interact with software repositories using natural language.

## Overview

RepoRAG allows developers to ask questions about a codebase and receive answers grounded in the repository's actual source code.

Example questions:

* Where is authentication implemented?
* Where is this endpoint defined?
* Which function creates a new incident?
* Why could this endpoint return a 404?

Unlike a traditional document RAG system, RepoRAG uses **AST-based code chunking** for Python files and preserves file, function, and line metadata for source attribution.

## Architecture

```text
Repository
    ↓
Code-Aware Chunking
    ↓
Embeddings
    ↓
ChromaDB
    ↓
Semantic Retrieval
    ↓
Context Builder
    ↓
Local LLM
    ↓
Grounded Answer
```

## Tech Stack

* **Python**
* **LangChain**
* **ChromaDB**
* **Sentence Transformers**
* **Ollama**
* **FastAPI** — planned
* **Streamlit** — planned
* **Docker** — planned

## Current Features

* Repository ingestion
* Multi-language file support
* Python AST-based chunking
* Function/class metadata extraction
* Sentence Transformer embeddings
* ChromaDB vector storage
* Semantic code retrieval
* Structured context generation

## Roadmap

* [x] Repository ingestion
* [x] Code-aware chunking
* [x] Embeddings & vector search
* [x] Semantic retrieval
* [x] Context construction
* [ ] Local LLM generation
* [ ] Source-aware answers
* [ ] Hybrid retrieval (Vector + BM25)
* [ ] Reranking
* [ ] Debugging mode
* [ ] FastAPI API
* [ ] Streamlit UI
* [ ] Evaluation
* [ ] Docker & CI/CD

## Example

**Question**

> Where are items created?

**Retrieved source**

```text
routes.py
add_item()
lines 24-27
```

**Relevant code**

```python
def add_item():
    item = request.get_json()
    items.append(item)
    return {"message": "Item added successfully"}, 201
```

RepoRAG can use this retrieved context to generate a grounded explanation instead of answering from general knowledge.

## Project Goal

The goal is to build a practical **RAG system for software engineering**, combining code-aware retrieval, semantic search, grounded generation, and eventually automated debugging assistance.

## Author

**Farah Ben Rejab**
Computer Science Engineering Student — ENSI Manouba
