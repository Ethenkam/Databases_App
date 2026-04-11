from fastapi import APIRouter, Depends, HTTPException
import asyncpg

from database import get_pool
from models import Page, BudgetCreate, BudgetUpdate, BudgetResponse

router = APIRouter(prefix="/api/budget", tags=["budget"])

_SELECT = """
    SELECT
        b.*,
        d.dept_name,
        bi.item_name
    FROM budget b
    LEFT JOIN department d ON b.dept_id = d.dept_id
    LEFT JOIN budget_item bi ON b.item_id = bi.item_id
"""

_PK_WHERE = " WHERE b.dept_id=$1 AND b.item_id=$2 AND b.budget_year=$3 AND b.budget_quarter=$4"


@router.get("", response_model=Page[BudgetResponse])
async def list_budgets(page: int = 1, size: int = 20, pool=Depends(get_pool)):
    offset = (page - 1) * size
    async with pool.acquire() as conn:
        total = await conn.fetchval("SELECT COUNT(*) FROM budget")
        rows = await conn.fetch(
            _SELECT + " ORDER BY b.dept_id, b.item_id, b.budget_year, b.budget_quarter"
                      " LIMIT $1 OFFSET $2",
            size, offset,
        )
    return {"total": total, "page": page, "size": size, "items": [dict(r) for r in rows]}


@router.get("/{dept_id}/{item_id}/{year}/{quarter}", response_model=BudgetResponse)
async def get_budget(dept_id: int, item_id: int, year: int, quarter: int, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        row = await conn.fetchrow(_SELECT + _PK_WHERE, dept_id, item_id, year, quarter)
    if not row:
        raise HTTPException(404, "Budget record not found")
    return dict(row)


@router.post("", response_model=BudgetResponse, status_code=201)
async def create_budget(data: BudgetCreate, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        try:
            await conn.execute(
                """INSERT INTO budget
                   (dept_id, item_id, budget_year, budget_quarter, plan_rub, fact_rub, approved_date)
                   VALUES ($1,$2,$3,$4,$5,$6,$7)""",
                data.dept_id, data.item_id, data.budget_year, data.budget_quarter,
                data.plan_rub, data.fact_rub, data.approved_date,
            )
        except asyncpg.UniqueViolationError:
            raise HTTPException(409, "Budget record already exists")
        except asyncpg.ForeignKeyViolationError as e:
            raise HTTPException(422, f"Foreign key violation: {e}")
        except (asyncpg.CheckViolationError, asyncpg.NotNullViolationError) as e:
            raise HTTPException(422, str(e))
        row = await conn.fetchrow(
            _SELECT + _PK_WHERE,
            data.dept_id, data.item_id, data.budget_year, data.budget_quarter,
        )
    return dict(row)


@router.put("/{dept_id}/{item_id}/{year}/{quarter}", response_model=BudgetResponse)
async def update_budget(
    dept_id: int, item_id: int, year: int, quarter: int,
    data: BudgetUpdate,
    pool=Depends(get_pool),
):
    updates = data.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(400, "No fields to update")
    cols, vals = list(updates.keys()), list(updates.values())
    # PK occupies $1..$4, update values start at $5
    set_clause = ", ".join(f"{c} = ${i + 5}" for i, c in enumerate(cols))
    async with pool.acquire() as conn:
        try:
            result = await conn.execute(
                f"UPDATE budget SET {set_clause}"
                " WHERE dept_id=$1 AND item_id=$2 AND budget_year=$3 AND budget_quarter=$4",
                dept_id, item_id, year, quarter, *vals,
            )
        except (asyncpg.CheckViolationError, asyncpg.NotNullViolationError) as e:
            raise HTTPException(422, str(e))
        if result == "UPDATE 0":
            raise HTTPException(404, "Budget record not found")
        row = await conn.fetchrow(_SELECT + _PK_WHERE, dept_id, item_id, year, quarter)
    return dict(row)


@router.delete("/{dept_id}/{item_id}/{year}/{quarter}", status_code=204)
async def delete_budget(
    dept_id: int, item_id: int, year: int, quarter: int, pool=Depends(get_pool)
):
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM budget"
            " WHERE dept_id=$1 AND item_id=$2 AND budget_year=$3 AND budget_quarter=$4",
            dept_id, item_id, year, quarter,
        )
    if result == "DELETE 0":
        raise HTTPException(404, "Budget record not found")
