from fastapi import APIRouter, HTTPException
from app.api.schemas import(
    AskRequest,
    AskResponse,
    IndexRepositoryRequest,
    IndexRepositoryResponse,
    SourceResponse,

)
from app.rag.generator import CodeGenerator
from app.rag.pipeline import RetrievalPipeline
from app.rag.rag_pipeline import RagPipeline
from app.rag.reranker import CodeReranker
from app.repository.service import ( RepositoryService,)

router=APIRouter()
repository_service = RepositoryService()
reranker = CodeReranker()
generator = CodeGenerator()

@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "RepoRAG",
    }


@router.post(
    "/repositories/index",
    response_model=IndexRepositoryResponse,
)
def index_repository(
    request: IndexRepositoryRequest,
):
    try:
        return repository_service.index_repository(
            request.repo_url
        )

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.post(
    "/ask",
    response_model=AskResponse,
)
def ask_repository(
    request: AskRequest,
):

    try:
        repository_index = (
            repository_service.get_index(
                request.repository_id
            )
        )

        retrieval_pipeline = (
            RetrievalPipeline(
                repository_index=repository_index,
                reranker=reranker,
            )
        )

        rag_pipeline = RagPipeline(
            retrieval_pipeline=retrieval_pipeline,
            generator=generator,
        )

        result = rag_pipeline.answer(
            question=request.question,
            candidate_k=10,
            top_k=5,
        )
        print("\n===== RETRIEVED SOURCES =====")

        for source in result["sources"]:
             print(
             source["file_path"],
             source["name"],
             source["start_line"],
             source["end_line"],
             source["rerank_score"],
    )

        print("\n===== CONTEXT =====")
        print(result["context"])

        print("\n===== ANSWER =====")
        print(result["answer"])
        

        sources = []

        for source in result["sources"]:
            sources.append(
                SourceResponse(
                    file=source["file_path"],
                    type=source["type"],
                    name=source["name"],
                    start_line=source["start_line"],
                    end_line=source["end_line"],
                    score=source[
                        "rerank_score"
                    ],
                )
            )

        return AskResponse(
            answer=result["answer"],
            sources=sources,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc