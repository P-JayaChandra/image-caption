"""
Caption History and Search Endpoints
"""
from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(prefix="/api/v1/history", tags=["History"])

@router.get("")
async def get_history(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    style: Optional[str] = None
):
    return {
        "status": "success",
        "limit": limit,
        "offset": offset,
        "total": 0,
        "records": []
    }
