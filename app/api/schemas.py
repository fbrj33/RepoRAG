from pydantic import BaseModel, Field


class IndexRepositoryRequest(BaseModel):
    repo_url: str = Field(
        min_length=1
    )


class IndexRepositoryResponse(BaseModel):
    repository_id: str
    repository_url: str
    repository_path: str
    index_path: str
    status: str
    files: int
    chunks: int


class AskRequest(BaseModel):
    repository_id: str = Field(
        min_length=1
    )

    question: str = Field(
        min_length=1
    )


class SourceResponse(BaseModel):
    file: str
    type: str
    name: str | None
    start_line: int
    end_line: int
    score: float


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]