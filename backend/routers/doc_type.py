from fastapi import APIRouter, Depends, HTTPException
import asyncpg

from database import get_pool
from models import Page, DocTypeCreate, DocTypeUpdate, DocTypeResponse

router = APIRouter(prefix="/api/doc-type", tags=["doc_type"])


@router.get("", response_model=Page[DocTypeResponse])
async def list_doc_types(page: int = 1, size: int = 20, pool=Depends(get_pool)):
    offset = (page - 1) * size
    async with pool.acquire() as conn:
        total = await conn.fetchval("SELECT COUNT(*) FROM doc_type")
        rows = await conn.fetch(
            "SELECT * FROM doc_type ORDER BY type_id LIMIT $1 OFFSET $2",
            size, offset,
        )
    return {"total": total, "page": page, "size": size, "items": [dict(r) for r in rows]}


@router.get("/{type_id}", response_model=DocTypeResponse)
async def get_doc_type(type_id: int, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM doc_type WHERE type_id = $1", type_id
        )
    if not row:
        raise HTTPException(404, "Document type not found")
    return dict(row)


@router.post("", response_model=DocTypeResponse, status_code=201)
async def create_doc_type(data: DocTypeCreate, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        try:
            row = await conn.fetchrow(
                "INSERT INTO doc_type (type_id, type_name, retention_years, requires_approval) "
                "VALUES ($1, $2, $3, $4) RETURNING *",
                data.type_id, data.type_name, data.retention_years, data.requires_approval,
            )
        except asyncpg.UniqueViolationError:
            raise HTTPException(409, "Document type already exists")
        except (asyncpg.CheckViolationError, asyncpg.NotNullViolationError) as e:
            raise HTTPException(422, str(e))
    return dict(row)


@router.put("/{type_id}", response_model=DocTypeResponse)
async def update_doc_type(type_id: int, data: DocTypeUpdate, pool=Depends(get_pool)):
    updates = data.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(400, "No fields to update")
    cols, vals = list(updates.keys()), list(updates.values())
    set_clause = ", ".join(f"{c} = ${i + 2}" for i, c in enumerate(cols))
    async with pool.acquire() as conn:
        try:
            row = await conn.fetchrow(
                f"UPDATE doc_type SET {set_clause} WHERE type_id = $1 RETURNING *",
                type_id, *vals,
            )
        except (asyncpg.CheckViolationError, asyncpg.NotNullViolationError) as e:
            raise HTTPException(422, str(e))
    if not row:
        raise HTTPException(404, "Document type not found")
    return dict(row)


@router.delete("/{type_id}", status_code=204)
async def delete_doc_type(type_id: int, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM doc_type WHERE type_id = $1", type_id
        )
    if result == "DELETE 0":
        raise HTTPException(404, "Document type not found")
