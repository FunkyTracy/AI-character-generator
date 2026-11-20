from fastapi import APIRouter, Request

from ..models.world_elements import ontology_catalog

router = APIRouter(tags=["meta"])


@router.get("/health")
def health(request: Request):
    return {
        "ok": request.app.state.db is not None,
        "error": request.app.state.db_error,
    }


@router.get("/ontology")
def ontology():
    return ontology_catalog()
