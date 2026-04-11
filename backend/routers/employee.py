from fastapi import APIRouter, Depends, HTTPException
import asyncpg

from database import get_pool
from models import Page, EmployeeCreate, EmployeeUpdate, EmployeeResponse

router = APIRouter(prefix="/api/employee", tags=["employee"])

_SELECT = """
    SELECT
        e.*,
        d.dept_name,
        p.position_name
    FROM employee e
    LEFT JOIN department d ON e.dept_id = d.dept_id
    LEFT JOIN position p ON e.position_id = p.position_id
"""


@router.get("", response_model=Page[EmployeeResponse])
async def list_employees(page: int = 1, size: int = 20, pool=Depends(get_pool)):
    offset = (page - 1) * size
    async with pool.acquire() as conn:
        total = await conn.fetchval("SELECT COUNT(*) FROM employee")
        rows = await conn.fetch(
            _SELECT + " ORDER BY e.emp_id LIMIT $1 OFFSET $2",
            size, offset,
        )
    return {"total": total, "page": page, "size": size, "items": [dict(r) for r in rows]}


@router.get("/{emp_id}", response_model=EmployeeResponse)
async def get_employee(emp_id: int, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        row = await conn.fetchrow(_SELECT + " WHERE e.emp_id = $1", emp_id)
    if not row:
        raise HTTPException(404, "Employee not found")
    return dict(row)


@router.post("", response_model=EmployeeResponse, status_code=201)
async def create_employee(data: EmployeeCreate, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        try:
            await conn.execute(
                """INSERT INTO employee
                   (emp_id, dept_id, last_name, first_name, middle_name, position_id,
                    salary, hire_date, birth_date, education, inn, snils, emp_phone, emp_email)
                   VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14)""",
                data.emp_id, data.dept_id, data.last_name, data.first_name,
                data.middle_name, data.position_id, data.salary, data.hire_date,
                data.birth_date, data.education, data.inn, data.snils,
                data.emp_phone, data.emp_email,
            )
        except asyncpg.UniqueViolationError as e:
            raise HTTPException(409, f"Unique constraint violation: {e.detail}")
        except asyncpg.ForeignKeyViolationError as e:
            raise HTTPException(422, f"Foreign key violation: {e}")
        except (asyncpg.CheckViolationError, asyncpg.NotNullViolationError) as e:
            raise HTTPException(422, str(e))
        row = await conn.fetchrow(_SELECT + " WHERE e.emp_id = $1", data.emp_id)
    return dict(row)


@router.put("/{emp_id}", response_model=EmployeeResponse)
async def update_employee(emp_id: int, data: EmployeeUpdate, pool=Depends(get_pool)):
    updates = data.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(400, "No fields to update")
    cols, vals = list(updates.keys()), list(updates.values())
    set_clause = ", ".join(f"{c} = ${i + 2}" for i, c in enumerate(cols))
    async with pool.acquire() as conn:
        try:
            result = await conn.execute(
                f"UPDATE employee SET {set_clause} WHERE emp_id = $1",
                emp_id, *vals,
            )
        except asyncpg.UniqueViolationError as e:
            raise HTTPException(409, f"Unique constraint violation: {e.detail}")
        except asyncpg.ForeignKeyViolationError as e:
            raise HTTPException(422, f"Foreign key violation: {e}")
        except (asyncpg.CheckViolationError, asyncpg.NotNullViolationError) as e:
            raise HTTPException(422, str(e))
        if result == "UPDATE 0":
            raise HTTPException(404, "Employee not found")
        row = await conn.fetchrow(_SELECT + " WHERE e.emp_id = $1", emp_id)
    return dict(row)


@router.delete("/{emp_id}", status_code=204)
async def delete_employee(emp_id: int, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        try:
            result = await conn.execute(
                "DELETE FROM employee WHERE emp_id = $1", emp_id
            )
        except asyncpg.ForeignKeyViolationError:
            raise HTTPException(409, "Cannot delete: referenced by other records")
    if result == "DELETE 0":
        raise HTTPException(404, "Employee not found")
