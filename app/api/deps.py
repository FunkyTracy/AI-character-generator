from fastapi import HTTPException, Request

from ..database.neo4j_connection import Neo4jDB


def get_db(request: Request) -> Neo4jDB:
    db = request.app.state.db
    if db is None:
        detail = request.app.state.db_error or "Neo4j is not connected"
        raise HTTPException(status_code=503, detail=detail)
    return db
