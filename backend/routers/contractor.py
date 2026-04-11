from fastapi import APIRouter, Depends, HTTPException
import asyncpg

from database import get_pool
from models import Page, ContractorCreate, ContractorUpdate, ContractorResponse

router = APIRouter(prefix="/api/contractor", tags=["contractor"])


@router.get("", response_model=Page[ContractorResponse])
async def list_contractors(page: int = 1, size: int = 20, pool=Depends(get_pool)):
    offset = (page - 1) * size
    async with pool.acquire() as conn:
        total = await conn.fetchval("SELECT COUNT(*) FROM contractor")
        rows = await conn.fetch(
            "SELECT * FROM contractor ORDER BY contr_inn LIMIT $1 OFFSET $2",
            size, offset,
        )
    return {"total": total, "page": page, "size": size, "items": [dict(r) for r in rows]}


@router.get("/{contr_inn}", response_model=ContractorResponse)
async def get_contractor(contr_inn: str, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM contractor WHERE contr_inn = $1", contr_inn
        )
    if not row:
        raise HTTPException(404, "Contractor not found")
    return dict(row)


@router.post("", response_model=ContractorResponse, status_code=201)
async def create_contractor(data: ContractorCreate, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        try:
            row = await conn.fetchrow(
                "INSERT INTO contractor (contr_inn, contr_name, contr_address, contr_phone) "
                "VALUES ($1, $2, $3, $4) RETURNING *",
                data.contr_inn, data.contr_name, data.contr_address, data.contr_phone,
            )
        except asyncpg.UniqueViolationError:
            raise HTTPException(409, "Contractor already exists")
        except asyncpg.NotNullViolationError as e:
            raise HTTPException(422, str(e))
    return dict(row)


@router.put("/{contr_inn}", response_model=ContractorResponse)
async def update_contractor(contr_inn: str, data: ContractorUpdate, pool=Depends(get_pool)):
    updates = data.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(400, "No fields to update")
    cols, vals = list(updates.keys()), list(updates.values())
    set_clause = ", ".join(f"{c} = ${i + 2}" for i, c in enumerate(cols))
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            f"UPDATE contractor SET {set_clause} WHERE contr_inn = $1 RETURNING *",
            contr_inn, *vals,
        )
    if not row:
        raise HTTPException(404, "Contractor not found")
    return dict(row)


@router.delete("/{contr_inn}", status_code=204)
async def delete_contractor(contr_inn: str, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM contractor WHERE contr_inn = $1", contr_inn
        )
    if result == "DELETE 0":
        raise HTTPException(404, "Contractor not found")
