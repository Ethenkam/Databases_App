from fastapi import APIRouter, Depends, HTTPException
import asyncpg

from database import get_pool
from models import Page, PositionCreate, PositionUpdate, PositionResponse

router = APIRouter(prefix="/api/position", tags=["position"])


@router.get("", response_model=Page[PositionResponse])
async def list_positions(page: int = 1, size: int = 20, pool=Depends(get_pool)):
    offset = (page - 1) * size
    async with pool.acquire() as conn:
        total = await conn.fetchval("SELECT COUNT(*) FROM position")
        rows = await conn.fetch(
            "SELECT * FROM position ORDER BY position_id LIMIT $1 OFFSET $2",
            size, offset,
        )
    return {"total": total, "page": page, "size": size, "items": [dict(r) for r in rows]}


@router.get("/{position_id}", response_model=PositionResponse)
async def get_position(position_id: int, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM position WHERE position_id = $1", position_id
        )
    if not row:
        raise HTTPException(404, "Position not found")
    return dict(row)


@router.post("", response_model=PositionResponse, status_code=201)
async def create_position(data: PositionCreate, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        try:
            row = await conn.fetchrow(
                "INSERT INTO position (position_id, position_name, position_grade, min_salary) "
                "VALUES ($1, $2, $3, $4) RETURNING *",
                data.position_id, data.position_name, data.position_grade, data.min_salary,
            )
        except asyncpg.UniqueViolationError:
            raise HTTPException(409, "Position already exists")
        except (asyncpg.CheckViolationError, asyncpg.NotNullViolationError) as e:
            raise HTTPException(422, str(e))
    return dict(row)


@router.put("/{position_id}", response_model=PositionResponse)
async def update_position(position_id: int, data: PositionUpdate, pool=Depends(get_pool)):
    updates = data.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(400, "No fields to update")
    cols, vals = list(updates.keys()), list(updates.values())
    set_clause = ", ".join(f"{c} = ${i + 2}" for i, c in enumerate(cols))
    async with pool.acquire() as conn:
        try:
            row = await conn.fetchrow(
                f"UPDATE position SET {set_clause} WHERE position_id = $1 RETURNING *",
                position_id, *vals,
            )
        except (asyncpg.CheckViolationError, asyncpg.NotNullViolationError) as e:
            raise HTTPException(422, str(e))
    if not row:
        raise HTTPException(404, "Position not found")
    return dict(row)


@router.delete("/{position_id}", status_code=204)
async def delete_position(position_id: int, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM position WHERE position_id = $1", position_id
        )
    if result == "DELETE 0":
        raise HTTPException(404, "Position not found")
