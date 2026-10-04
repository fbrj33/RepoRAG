import os

import ollama


class CodeGenerator:
    def __init__(self, model_name: str = "llama3.2:3b"):
        self.model_name = model_name

        self.client = ollama.Client(
            host=os.getenv(
                "OLLAMA_HOST",
                "http://127.0.0.1:11434",
            )
        )

    def generate(self, question: str, context: str) -> str:
        prompt = f"""
You are RepoRAG, an AI assistant that answers questions about a software repository.

Answer the user's question using ONLY the repository context provided below.

IMPORTANT RULES:
1. Use the context as the source of truth.
2. Do not say that the context is missing if the answer is clearly present.
3. Do not invent files, functions, or code.
4. When the question asks where something is implemented, give:
   - the file path
   - the function/class name
   - the line numbers
   - a short explanation
5. If the context genuinely does not contain the answer, say:
   "I cannot determine the answer from the provided repository context."
6. Be concise and technical.

Repository context:
{context}

User question:
{question}

Answer:
"""

        response = self.client.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"].strip()