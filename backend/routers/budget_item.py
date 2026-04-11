from fastapi import APIRouter, Depends, HTTPException
import asyncpg

from database import get_pool
from models import Page, BudgetItemCreate, BudgetItemUpdate, BudgetItemResponse

router = APIRouter(prefix="/api/budget-item", tags=["budget_item"])


@router.get("", response_model=Page[BudgetItemResponse])
async def list_budget_items(page: int = 1, size: int = 20, pool=Depends(get_pool)):
    offset = (page - 1) * size
    async with pool.acquire() as conn:
        total = await conn.fetchval("SELECT COUNT(*) FROM budget_item")
        rows = await conn.fetch(
            "SELECT * FROM budget_item ORDER BY item_id LIMIT $1 OFFSET $2",
            size, offset,
        )
    return {"total": total, "page": page, "size": size, "items": [dict(r) for r in rows]}


@router.get("/{item_id}", response_model=BudgetItemResponse)
async def get_budget_item(item_id: int, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM budget_item WHERE item_id = $1", item_id
        )
    if not row:
        raise HTTPException(404, "Budget item not found")
    return dict(row)


@router.post("", response_model=BudgetItemResponse, status_code=201)
async def create_budget_item(data: BudgetItemCreate, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        try:
            row = await conn.fetchrow(
                "INSERT INTO budget_item (item_id, item_name, item_category) "
                "VALUES ($1, $2, $3) RETURNING *",
                data.item_id, data.item_name, data.item_category,
            )
        except asyncpg.UniqueViolationError:
            raise HTTPException(409, "Budget item already exists")
        except asyncpg.NotNullViolationError as e:
            raise HTTPException(422, str(e))
    return dict(row)


@router.put("/{item_id}", response_model=BudgetItemResponse)
async def update_budget_item(item_id: int, data: BudgetItemUpdate, pool=Depends(get_pool)):
    updates = data.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(400, "No fields to update")
    cols, vals = list(updates.keys()), list(updates.values())
    set_clause = ", ".join(f"{c} = ${i + 2}" for i, c in enumerate(cols))
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            f"UPDATE budget_item SET {set_clause} WHERE item_id = $1 RETURNING *",
            item_id, *vals,
        )
    if not row:
        raise HTTPException(404, "Budget item not found")
    return dict(row)


@router.delete("/{item_id}", status_code=204)
async def delete_budget_item(item_id: int, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM budget_item WHERE item_id = $1", item_id
        )
    if result == "DELETE 0":
        raise HTTPException(404, "Budget item not found")
