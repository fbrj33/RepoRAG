# RepoRAG — AI Codebase Understanding & Debugging Assistant

RepoRAG is a code-aware Retrieval-Augmented Generation (RAG) system designed to help developers understand and debug software repositories.

Instead of treating a repository as plain text, RepoRAG extracts code structure, creates semantic embeddings, retrieves relevant code, and uses a local LLM to generate grounded answers with source references.

## Features

- Repository ingestion
- Code-aware Python chunking using AST
- Semantic code retrieval
- Vector search with ChromaDB
- Local embeddings with Sentence Transformers
- Context construction with file and line metadata
- Local LLM generation using Ollama
- Source-aware answers

## Architecture

```text
Repository
    ↓
Repository Loader
    ↓
Code-Aware Splitter
    ↓
Sentence Transformers
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
