import ollama

context = """
File: scripts/daily_report.py
Lines: 13-22
Function: generate_report

Code:
def generate_report() -> str:
    db: Session = SessionLocal()
    try:
        total = db.query(models.Item).count()
        active = db.query(models.Item).filter(models.Item.is_active.is_(True)).count()
        inactive = total - active
    finally:
        db.close()

    return f"Items report -> total: {total}, active: {active}, inactive: {inactive}"
"""

question = "Where is the scheduled report implemented?"

prompt = f"""
Answer the question using ONLY the repository context below.

Repository context:
{context}

Question:
{question}

The answer is clearly present in the context.
Give the file path, function name, line numbers, and a short explanation.
Do not refuse to answer.

Answer:
"""

response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
)

print(response["message"]["content"])