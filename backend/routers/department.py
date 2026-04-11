from fastapi import APIRouter, Depends, HTTPException
import asyncpg

from database import get_pool
from models import Page, DepartmentCreate, DepartmentUpdate, DepartmentResponse

router = APIRouter(prefix="/api/department", tags=["department"])

_SELECT = """
    SELECT
        d.*,
        e.last_name || ' ' || e.first_name AS head_emp_name
    FROM department d
    LEFT JOIN employee e ON d.head_emp_id = e.emp_id
"""


@router.get("", response_model=Page[DepartmentResponse])
async def list_departments(page: int = 1, size: int = 20, pool=Depends(get_pool)):
    offset = (page - 1) * size
    async with pool.acquire() as conn:
        total = await conn.fetchval("SELECT COUNT(*) FROM department")
        rows = await conn.fetch(
            _SELECT + " ORDER BY d.dept_id LIMIT $1 OFFSET $2",
            size, offset,
        )
    return {"total": total, "page": page, "size": size, "items": [dict(r) for r in rows]}


@router.get("/{dept_id}", response_model=DepartmentResponse)
async def get_department(dept_id: int, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            _SELECT + " WHERE d.dept_id = $1", dept_id
        )
    if not row:
        raise HTTPException(404, "Department not found")
    return dict(row)


@router.post("", response_model=DepartmentResponse, status_code=201)
async def create_department(data: DepartmentCreate, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        try:
            await conn.execute(
                """INSERT INTO department
                   (dept_id, dept_name, emp_count, floor_num, room_num,
                    dept_phone, dept_email, created_date, head_emp_id, head_appoint_date)
                   VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)""",
                data.dept_id, data.dept_name, data.emp_count, data.floor_num,
                data.room_num, data.dept_phone, data.dept_email, data.created_date,
                data.head_emp_id, data.head_appoint_date,
            )
        except asyncpg.UniqueViolationError:
            raise HTTPException(409, "Department already exists")
        except asyncpg.ForeignKeyViolationError as e:
            raise HTTPException(422, f"Foreign key violation: {e}")
        except (asyncpg.CheckViolationError, asyncpg.NotNullViolationError) as e:
            raise HTTPException(422, str(e))
        row = await conn.fetchrow(_SELECT + " WHERE d.dept_id = $1", data.dept_id)
    return dict(row)


@router.put("/{dept_id}", response_model=DepartmentResponse)
async def update_department(dept_id: int, data: DepartmentUpdate, pool=Depends(get_pool)):
    updates = data.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(400, "No fields to update")
    cols, vals = list(updates.keys()), list(updates.values())
    set_clause = ", ".join(f"{c} = ${i + 2}" for i, c in enumerate(cols))
    async with pool.acquire() as conn:
        try:
            result = await conn.execute(
                f"UPDATE department SET {set_clause} WHERE dept_id = $1",
                dept_id, *vals,
            )
        except asyncpg.ForeignKeyViolationError as e:
            raise HTTPException(422, f"Foreign key violation: {e}")
        except (asyncpg.CheckViolationError, asyncpg.NotNullViolationError) as e:
            raise HTTPException(422, str(e))
        if result == "UPDATE 0":
            raise HTTPException(404, "Department not found")
        row = await conn.fetchrow(_SELECT + " WHERE d.dept_id = $1", dept_id)
    return dict(row)


@router.delete("/{dept_id}", status_code=204)
async def delete_department(dept_id: int, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        try:
            result = await conn.execute(
                "DELETE FROM department WHERE dept_id = $1", dept_id
            )
        except asyncpg.ForeignKeyViolationError as e:
            raise HTTPException(409, f"Cannot delete: referenced by other records")
    if result == "DELETE 0":
        raise HTTPException(404, "Department not found")
