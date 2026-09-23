from fastapi import FastAPI 
from app.api.routes import router 

app = FastAPI(
    title="RepoRAG",
    description=(
        "AI-powered codebase understanding "
        "and debugging assistant."
    ),
    version="1.0.0",
)

app.include_router(router)