import ollama


class CodeGenerator:
    """Generate grounded answers using a local LLM."""

    def __init__(
        self,
        model_name: str = "llama3.2:3b",
    ):
        self.model_name = model_name

    def generate(
        self,
        question: str,
        context: str,
    ) -> str:
        """Generate an answer using retrieved repository context."""

        prompt = f"""
You are RepoRAG, an AI assistant specialized in
understanding software repositories.

Answer the user's question using ONLY the provided
repository context.

Rules:
- Do not invent code or files.
- If a retrieved source contains a file or function that
    directly matches the question, answer from that source.
- Only say that you cannot determine the answer when no
    retrieved source is relevant.
- Mention the relevant file and line numbers when available.
- Explain your reasoning briefly.
- Keep the answer concise and technical.

USER QUESTION:
{question}

REPOSITORY CONTEXT:
{context}

ANSWER:
"""

        response = ollama.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]