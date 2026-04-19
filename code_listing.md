# Code Listing

## backend/database.py

```py
import asyncpg

_pool: asyncpg.Pool | None = None


async def init_pool() -> None:
    global _pool
    _pool = await asyncpg.create_pool(
        host="localhost",
        port=5432,
        user="postgres",
        password="3570",
        database="Laba3",
        min_size=2,
        max_size=10,
    )


async def close_pool() -> None:
    global _pool
    if _pool:
        await _pool.close()
        _pool = None


def get_pool() -> asyncpg.Pool:
    return _pool

```

## backend/main.py

```py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_pool, close_pool
from routers import position, budget_item, contractor, doc_type, department, employee, budget, document, olap, export


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_pool()
    yield
    await close_pool()


app = FastAPI(title="Laba3 API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for _router in [
    position.router,
    budget_item.router,
    contractor.router,
    doc_type.router,
    department.router,
    employee.router,
    budget.router,
    document.router,
    olap.router,
    export.router,
]:
    app.include_router(_router)

```

## backend/models.py

```py
from pydantic import BaseModel
from typing import Generic, List, Optional, TypeVar
from datetime import date
from decimal import Decimal

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    total: int
    page: int
    size: int
    items: List[T]


# ── Position ──────────────────────────────────────────────────────────────────

class PositionCreate(BaseModel):
    position_id: int
    position_name: str
    position_grade: Optional[str] = None
    min_salary: Decimal


class PositionUpdate(BaseModel):
    position_name: Optional[str] = None
    position_grade: Optional[str] = None
    min_salary: Optional[Decimal] = None


class PositionResponse(BaseModel):
    position_id: int
    position_name: str
    position_grade: Optional[str] = None
    min_salary: Decimal

    model_config = {"from_attributes": True}


# ── BudgetItem ────────────────────────────────────────────────────────────────

class BudgetItemCreate(BaseModel):
    item_id: int
    item_name: str
    item_category: Optional[str] = None


class BudgetItemUpdate(BaseModel):
    item_name: Optional[str] = None
    item_category: Optional[str] = None


class BudgetItemResponse(BaseModel):
    item_id: int
    item_name: str
    item_category: Optional[str] = None

    model_config = {"from_attributes": True}


# ── Contractor ────────────────────────────────────────────────────────────────

class ContractorCreate(BaseModel):
    contr_inn: str
    contr_name: str
    contr_address: Optional[str] = None
    contr_phone: Optional[str] = None


class ContractorUpdate(BaseModel):
    contr_name: Optional[str] = None
    contr_address: Optional[str] = None
    contr_phone: Optional[str] = None


class ContractorResponse(BaseModel):
    contr_inn: str
    contr_name: str
    contr_address: Optional[str] = None
    contr_phone: Optional[str] = None

    model_config = {"from_attributes": True}


# ── DocType ───────────────────────────────────────────────────────────────────

class DocTypeCreate(BaseModel):
    type_id: int
    type_name: str
    retention_years: int
    requires_approval: bool = False


class DocTypeUpdate(BaseModel):
    type_name: Optional[str] = None
    retention_years: Optional[int] = None
    requires_approval: Optional[bool] = None


class DocTypeResponse(BaseModel):
    type_id: int
    type_name: str
    retention_years: int
    requires_approval: bool

    model_config = {"from_attributes": True}


# ── Department ────────────────────────────────────────────────────────────────

class DepartmentCreate(BaseModel):
    dept_id: int
    dept_name: str
    emp_count: int = 0
    floor_num: Optional[int] = None
    room_num: Optional[str] = None
    dept_phone: Optional[str] = None
    dept_email: Optional[str] = None
    created_date: Optional[date] = None
    head_emp_id: Optional[int] = None
    head_appoint_date: Optional[date] = None


class DepartmentUpdate(BaseModel):
    dept_name: Optional[str] = None
    emp_count: Optional[int] = None
    floor_num: Optional[int] = None
    room_num: Optional[str] = None
    dept_phone: Optional[str] = None
    dept_email: Optional[str] = None
    created_date: Optional[date] = None
    head_emp_id: Optional[int] = None
    head_appoint_date: Optional[date] = None


class DepartmentResponse(BaseModel):
    dept_id: int
    dept_name: str
    emp_count: int
    floor_num: Optional[int] = None
    room_num: Optional[str] = None
    dept_phone: Optional[str] = None
    dept_email: Optional[str] = None
    created_date: Optional[date] = None
    head_emp_id: Optional[int] = None
    head_appoint_date: Optional[date] = None
    head_emp_name: Optional[str] = None

    model_config = {"from_attributes": True}


# ── Employee ──────────────────────────────────────────────────────────────────

class EmployeeCreate(BaseModel):
    emp_id: int
    dept_id: int
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    position_id: int
    salary: Decimal
    hire_date: date
    birth_date: Optional[date] = None
    education: Optional[str] = None
    inn: Optional[str] = None
    snils: Optional[str] = None
    emp_phone: Optional[str] = None
    emp_email: Optional[str] = None


class EmployeeUpdate(BaseModel):
    dept_id: Optional[int] = None
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    position_id: Optional[int] = None
    salary: Optional[Decimal] = None
    hire_date: Optional[date] = None
    birth_date: Optional[date] = None
    education: Optional[str] = None
    inn: Optional[str] = None
    snils: Optional[str] = None
    emp_phone: Optional[str] = None
    emp_email: Optional[str] = None


class EmployeeResponse(BaseModel):
    emp_id: int
    dept_id: int
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    position_id: int
    salary: Decimal
    hire_date: date
    birth_date: Optional[date] = None
    education: Optional[str] = None
    inn: Optional[str] = None
    snils: Optional[str] = None
    emp_phone: Optional[str] = None
    emp_email: Optional[str] = None
    dept_name: Optional[str] = None
    position_name: Optional[str] = None

    model_config = {"from_attributes": True}


# ── Budget ────────────────────────────────────────────────────────────────────

class BudgetCreate(BaseModel):
    dept_id: int
    item_id: int
    budget_year: int
    budget_quarter: int
    plan_rub: Decimal
    fact_rub: Decimal
    approved_date: Optional[date] = None


class BudgetUpdate(BaseModel):
    plan_rub: Optional[Decimal] = None
    fact_rub: Optional[Decimal] = None
    approved_date: Optional[date] = None


class BudgetResponse(BaseModel):
    dept_id: int
    item_id: int
    budget_year: int
    budget_quarter: int
    plan_rub: Decimal
    fact_rub: Decimal
    approved_date: Optional[date] = None
    dept_name: Optional[str] = None
    item_name: Optional[str] = None

    model_config = {"from_attributes": True}


# ── Document ──────────────────────────────────────────────────────────────────

class DocumentCreate(BaseModel):
    doc_id: int
    dept_id: int
    item_id: int
    type_id: int
    doc_date: date
    doc_amount: Optional[Decimal] = None
    contr_inn: Optional[str] = None
    resp_emp_id: int


class DocumentUpdate(BaseModel):
    dept_id: Optional[int] = None
    item_id: Optional[int] = None
    type_id: Optional[int] = None
    doc_date: Optional[date] = None
    doc_amount: Optional[Decimal] = None
    contr_inn: Optional[str] = None
    resp_emp_id: Optional[int] = None


class DocumentResponse(BaseModel):
    doc_id: int
    dept_id: int
    item_id: int
    type_id: int
    doc_date: date
    doc_amount: Optional[Decimal] = None
    contr_inn: Optional[str] = None
    resp_emp_id: int
    dept_name: Optional[str] = None
    item_name: Optional[str] = None
    type_name: Optional[str] = None
    contr_name: Optional[str] = None
    resp_emp_name: Optional[str] = None

    model_config = {"from_attributes": True}

```

## backend/routers/__init__.py

```py

```

## backend/routers/budget.py

```py
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

```

## backend/routers/budget_item.py

```py
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

```

## backend/routers/contractor.py

```py
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

```

## backend/routers/department.py

```py
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

```

## backend/routers/doc_type.py

```py
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

```

## backend/routers/document.py

```py
from fastapi import APIRouter, Depends, HTTPException
import asyncpg

from database import get_pool
from models import Page, DocumentCreate, DocumentUpdate, DocumentResponse

router = APIRouter(prefix="/api/document", tags=["document"])

_SELECT = """
    SELECT
        doc.*,
        d.dept_name,
        bi.item_name,
        dt.type_name,
        c.contr_name,
        e.last_name || ' ' || e.first_name AS resp_emp_name
    FROM document doc
    LEFT JOIN department d    ON doc.dept_id     = d.dept_id
    LEFT JOIN budget_item bi  ON doc.item_id     = bi.item_id
    LEFT JOIN doc_type dt     ON doc.type_id     = dt.type_id
    LEFT JOIN contractor c    ON doc.contr_inn   = c.contr_inn
    LEFT JOIN employee e      ON doc.resp_emp_id = e.emp_id
"""


@router.get("", response_model=Page[DocumentResponse])
async def list_documents(page: int = 1, size: int = 20, pool=Depends(get_pool)):
    offset = (page - 1) * size
    async with pool.acquire() as conn:
        total = await conn.fetchval("SELECT COUNT(*) FROM document")
        rows = await conn.fetch(
            _SELECT + " ORDER BY doc.doc_id LIMIT $1 OFFSET $2",
            size, offset,
        )
    return {"total": total, "page": page, "size": size, "items": [dict(r) for r in rows]}


@router.get("/{doc_id}", response_model=DocumentResponse)
async def get_document(doc_id: int, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        row = await conn.fetchrow(_SELECT + " WHERE doc.doc_id = $1", doc_id)
    if not row:
        raise HTTPException(404, "Document not found")
    return dict(row)


@router.post("", response_model=DocumentResponse, status_code=201)
async def create_document(data: DocumentCreate, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        try:
            await conn.execute(
                """INSERT INTO document
                   (doc_id, dept_id, item_id, type_id, doc_date,
                    doc_amount, contr_inn, resp_emp_id)
                   VALUES ($1,$2,$3,$4,$5,$6,$7,$8)""",
                data.doc_id, data.dept_id, data.item_id, data.type_id,
                data.doc_date, data.doc_amount, data.contr_inn, data.resp_emp_id,
            )
        except asyncpg.UniqueViolationError:
            raise HTTPException(409, "Document already exists")
        except asyncpg.ForeignKeyViolationError as e:
            raise HTTPException(422, f"Foreign key violation: {e}")
        except (asyncpg.CheckViolationError, asyncpg.NotNullViolationError) as e:
            raise HTTPException(422, str(e))
        row = await conn.fetchrow(_SELECT + " WHERE doc.doc_id = $1", data.doc_id)
    return dict(row)


@router.put("/{doc_id}", response_model=DocumentResponse)
async def update_document(doc_id: int, data: DocumentUpdate, pool=Depends(get_pool)):
    updates = data.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(400, "No fields to update")
    cols, vals = list(updates.keys()), list(updates.values())
    set_clause = ", ".join(f"{c} = ${i + 2}" for i, c in enumerate(cols))
    async with pool.acquire() as conn:
        try:
            result = await conn.execute(
                f"UPDATE document SET {set_clause} WHERE doc_id = $1",
                doc_id, *vals,
            )
        except asyncpg.ForeignKeyViolationError as e:
            raise HTTPException(422, f"Foreign key violation: {e}")
        except (asyncpg.CheckViolationError, asyncpg.NotNullViolationError) as e:
            raise HTTPException(422, str(e))
        if result == "UPDATE 0":
            raise HTTPException(404, "Document not found")
        row = await conn.fetchrow(_SELECT + " WHERE doc.doc_id = $1", doc_id)
    return dict(row)


@router.delete("/{doc_id}", status_code=204)
async def delete_document(doc_id: int, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM document WHERE doc_id = $1", doc_id
        )
    if result == "DELETE 0":
        raise HTTPException(404, "Document not found")

```

## backend/routers/employee.py

```py
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

```

## backend/routers/export.py

```py
import csv
import io
from decimal import Decimal
from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import Optional

from database import get_pool

router = APIRouter(prefix="/api/export", tags=["export"])

REPORT_QUERIES = {
    "rollup-by-dept": """
        SELECT
            d.dept_name                AS "Отдел",
            COALESCE(SUM(b.plan_rub), 0)  AS "План",
            COALESCE(SUM(b.fact_rub), 0)  AS "Факт",
            COALESCE(SUM(b.plan_rub), 0) - COALESCE(SUM(b.fact_rub), 0) AS "Отклонение",
            COUNT(DISTINCT doc.doc_id)     AS "Кол-во документов"
        FROM department d
        LEFT JOIN budget   b   ON b.dept_id = d.dept_id
        LEFT JOIN document doc ON doc.dept_id = d.dept_id
        GROUP BY d.dept_id, d.dept_name
        ORDER BY d.dept_name
    """,
    "rollup-by-item": """
        SELECT
            bi.item_name               AS "Статья",
            bi.item_category           AS "Категория",
            COALESCE(SUM(b.plan_rub), 0)  AS "План",
            COALESCE(SUM(b.fact_rub), 0)  AS "Факт",
            COALESCE(SUM(b.plan_rub), 0) - COALESCE(SUM(b.fact_rub), 0) AS "Отклонение",
            COUNT(DISTINCT doc.doc_id)     AS "Кол-во документов"
        FROM budget_item bi
        LEFT JOIN budget   b   ON b.item_id = bi.item_id
        LEFT JOIN document doc ON doc.item_id = bi.item_id
        GROUP BY bi.item_id, bi.item_name, bi.item_category
        ORDER BY bi.item_name
    """,
    "rollup-by-quarter": """
        SELECT
            b.budget_year              AS "Год",
            b.budget_quarter           AS "Квартал",
            COALESCE(SUM(b.plan_rub), 0) AS "План",
            COALESCE(SUM(b.fact_rub), 0) AS "Факт",
            COALESCE(SUM(b.plan_rub), 0) - COALESCE(SUM(b.fact_rub), 0) AS "Отклонение"
        FROM budget b
        GROUP BY b.budget_year, b.budget_quarter
        ORDER BY b.budget_year, b.budget_quarter
    """,
    "cross-dept-item": """
        SELECT
            d.dept_name                AS "Отдел",
            bi.item_name               AS "Статья",
            COALESCE(SUM(b.plan_rub), 0) AS "План",
            COALESCE(SUM(b.fact_rub), 0) AS "Факт",
            COALESCE(SUM(b.plan_rub), 0) - COALESCE(SUM(b.fact_rub), 0) AS "Отклонение"
        FROM budget b
        JOIN department  d  ON d.dept_id  = b.dept_id
        JOIN budget_item bi ON bi.item_id = b.item_id
        GROUP BY d.dept_id, d.dept_name, bi.item_id, bi.item_name
        ORDER BY d.dept_name, bi.item_name
    """,
    "slice-by-dept": """
        SELECT
            d.dept_name                AS "Отдел",
            doc.doc_id                 AS "Документ ID",
            dt.type_name               AS "Тип документа",
            bi.item_name               AS "Статья",
            doc.doc_date               AS "Дата",
            doc.doc_amount             AS "Сумма",
            c.contr_name               AS "Контрагент",
            e.last_name || ' ' || e.first_name AS "Ответственный"
        FROM document doc
        LEFT JOIN department  d  ON d.dept_id    = doc.dept_id
        LEFT JOIN doc_type   dt ON dt.type_id    = doc.type_id
        LEFT JOIN budget_item bi ON bi.item_id   = doc.item_id
        LEFT JOIN contractor  c  ON c.contr_inn   = doc.contr_inn
        LEFT JOIN employee   e  ON e.emp_id      = doc.resp_emp_id
        WHERE doc.dept_id = $1
        ORDER BY doc.doc_date DESC
    """,
    "slice-by-contractor": """
        SELECT
            c.contr_name               AS "Контрагент",
            doc.doc_id                 AS "Документ ID",
            d.dept_name                AS "Отдел",
            dt.type_name               AS "Тип документа",
            bi.item_name               AS "Статья",
            doc.doc_date               AS "Дата",
            doc.doc_amount             AS "Сумма",
            e.last_name || ' ' || e.first_name AS "Ответственный"
        FROM document doc
        LEFT JOIN department  d  ON d.dept_id    = doc.dept_id
        LEFT JOIN doc_type   dt ON dt.type_id    = doc.type_id
        LEFT JOIN budget_item bi ON bi.item_id   = doc.item_id
        LEFT JOIN contractor  c  ON c.contr_inn   = doc.contr_inn
        LEFT JOIN employee   e  ON e.emp_id      = doc.resp_emp_id
        WHERE doc.contr_inn = $1
        ORDER BY doc.doc_date DESC
    """,
}

PARAMETERISED_REPORTS = {"slice-by-dept", "slice-by-contractor"}


def _serialize(value):
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return value


async def _fetch_report(report_type: str, pool, dept_id=None, contr_inn=None):
    query = REPORT_QUERIES.get(report_type)
    if query is None:
        raise HTTPException(404, f"Unknown report type: {report_type}")

    params: list = []
    if report_type == "slice-by-dept":
        if dept_id is None:
            raise HTTPException(400, "dept_id is required for slice-by-dept")
        params.append(dept_id)
    elif report_type == "slice-by-contractor":
        if contr_inn is None:
            raise HTTPException(400, "contr_inn is required for slice-by-contractor")
        params.append(contr_inn)

    async with pool.acquire() as conn:
        rows = await conn.fetch(query, *params)

    return rows


def _rows_to_csv(rows) -> str:
    if not rows:
        return ""
    buf = io.StringIO()
    headers = list(rows[0].keys())
    writer = csv.writer(buf)
    writer.writerow(headers)
    for r in rows:
        writer.writerow([_serialize(r[h]) for h in headers])
    return buf.getvalue()


def _rows_to_xlsx(rows) -> bytes:
    from openpyxl import Workbook
    from openpyxl.utils import get_column_letter

    wb = Workbook()
    ws = wb.active
    if not rows:
        output = io.BytesIO()
        wb.save(output)
        return output.getvalue()

    headers = list(rows[0].keys())
    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.font = cell.font.copy(bold=True)

    for row_idx, r in enumerate(rows, 2):
        for col_idx, h in enumerate(headers, 1):
            ws.cell(row=row_idx, column=col_idx, value=_serialize(r[h]))

    for col_idx in range(1, len(headers) + 1):
        col_letter = get_column_letter(col_idx)
        max_len = max(
            len(str(ws.cell(row=r, column=col_idx).value or ""))
            for r in range(1, len(rows) + 2)
        )
        ws.column_dimensions[col_letter].width = min(max_len + 2, 50)

    output = io.BytesIO()
    wb.save(output)
    return output.getvalue()


@router.get("/{report_type}")
async def export_report(
    report_type: str,
    format: str = Query("csv", pattern="^(csv|xlsx)$"),
    dept_id: Optional[int] = None,
    contr_inn: Optional[str] = None,
    pool=Depends(get_pool),
):
    rows = await _fetch_report(report_type, pool, dept_id=dept_id, contr_inn=contr_inn)

    filename = f"{report_type}.{format}"

    if format == "csv":
        content = _rows_to_csv(rows)
        return StreamingResponse(
            io.StringIO(content),
            media_type="text/csv; charset=utf-8",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    xlsx_bytes = _rows_to_xlsx(rows)
    return StreamingResponse(
        io.BytesIO(xlsx_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )

```

## backend/routers/olap.py

```py
from fastapi import APIRouter, Depends, Query
from typing import Optional

from database import get_pool

router = APIRouter(prefix="/api/olap", tags=["olap"])


@router.get("/rollup-by-dept")
async def rollup_by_dept(pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT
                d.dept_id,
                d.dept_name,
                COALESCE(SUM(b.plan_rub), 0)  AS total_plan,
                COALESCE(SUM(b.fact_rub), 0)  AS total_fact,
                COALESCE(SUM(b.plan_rub), 0) - COALESCE(SUM(b.fact_rub), 0) AS deviation,
                COUNT(DISTINCT doc.doc_id)     AS doc_count
            FROM department d
            LEFT JOIN budget   b   ON b.dept_id = d.dept_id
            LEFT JOIN document doc ON doc.dept_id = d.dept_id
            GROUP BY d.dept_id, d.dept_name
            ORDER BY d.dept_name
        """)
    return [dict(r) for r in rows]


@router.get("/rollup-by-item")
async def rollup_by_item(pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT
                bi.item_id,
                bi.item_name,
                bi.item_category,
                COALESCE(SUM(b.plan_rub), 0)  AS total_plan,
                COALESCE(SUM(b.fact_rub), 0)  AS total_fact,
                COALESCE(SUM(b.plan_rub), 0) - COALESCE(SUM(b.fact_rub), 0) AS deviation,
                COUNT(DISTINCT doc.doc_id)     AS doc_count
            FROM budget_item bi
            LEFT JOIN budget   b   ON b.item_id = bi.item_id
            LEFT JOIN document doc ON doc.item_id = bi.item_id
            GROUP BY bi.item_id, bi.item_name, bi.item_category
            ORDER BY bi.item_name
        """)
    return [dict(r) for r in rows]


@router.get("/rollup-by-quarter")
async def rollup_by_quarter(pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT
                b.budget_year,
                b.budget_quarter,
                COALESCE(SUM(b.plan_rub), 0) AS total_plan,
                COALESCE(SUM(b.fact_rub), 0) AS total_fact,
                COALESCE(SUM(b.plan_rub), 0) - COALESCE(SUM(b.fact_rub), 0) AS deviation
            FROM budget b
            GROUP BY b.budget_year, b.budget_quarter
            ORDER BY b.budget_year, b.budget_quarter
        """)
    return [dict(r) for r in rows]


@router.get("/slice-by-dept")
async def slice_by_dept(dept_id: int, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        dept = await conn.fetchrow(
            "SELECT * FROM department WHERE dept_id = $1", dept_id,
        )
        budget_rows = await conn.fetch("""
            SELECT b.*, bi.item_name, bi.item_category
            FROM budget b
            JOIN budget_item bi ON bi.item_id = b.item_id
            WHERE b.dept_id = $1
            ORDER BY b.budget_year, b.budget_quarter, bi.item_name
        """, dept_id)
        doc_rows = await conn.fetch("""
            SELECT
                doc.*,
                dt.type_name,
                bi.item_name,
                c.contr_name,
                e.last_name || ' ' || e.first_name AS resp_emp_name
            FROM document doc
            LEFT JOIN doc_type    dt ON dt.type_id   = doc.type_id
            LEFT JOIN budget_item bi ON bi.item_id   = doc.item_id
            LEFT JOIN contractor  c  ON c.contr_inn   = doc.contr_inn
            LEFT JOIN employee    e  ON e.emp_id      = doc.resp_emp_id
            WHERE doc.dept_id = $1
            ORDER BY doc.doc_date DESC
        """, dept_id)
    return {
        "department": dict(dept) if dept else None,
        "budget": [dict(r) for r in budget_rows],
        "documents": [dict(r) for r in doc_rows],
    }


@router.get("/slice-by-contractor")
async def slice_by_contractor(contr_inn: str, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        contractor = await conn.fetchrow(
            "SELECT * FROM contractor WHERE contr_inn = $1", contr_inn,
        )
        doc_rows = await conn.fetch("""
            SELECT
                doc.*,
                d.dept_name,
                dt.type_name,
                bi.item_name,
                e.last_name || ' ' || e.first_name AS resp_emp_name
            FROM document doc
            LEFT JOIN department  d  ON d.dept_id    = doc.dept_id
            LEFT JOIN doc_type   dt ON dt.type_id    = doc.type_id
            LEFT JOIN budget_item bi ON bi.item_id   = doc.item_id
            LEFT JOIN employee   e  ON e.emp_id      = doc.resp_emp_id
            WHERE doc.contr_inn = $1
            ORDER BY doc.doc_date DESC
        """, contr_inn)
    return {
        "contractor": dict(contractor) if contractor else None,
        "documents": [dict(r) for r in doc_rows],
    }


@router.get("/dice")
async def dice(
    dept_id: Optional[int] = None,
    item_id: Optional[int] = None,
    budget_year: Optional[int] = None,
    budget_quarter: Optional[int] = None,
    contr_inn: Optional[str] = None,
    pool=Depends(get_pool),
):
    conditions = []
    params = []
    idx = 1

    if dept_id is not None:
        conditions.append(f"b.dept_id = ${idx}")
        params.append(dept_id)
        idx += 1
    if item_id is not None:
        conditions.append(f"b.item_id = ${idx}")
        params.append(item_id)
        idx += 1
    if budget_year is not None:
        conditions.append(f"b.budget_year = ${idx}")
        params.append(budget_year)
        idx += 1
    if budget_quarter is not None:
        conditions.append(f"b.budget_quarter = ${idx}")
        params.append(budget_quarter)
        idx += 1

    where = (" WHERE " + " AND ".join(conditions)) if conditions else ""

    async with pool.acquire() as conn:
        budget_rows = await conn.fetch(f"""
            SELECT
                b.*,
                d.dept_name,
                bi.item_name,
                bi.item_category
            FROM budget b
            JOIN department  d  ON d.dept_id  = b.dept_id
            JOIN budget_item bi ON bi.item_id = b.item_id
            {where}
            ORDER BY d.dept_name, bi.item_name, b.budget_year, b.budget_quarter
        """, *params)

        doc_conditions = []
        doc_params = []
        didx = 1
        if dept_id is not None:
            doc_conditions.append(f"doc.dept_id = ${didx}")
            doc_params.append(dept_id)
            didx += 1
        if item_id is not None:
            doc_conditions.append(f"doc.item_id = ${didx}")
            doc_params.append(item_id)
            didx += 1
        if contr_inn is not None:
            doc_conditions.append(f"doc.contr_inn = ${didx}")
            doc_params.append(contr_inn)
            didx += 1

        doc_where = (" WHERE " + " AND ".join(doc_conditions)) if doc_conditions else ""

        doc_rows = await conn.fetch(f"""
            SELECT
                doc.*,
                d.dept_name,
                bi.item_name,
                dt.type_name,
                c.contr_name,
                e.last_name || ' ' || e.first_name AS resp_emp_name
            FROM document doc
            LEFT JOIN department  d  ON d.dept_id    = doc.dept_id
            LEFT JOIN budget_item bi ON bi.item_id   = doc.item_id
            LEFT JOIN doc_type   dt ON dt.type_id    = doc.type_id
            LEFT JOIN contractor  c  ON c.contr_inn   = doc.contr_inn
            LEFT JOIN employee   e  ON e.emp_id      = doc.resp_emp_id
            {doc_where}
            ORDER BY doc.doc_date DESC
        """, *doc_params)

    return {
        "budget": [dict(r) for r in budget_rows],
        "documents": [dict(r) for r in doc_rows],
    }


@router.get("/drilldown-dept")
async def drilldown_dept(dept_id: int, pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        dept = await conn.fetchrow(
            "SELECT * FROM department WHERE dept_id = $1", dept_id,
        )
        employees = await conn.fetch("""
            SELECT e.*, p.position_name, p.position_grade
            FROM employee e
            LEFT JOIN position p ON p.position_id = e.position_id
            WHERE e.dept_id = $1
            ORDER BY e.last_name, e.first_name
        """, dept_id)
        budget_rows = await conn.fetch("""
            SELECT b.*, bi.item_name, bi.item_category
            FROM budget b
            JOIN budget_item bi ON bi.item_id = b.item_id
            WHERE b.dept_id = $1
            ORDER BY b.budget_year, b.budget_quarter, bi.item_name
        """, dept_id)
        doc_rows = await conn.fetch("""
            SELECT
                doc.*,
                dt.type_name,
                bi.item_name,
                c.contr_name,
                e.last_name || ' ' || e.first_name AS resp_emp_name
            FROM document doc
            LEFT JOIN doc_type    dt ON dt.type_id   = doc.type_id
            LEFT JOIN budget_item bi ON bi.item_id   = doc.item_id
            LEFT JOIN contractor  c  ON c.contr_inn   = doc.contr_inn
            LEFT JOIN employee    e  ON e.emp_id      = doc.resp_emp_id
            WHERE doc.dept_id = $1
            ORDER BY doc.doc_date DESC
        """, dept_id)

    summary = {
        "total_plan": sum(float(r["plan_rub"] or 0) for r in budget_rows),
        "total_fact": sum(float(r["fact_rub"] or 0) for r in budget_rows),
        "employee_count": len(employees),
        "doc_count": len(doc_rows),
    }
    summary["deviation"] = summary["total_plan"] - summary["total_fact"]

    return {
        "department": dict(dept) if dept else None,
        "summary": summary,
        "employees": [dict(r) for r in employees],
        "budget": [dict(r) for r in budget_rows],
        "documents": [dict(r) for r in doc_rows],
    }


@router.get("/cross-dept-item")
async def cross_dept_item(pool=Depends(get_pool)):
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT
                d.dept_id,
                d.dept_name,
                bi.item_id,
                bi.item_name,
                COALESCE(SUM(b.plan_rub), 0) AS total_plan,
                COALESCE(SUM(b.fact_rub), 0) AS total_fact,
                COALESCE(SUM(b.plan_rub), 0) - COALESCE(SUM(b.fact_rub), 0) AS deviation
            FROM budget b
            JOIN department  d  ON d.dept_id  = b.dept_id
            JOIN budget_item bi ON bi.item_id = b.item_id
            GROUP BY d.dept_id, d.dept_name, bi.item_id, bi.item_name
            ORDER BY d.dept_name, bi.item_name
        """)

    pivot: dict[str, dict] = {}
    for r in rows:
        dept = r["dept_name"]
        if dept not in pivot:
            pivot[dept] = {"dept_id": r["dept_id"], "dept_name": dept, "items": {}}
        pivot[dept]["items"][r["item_name"]] = {
            "item_id": r["item_id"],
            "total_plan": r["total_plan"],
            "total_fact": r["total_fact"],
            "deviation": r["deviation"],
        }

    return list(pivot.values())

```

## backend/routers/position.py

```py
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

```

## backend/seed_data.sql

```sql
-- ============================================================
-- SEED: репрезентативные тестовые данные
-- ============================================================

BEGIN;

-- ── Очистка (порядок важен из-за FK) ────────────────────────
TRUNCATE document, budget, employee, department, budget_item,
         contractor, doc_type, position RESTART IDENTITY CASCADE;

-- ============================================================
-- 1. ДОЛЖНОСТИ
-- ============================================================
INSERT INTO position (position_id, position_name, position_grade, min_salary) VALUES
  (1,  'Главный бухгалтер',           'С5', 95000),
  (2,  'Бухгалтер',                   'С3', 55000),
  (3,  'Экономист',                   'С4', 70000),
  (4,  'Генеральный директор',        'С7', 200000),
  (5,  'Заместитель директора',       'С6', 140000),
  (6,  'Руководитель отдела',         'С5', 100000),
  (7,  'Системный администратор',     'С3', 68000),
  (8,  'Разработчик ПО',              'С4', 90000),
  (9,  'Юрисконсульт',                'С4', 78000),
  (10, 'Старший юрисконсульт',        'С5', 98000),
  (11, 'Менеджер по маркетингу',      'С3', 62000),
  (12, 'Специалист по рекламе',       'С3', 58000),
  (13, 'Специалист по кадрам',        'С2', 52000),
  (14, 'Офис-менеджер',               'С2', 48000),
  (15, 'Аналитик',                    'С4', 75000);

-- ============================================================
-- 2. ТИПЫ ДОКУМЕНТОВ
-- ============================================================
INSERT INTO doc_type (type_id, type_name, retention_years, requires_approval) VALUES
  (1, 'Счёт-фактура',             5, true),
  (2, 'Акт выполненных работ',    5, true),
  (3, 'Внутренняя записка',       3, false),
  (4, 'Договор',                  7, true),
  (5, 'Приказ',                   5, true),
  (6, 'Служебная записка',        3, false),
  (7, 'Авансовый отчёт',          5, true),
  (8, 'Накладная',                5, false);

-- ============================================================
-- 3. СТАТЬИ БЮДЖЕТА
-- ============================================================
INSERT INTO budget_item (item_id, item_name, item_category) VALUES
  (1,  'Заработная плата',         'Расходы на персонал'),
  (2,  'Канцелярские товары',      'Хозяйственные расходы'),
  (3,  'Командировочные расходы',  'Расходы на персонал'),
  (4,  'Аренда помещений',         'Административные расходы'),
  (5,  'Коммунальные услуги',      'Административные расходы'),
  (6,  'ИТ-оборудование',          'ИТ-расходы'),
  (7,  'Программное обеспечение',  'ИТ-расходы'),
  (8,  'Маркетинг и реклама',      'Коммерческие расходы'),
  (9,  'Обучение персонала',       'Расходы на персонал'),
  (10, 'Транспортные расходы',     'Хозяйственные расходы'),
  (11, 'Связь и интернет',         'ИТ-расходы'),
  (12, 'Ремонт и обслуживание',    'Административные расходы');

-- ============================================================
-- 4. КОНТРАГЕНТЫ
-- ============================================================
INSERT INTO contractor (contr_inn, contr_name, contr_address, contr_phone) VALUES
  ('7701234567', 'ООО «Альфа-Снаб»',          'г. Москва, ул. Ленина, д. 10',          '+7(495)111-22-33'),
  ('7709876543', 'АО «БетаСервис»',            'г. Москва, Пресненская наб., д. 6',     '+7(495)444-55-66'),
  ('7723456789', 'ООО «ИТ-Технологии»',        'г. Москва, ш. Варшавское, д. 125',      '+7(495)300-10-10'),
  ('7731234567', 'ООО «ЮрКонсалт»',            'г. Москва, ул. Садовая, д. 3',          '+7(495)500-20-20'),
  ('7745678901', 'ИП Федоров И.М.',             'г. Москва, ул. Профсоюзная, д. 47',    '+7(926)600-30-30'),
  ('7756789012', 'ООО «КлинПро»',              'г. Москва, ул. Новороссийская, д. 8',   '+7(499)700-40-40'),
  ('7799012345', 'ПАО «РосТелеком»',           'г. Москва, ул. Тверская, д. 7',         '+7(800)100-08-00'),
  ('7812345678', 'ООО «АдвансЛёрнинг»',        'г. Санкт-Петербург, Невский пр., д. 30','+7(812)200-50-50'),
  ('7867890123', 'ООО «РекламаПро»',           'г. Москва, ул. Арбат, д. 20',           '+7(495)800-60-60'),
  ('5012345678', 'ЗАО «КанцторМаркет»',        'г. Москва, ул. Маросейка, д. 12',       '+7(495)900-70-70');

-- ============================================================
-- 5. ОТДЕЛЫ (временно без head_emp_id)
-- ============================================================
INSERT INTO department (dept_id, dept_name, emp_count, floor_num, room_num, dept_phone, dept_email, created_date) VALUES
  (1, 'Бухгалтерия',                        5, 2, '205',  '+7(495)100-00-01', 'buh@company.ru',   '2010-03-15'),
  (2, 'Планово-экономический отдел',         4, 3, '312а', '+7(495)100-00-02', 'plan@company.ru',  '2012-06-01'),
  (3, 'Отдел информационных технологий',     6, 4, '401',  '+7(495)100-00-03', 'it@company.ru',    '2015-01-10'),
  (4, 'Юридический отдел',                   3, 3, '305',  '+7(495)100-00-04', 'legal@company.ru', '2011-09-01'),
  (5, 'Отдел маркетинга и рекламы',          4, 2, '210',  '+7(495)100-00-05', 'mkt@company.ru',   '2016-04-01'),
  (6, 'Отдел кадров',                        3, 2, '202',  '+7(495)100-00-06', 'hr@company.ru',    '2010-03-15'),
  (7, 'Административно-хозяйственный отдел', 4, 1, '101',  '+7(495)100-00-07', 'aho@company.ru',   '2010-03-15'),
  (8, 'Дирекция',                            3, 5, '501',  '+7(495)100-00-08', 'dir@company.ru',   '2010-01-01');

-- ============================================================
-- 6. СОТРУДНИКИ
-- ============================================================
INSERT INTO employee (emp_id, dept_id, last_name, first_name, middle_name, position_id, salary, hire_date, birth_date, education, inn, snils, emp_phone, emp_email) VALUES
-- Бухгалтерия (dept 1)
  (101, 1, 'Иванова',    'Мария',     'Петровна',      1, 125000, '2010-03-15', '1980-07-22', 'Высшее', '770101010101', '001-001-001 01', '+7(495)200-01-01', 'ivanova@company.ru'),
  (102, 1, 'Сидоров',    'Алексей',   'Игоревич',      2,  67000, '2018-09-01', '1992-11-03', 'Высшее', '770202020202', '002-002-002 02', '+7(495)200-01-02', 'sidorov@company.ru'),
  (103, 1, 'Кузнецова',  'Елена',     'Сергеевна',     2,  62000, '2020-01-15', '1995-04-18', 'Высшее', '770303030303', '003-003-003 03', '+7(495)200-01-03', 'kuznetsova@company.ru'),
  (104, 1, 'Миронова',   'Светлана',  'Борисовна',     2,  64000, '2021-06-01', '1994-02-14', 'Высшее', '770404040411', '004-004-004 11', '+7(495)200-01-04', 'mironova@company.ru'),
  (105, 1, 'Орлов',      'Павел',     'Николаевич',    3,  78000, '2017-03-20', '1988-09-05', 'Высшее', '770505050511', '005-005-005 11', '+7(495)200-01-05', 'orlov@company.ru'),
-- Планово-экономический (dept 2)
  (201, 2, 'Петров',     'Дмитрий',   'Александрович', 6,  98000, '2012-06-01', '1985-01-30', 'Высшее', '770404040404', '004-004-004 04', '+7(495)200-02-01', 'petrov@company.ru'),
  (202, 2, 'Смирнова',   'Ольга',     'Викторовна',    3,  78000, '2019-03-10', '1990-09-12', 'Высшее', '770505050505', '005-005-005 05', '+7(495)200-02-02', 'smirnova@company.ru'),
  (203, 2, 'Зайцев',     'Артём',     'Владимирович',  15, 77000, '2020-08-15', '1993-05-25', 'Высшее', '770606060606', '006-006-006 06', '+7(495)200-02-03', 'zaitsev@company.ru'),
  (204, 2, 'Фёдорова',   'Наталья',   'Алексеевна',    3,  72000, '2022-01-10', '1996-11-08', 'Высшее', '770707070707', '007-007-007 07', '+7(495)200-02-04', 'fedorova@company.ru'),
-- ИТ-отдел (dept 3)
  (301, 3, 'Новиков',    'Игорь',     'Константинович',6, 105000, '2015-01-10', '1982-06-15', 'Высшее', '770808080808', '008-008-008 08', '+7(495)200-03-01', 'novikov@company.ru'),
  (302, 3, 'Козлов',     'Денис',     'Максимович',    8,  98000, '2016-04-01', '1990-03-22', 'Высшее', '770909090909', '009-009-009 09', '+7(495)200-03-02', 'kozlov@company.ru'),
  (303, 3, 'Лебедева',   'Анна',      'Юрьевна',       8,  95000, '2017-07-01', '1991-12-10', 'Высшее', '771010101010', '010-010-010 10', '+7(495)200-03-03', 'lebedeva@company.ru'),
  (304, 3, 'Морозов',    'Кирилл',    'Андреевич',     7,  72000, '2019-09-15', '1995-08-27', 'Высшее', '771111111111', '011-011-011 11', '+7(495)200-03-04', 'morozov@company.ru'),
  (305, 3, 'Волкова',    'Татьяна',   'Игоревна',      8,  92000, '2020-03-01', '1993-04-03', 'Высшее', '771212121212', '012-012-012 12', '+7(495)200-03-05', 'volkova@company.ru'),
  (306, 3, 'Соловьёв',   'Максим',    'Олегович',      7,  69000, '2023-02-01', '1998-01-15', 'Высшее', '771313131313', '013-013-013 13', '+7(495)200-03-06', 'solovyev@company.ru'),
-- Юридический (dept 4)
  (401, 4, 'Захарова',   'Виктория',  'Павловна',      10, 102000, '2011-09-01', '1983-10-20', 'Высшее', '771414141414', '014-014-014 14', '+7(495)200-04-01', 'zakharova@company.ru'),
  (402, 4, 'Яковлев',    'Роман',     'Сергеевич',     9,  82000, '2018-05-15', '1991-07-14', 'Высшее', '771515151515', '015-015-015 15', '+7(495)200-04-02', 'yakovlev@company.ru'),
  (403, 4, 'Воронова',   'Ксения',    'Дмитриевна',    9,  80000, '2021-11-01', '1994-03-07', 'Высшее', '771616161616', '016-016-016 16', '+7(495)200-04-03', 'voronova@company.ru'),
-- Маркетинг (dept 5)
  (501, 5, 'Белова',     'Марина',    'Геннадьевна',   6, 105000, '2016-04-01', '1984-09-18', 'Высшее', '771717171717', '017-017-017 17', '+7(495)200-05-01', 'belova@company.ru'),
  (502, 5, 'Тихонов',    'Евгений',   'Романович',     11, 65000, '2019-08-01', '1994-06-22', 'Высшее', '771818181818', '018-018-018 18', '+7(495)200-05-02', 'tikhonov@company.ru'),
  (503, 5, 'Степанова',  'Дарья',     'Николаевна',    12, 61000, '2021-02-15', '1996-12-05', 'Высшее', '771919191919', '019-019-019 19', '+7(495)200-05-03', 'stepanova@company.ru'),
  (504, 5, 'Григорьев',  'Антон',     'Михайлович',    11, 64000, '2022-07-01', '1997-03-30', 'Высшее', '772020202020', '020-020-020 20', '+7(495)200-05-04', 'grigoriev@company.ru'),
-- Кадры (dept 6)
  (601, 6, 'Кириллова',  'Людмила',   'Ивановна',      6,  95000, '2010-03-15', '1979-05-12', 'Высшее', '772121212121', '021-021-021 21', '+7(495)200-06-01', 'kirillova@company.ru'),
  (602, 6, 'Комарова',   'Полина',    'Витальевна',    13, 55000, '2020-10-01', '1996-08-19', 'Высшее', '772222222222', '022-022-022 22', '+7(495)200-06-02', 'komarova@company.ru'),
  (603, 6, 'Тарасов',    'Сергей',    'Юрьевич',       13, 54000, '2021-04-01', '1995-11-23', 'Высшее', '772323232323', '023-023-023 23', '+7(495)200-06-03', 'tarasov@company.ru'),
-- АХО (dept 7)
  (701, 7, 'Крылова',    'Надежда',   'Семёновна',     6,  92000, '2010-03-15', '1978-02-28', 'Среднее специальное', '772424242424', '024-024-024 24', '+7(495)200-07-01', 'krylova@company.ru'),
  (702, 7, 'Попов',      'Виталий',   'Анатольевич',   14, 51000, '2015-06-01', '1988-07-07', 'Среднее специальное', '772525252525', '025-025-025 25', '+7(495)200-07-02', 'popov@company.ru'),
  (703, 7, 'Гусева',     'Ирина',     'Вячеславовна',  14, 50000, '2018-01-10', '1992-04-16', 'Среднее специальное', '772626262626', '026-026-026 26', '+7(495)200-07-03', 'guseva@company.ru'),
  (704, 7, 'Рябов',      'Николай',   'Петрович',      14, 49000, '2022-09-01', '1997-10-10', 'Среднее', '772727272727', '027-027-027 27', '+7(495)200-07-04', 'ryabov@company.ru'),
-- Дирекция (dept 8)
  (801, 8, 'Шаров',      'Александр', 'Владимирович',  4, 220000, '2010-01-01', '1972-03-25', 'Высшее', '772828282828', '028-028-028 28', '+7(495)200-08-01', 'sharov@company.ru'),
  (802, 8, 'Громова',    'Ирина',     'Александровна', 5, 155000, '2010-01-15', '1975-11-30', 'Высшее', '772929292929', '029-029-029 29', '+7(495)200-08-02', 'gromova@company.ru'),
  (803, 8, 'Лукьянов',   'Виктор',    'Игоревич',      5, 148000, '2013-04-01', '1978-06-17', 'Высшее', '773030303030', '030-030-030 30', '+7(495)200-08-03', 'lukyanov@company.ru');

-- ============================================================
-- 7. ОБНОВЛЯЕМ РУКОВОДИТЕЛЕЙ ОТДЕЛОВ
-- ============================================================
UPDATE department SET head_emp_id = 101, head_appoint_date = '2010-03-15' WHERE dept_id = 1;
UPDATE department SET head_emp_id = 201, head_appoint_date = '2012-06-01' WHERE dept_id = 2;
UPDATE department SET head_emp_id = 301, head_appoint_date = '2015-01-10' WHERE dept_id = 3;
UPDATE department SET head_emp_id = 401, head_appoint_date = '2011-09-01' WHERE dept_id = 4;
UPDATE department SET head_emp_id = 501, head_appoint_date = '2016-04-01' WHERE dept_id = 5;
UPDATE department SET head_emp_id = 601, head_appoint_date = '2010-03-15' WHERE dept_id = 6;
UPDATE department SET head_emp_id = 701, head_appoint_date = '2010-03-15' WHERE dept_id = 7;
UPDATE department SET head_emp_id = 801, head_appoint_date = '2010-01-01' WHERE dept_id = 8;

-- ============================================================
-- 8. БЮДЖЕТ (2023-2024 все 4 квартала, 2025 Q1-Q2)
-- Отдел 1: Бухгалтерия — зарплата, канцелярия, обучение
-- Отдел 2: ПЭО — зарплата, командировки, канцелярия
-- Отдел 3: ИТ — зарплата, оборудование, ПО, связь
-- Отдел 4: Юридический — зарплата, командировки
-- Отдел 5: Маркетинг — зарплата, маркетинг/реклама
-- Отдел 6: Кадры — зарплата, обучение, канцелярия
-- Отдел 7: АХО — зарплата, транспорт, ремонт, коммуналка
-- Отдел 8: Дирекция — зарплата, аренда, командировки, транспорт
-- ============================================================

INSERT INTO budget (dept_id, item_id, budget_year, budget_quarter, plan_rub, fact_rub, approved_date) VALUES

-- ══════════ 2023 ══════════
-- Бухгалтерия (dept 1) — зарплата (item 1)
  (1, 1, 2023, 1,  990000,  972000, '2022-12-20'),
  (1, 1, 2023, 2,  990000,  985000, '2022-12-20'),
  (1, 1, 2023, 3,  990000,  990000, '2022-12-20'),
  (1, 1, 2023, 4, 1200000, 1198000, '2022-12-20'),
-- Бухгалтерия — канцелярия (item 2)
  (1, 2, 2023, 1,  25000,  22400, '2022-12-20'),
  (1, 2, 2023, 2,  20000,  19100, '2022-12-20'),
  (1, 2, 2023, 3,  20000,  21300, '2022-12-20'),
  (1, 2, 2023, 4,  30000,  28600, '2022-12-20'),
-- Бухгалтерия — обучение (item 9)
  (1, 9, 2023, 1,  30000,     0, '2022-12-20'),
  (1, 9, 2023, 2,  60000, 58500, '2022-12-20'),
  (1, 9, 2023, 3,  30000, 31200, '2022-12-20'),
  (1, 9, 2023, 4,  50000, 47000, '2022-12-20'),

-- ПЭО (dept 2) — зарплата
  (2, 1, 2023, 1,  780000,  762000, '2022-12-22'),
  (2, 1, 2023, 2,  780000,  780000, '2022-12-22'),
  (2, 1, 2023, 3,  780000,  775000, '2022-12-22'),
  (2, 1, 2023, 4,  950000,  948000, '2022-12-22'),
-- ПЭО — командировки (item 3)
  (2, 3, 2023, 1, 120000, 115000, '2022-12-22'),
  (2, 3, 2023, 2, 150000, 162000, '2022-12-22'),
  (2, 3, 2023, 3, 130000, 128000, '2022-12-22'),
  (2, 3, 2023, 4, 100000,  95000, '2022-12-22'),
-- ПЭО — канцелярия
  (2, 2, 2023, 1, 18000,  16200, '2022-12-22'),
  (2, 2, 2023, 2, 15000,  14900, '2022-12-22'),
  (2, 2, 2023, 3, 15000,  15800, '2022-12-22'),
  (2, 2, 2023, 4, 22000,  21000, '2022-12-22'),

-- ИТ (dept 3) — зарплата
  (3, 1, 2023, 1, 1320000, 1298000, '2022-12-25'),
  (3, 1, 2023, 2, 1320000, 1320000, '2022-12-25'),
  (3, 1, 2023, 3, 1320000, 1335000, '2022-12-25'),
  (3, 1, 2023, 4, 1600000, 1598000, '2022-12-25'),
-- ИТ — оборудование (item 6)
  (3, 6, 2023, 1, 500000,  487000, '2022-12-25'),
  (3, 6, 2023, 2, 300000,  312000, '2022-12-25'),
  (3, 6, 2023, 3, 400000,  445000, '2022-12-25'),
  (3, 6, 2023, 4, 700000,  712000, '2022-12-25'),
-- ИТ — ПО (item 7)
  (3, 7, 2023, 1, 280000, 275000, '2022-12-25'),
  (3, 7, 2023, 2, 180000, 190000, '2022-12-25'),
  (3, 7, 2023, 3, 200000, 198000, '2022-12-25'),
  (3, 7, 2023, 4, 350000, 362000, '2022-12-25'),
-- ИТ — связь (item 11)
  (3, 11, 2023, 1,  90000,  88000, '2022-12-25'),
  (3, 11, 2023, 2,  90000,  92000, '2022-12-25'),
  (3, 11, 2023, 3,  90000,  90000, '2022-12-25'),
  (3, 11, 2023, 4,  90000,  91000, '2022-12-25'),

-- Юридический (dept 4) — зарплата
  (4, 1, 2023, 1, 636000, 625000, '2022-12-23'),
  (4, 1, 2023, 2, 636000, 636000, '2022-12-23'),
  (4, 1, 2023, 3, 636000, 640000, '2022-12-23'),
  (4, 1, 2023, 4, 780000, 778000, '2022-12-23'),
-- Юридический — командировки
  (4, 3, 2023, 1,  80000,  72000, '2022-12-23'),
  (4, 3, 2023, 2,  90000,  95000, '2022-12-23'),
  (4, 3, 2023, 3,  70000,  68000, '2022-12-23'),
  (4, 3, 2023, 4,  60000,  58000, '2022-12-23'),

-- Маркетинг (dept 5) — зарплата
  (5, 1, 2023, 1,  735000,  720000, '2022-12-26'),
  (5, 1, 2023, 2,  735000,  735000, '2022-12-26'),
  (5, 1, 2023, 3,  735000,  740000, '2022-12-26'),
  (5, 1, 2023, 4,  900000,  895000, '2022-12-26'),
-- Маркетинг — маркетинг/реклама (item 8)
  (5, 8, 2023, 1,  250000,  238000, '2022-12-26'),
  (5, 8, 2023, 2,  350000,  362000, '2022-12-26'),
  (5, 8, 2023, 3,  450000,  478000, '2022-12-26'),
  (5, 8, 2023, 4,  500000,  512000, '2022-12-26'),

-- Кадры (dept 6) — зарплата
  (6, 1, 2023, 1, 492000, 482000, '2022-12-23'),
  (6, 1, 2023, 2, 492000, 492000, '2022-12-23'),
  (6, 1, 2023, 3, 492000, 488000, '2022-12-23'),
  (6, 1, 2023, 4, 600000, 598000, '2022-12-23'),
-- Кадры — обучение (item 9)
  (6, 9, 2023, 1, 120000, 115000, '2022-12-23'),
  (6, 9, 2023, 2, 150000, 148000, '2022-12-23'),
  (6, 9, 2023, 3, 100000, 102000, '2022-12-23'),
  (6, 9, 2023, 4, 200000, 195000, '2022-12-23'),
-- Кадры — канцелярия
  (6, 2, 2023, 1, 10000,  9200, '2022-12-23'),
  (6, 2, 2023, 2, 10000,  9800, '2022-12-23'),
  (6, 2, 2023, 3, 10000, 10500, '2022-12-23'),
  (6, 2, 2023, 4, 15000, 14200, '2022-12-23'),

-- АХО (dept 7) — зарплата
  (7, 1, 2023, 1, 588000, 574000, '2022-12-24'),
  (7, 1, 2023, 2, 588000, 588000, '2022-12-24'),
  (7, 1, 2023, 3, 588000, 582000, '2022-12-24'),
  (7, 1, 2023, 4, 720000, 718000, '2022-12-24'),
-- АХО — транспорт (item 10)
  (7, 10, 2023, 1, 150000, 142000, '2022-12-24'),
  (7, 10, 2023, 2, 120000, 125000, '2022-12-24'),
  (7, 10, 2023, 3, 130000, 138000, '2022-12-24'),
  (7, 10, 2023, 4, 160000, 155000, '2022-12-24'),
-- АХО — ремонт (item 12)
  (7, 12, 2023, 1, 200000, 185000, '2022-12-24'),
  (7, 12, 2023, 2, 150000, 148000, '2022-12-24'),
  (7, 12, 2023, 3, 300000, 318000, '2022-12-24'),
  (7, 12, 2023, 4, 250000, 245000, '2022-12-24'),
-- АХО — коммунальные (item 5)
  (7, 5, 2023, 1, 280000, 272000, '2022-12-24'),
  (7, 5, 2023, 2, 210000, 205000, '2022-12-24'),
  (7, 5, 2023, 3, 220000, 228000, '2022-12-24'),
  (7, 5, 2023, 4, 290000, 285000, '2022-12-24'),

-- Дирекция (dept 8) — зарплата
  (8, 1, 2023, 1, 1548000, 1520000, '2022-12-18'),
  (8, 1, 2023, 2, 1548000, 1548000, '2022-12-18'),
  (8, 1, 2023, 3, 1548000, 1560000, '2022-12-18'),
  (8, 1, 2023, 4, 1900000, 1898000, '2022-12-18'),
-- Дирекция — аренда (item 4)
  (8, 4, 2023, 1, 1800000, 1800000, '2022-12-18'),
  (8, 4, 2023, 2, 1800000, 1800000, '2022-12-18'),
  (8, 4, 2023, 3, 1800000, 1800000, '2022-12-18'),
  (8, 4, 2023, 4, 1800000, 1800000, '2022-12-18'),
-- Дирекция — командировки
  (8, 3, 2023, 1, 200000, 188000, '2022-12-18'),
  (8, 3, 2023, 2, 250000, 265000, '2022-12-18'),
  (8, 3, 2023, 3, 200000, 195000, '2022-12-18'),
  (8, 3, 2023, 4, 300000, 312000, '2022-12-18'),
-- Дирекция — транспорт
  (8, 10, 2023, 1, 180000, 172000, '2022-12-18'),
  (8, 10, 2023, 2, 150000, 158000, '2022-12-18'),
  (8, 10, 2023, 3, 160000, 162000, '2022-12-18'),
  (8, 10, 2023, 4, 200000, 195000, '2022-12-18'),

-- ══════════ 2024 ══════════
-- Бухгалтерия
  (1, 1, 2024, 1, 1050000, 1032000, '2023-12-20'),
  (1, 1, 2024, 2, 1050000, 1048000, '2023-12-20'),
  (1, 1, 2024, 3, 1050000, 1055000, '2023-12-20'),
  (1, 1, 2024, 4, 1280000, 1275000, '2023-12-20'),
  (1, 2, 2024, 1,  28000,  26200, '2023-12-20'),
  (1, 2, 2024, 2,  22000,  21500, '2023-12-20'),
  (1, 2, 2024, 3,  22000,  23100, '2023-12-20'),
  (1, 2, 2024, 4,  35000,  33800, '2023-12-20'),
  (1, 9, 2024, 1,  40000,      0, '2023-12-20'),
  (1, 9, 2024, 2,  80000,  78500, '2023-12-20'),
  (1, 9, 2024, 3,  40000,  42000, '2023-12-20'),
  (1, 9, 2024, 4,  60000,  57000, '2023-12-20'),
-- ПЭО
  (2, 1, 2024, 1,  840000,  822000, '2023-12-22'),
  (2, 1, 2024, 2,  840000,  840000, '2023-12-22'),
  (2, 1, 2024, 3,  840000,  838000, '2023-12-22'),
  (2, 1, 2024, 4, 1020000, 1018000, '2023-12-22'),
  (2, 3, 2024, 1, 130000, 122000, '2023-12-22'),
  (2, 3, 2024, 2, 160000, 175000, '2023-12-22'),
  (2, 3, 2024, 3, 140000, 138000, '2023-12-22'),
  (2, 3, 2024, 4, 110000, 102000, '2023-12-22'),
  (2, 2, 2024, 1,  20000,  18500, '2023-12-22'),
  (2, 2, 2024, 2,  17000,  16800, '2023-12-22'),
  (2, 2, 2024, 3,  17000,  17500, '2023-12-22'),
  (2, 2, 2024, 4,  25000,  24000, '2023-12-22'),
-- ИТ
  (3, 1, 2024, 1, 1450000, 1428000, '2023-12-25'),
  (3, 1, 2024, 2, 1450000, 1450000, '2023-12-25'),
  (3, 1, 2024, 3, 1450000, 1465000, '2023-12-25'),
  (3, 1, 2024, 4, 1760000, 1758000, '2023-12-25'),
  (3, 6, 2024, 1,  600000,  578000, '2023-12-25'),
  (3, 6, 2024, 2,  350000,  368000, '2023-12-25'),
  (3, 6, 2024, 3,  450000,  510000, '2023-12-25'),
  (3, 6, 2024, 4,  800000,  825000, '2023-12-25'),
  (3, 7, 2024, 1,  320000,  315000, '2023-12-25'),
  (3, 7, 2024, 2,  220000,  235000, '2023-12-25'),
  (3, 7, 2024, 3,  250000,  248000, '2023-12-25'),
  (3, 7, 2024, 4,  420000,  438000, '2023-12-25'),
  (3, 11, 2024, 1, 100000,  98000, '2023-12-25'),
  (3, 11, 2024, 2, 100000, 104000, '2023-12-25'),
  (3, 11, 2024, 3, 100000, 100000, '2023-12-25'),
  (3, 11, 2024, 4, 100000, 102000, '2023-12-25'),
-- Юридический
  (4, 1, 2024, 1,  700000,  688000, '2023-12-23'),
  (4, 1, 2024, 2,  700000,  700000, '2023-12-23'),
  (4, 1, 2024, 3,  700000,  708000, '2023-12-23'),
  (4, 1, 2024, 4,  860000,  855000, '2023-12-23'),
  (4, 3, 2024, 1,   90000,  82000, '2023-12-23'),
  (4, 3, 2024, 2,  100000, 108000, '2023-12-23'),
  (4, 3, 2024, 3,   80000,  78000, '2023-12-23'),
  (4, 3, 2024, 4,   70000,  65000, '2023-12-23'),
-- Маркетинг
  (5, 1, 2024, 1,  800000,  785000, '2023-12-26'),
  (5, 1, 2024, 2,  800000,  800000, '2023-12-26'),
  (5, 1, 2024, 3,  800000,  808000, '2023-12-26'),
  (5, 1, 2024, 4,  980000,  972000, '2023-12-26'),
  (5, 8, 2024, 1,  300000,  285000, '2023-12-26'),
  (5, 8, 2024, 2,  420000,  445000, '2023-12-26'),
  (5, 8, 2024, 3,  550000,  582000, '2023-12-26'),
  (5, 8, 2024, 4,  600000,  628000, '2023-12-26'),
-- Кадры
  (6, 1, 2024, 1,  528000,  518000, '2023-12-23'),
  (6, 1, 2024, 2,  528000,  528000, '2023-12-23'),
  (6, 1, 2024, 3,  528000,  522000, '2023-12-23'),
  (6, 1, 2024, 4,  645000,  642000, '2023-12-23'),
  (6, 9, 2024, 1,  140000, 132000, '2023-12-23'),
  (6, 9, 2024, 2,  180000, 178000, '2023-12-23'),
  (6, 9, 2024, 3,  120000, 125000, '2023-12-23'),
  (6, 9, 2024, 4,  240000, 232000, '2023-12-23'),
  (6, 2, 2024, 1,  12000,  11200, '2023-12-23'),
  (6, 2, 2024, 2,  12000,  11800, '2023-12-23'),
  (6, 2, 2024, 3,  12000,  12500, '2023-12-23'),
  (6, 2, 2024, 4,  18000,  17200, '2023-12-23'),
-- АХО
  (7, 1, 2024, 1,  630000,  615000, '2023-12-24'),
  (7, 1, 2024, 2,  630000,  630000, '2023-12-24'),
  (7, 1, 2024, 3,  630000,  625000, '2023-12-24'),
  (7, 1, 2024, 4,  770000,  768000, '2023-12-24'),
  (7, 10, 2024, 1, 165000, 158000, '2023-12-24'),
  (7, 10, 2024, 2, 135000, 142000, '2023-12-24'),
  (7, 10, 2024, 3, 145000, 152000, '2023-12-24'),
  (7, 10, 2024, 4, 175000, 168000, '2023-12-24'),
  (7, 12, 2024, 1, 220000, 205000, '2023-12-24'),
  (7, 12, 2024, 2, 170000, 168000, '2023-12-24'),
  (7, 12, 2024, 3, 350000, 372000, '2023-12-24'),
  (7, 12, 2024, 4, 280000, 272000, '2023-12-24'),
  (7, 5, 2024, 1,  300000, 292000, '2023-12-24'),
  (7, 5, 2024, 2,  225000, 220000, '2023-12-24'),
  (7, 5, 2024, 3,  235000, 244000, '2023-12-24'),
  (7, 5, 2024, 4,  310000, 305000, '2023-12-24'),
-- Дирекция
  (8, 1, 2024, 1, 1644000, 1615000, '2023-12-18'),
  (8, 1, 2024, 2, 1644000, 1644000, '2023-12-18'),
  (8, 1, 2024, 3, 1644000, 1660000, '2023-12-18'),
  (8, 1, 2024, 4, 2015000, 2012000, '2023-12-18'),
  (8, 4, 2024, 1, 1980000, 1980000, '2023-12-18'),
  (8, 4, 2024, 2, 1980000, 1980000, '2023-12-18'),
  (8, 4, 2024, 3, 1980000, 1980000, '2023-12-18'),
  (8, 4, 2024, 4, 1980000, 1980000, '2023-12-18'),
  (8, 3, 2024, 1,  220000, 208000, '2023-12-18'),
  (8, 3, 2024, 2,  280000, 295000, '2023-12-18'),
  (8, 3, 2024, 3,  220000, 215000, '2023-12-18'),
  (8, 3, 2024, 4,  330000, 345000, '2023-12-18'),
  (8, 10, 2024, 1, 200000, 192000, '2023-12-18'),
  (8, 10, 2024, 2, 165000, 172000, '2023-12-18'),
  (8, 10, 2024, 3, 175000, 178000, '2023-12-18'),
  (8, 10, 2024, 4, 220000, 215000, '2023-12-18'),

-- ══════════ 2025 (Q1-Q2) ══════════
-- Бухгалтерия
  (1, 1, 2025, 1, 1100000, 1088000, '2024-12-20'),
  (1, 1, 2025, 2, 1100000,  950000, '2024-12-20'),
  (1, 2, 2025, 1,   30000,   27500, '2024-12-20'),
  (1, 2, 2025, 2,   25000,   12000, '2024-12-20'),
  (1, 9, 2025, 1,   50000,       0, '2024-12-20'),
  (1, 9, 2025, 2,   90000,   45000, '2024-12-20'),
-- ПЭО
  (2, 1, 2025, 1,  900000,  885000, '2024-12-22'),
  (2, 1, 2025, 2,  900000,  780000, '2024-12-22'),
  (2, 3, 2025, 1,  140000,  132000, '2024-12-22'),
  (2, 3, 2025, 2,  170000,   85000, '2024-12-22'),
  (2, 2, 2025, 1,   22000,   19800, '2024-12-22'),
  (2, 2, 2025, 2,   18000,    9500, '2024-12-22'),
-- ИТ
  (3, 1, 2025, 1, 1560000, 1538000, '2024-12-25'),
  (3, 1, 2025, 2, 1560000, 1350000, '2024-12-25'),
  (3, 6, 2025, 1,  650000,  628000, '2024-12-25'),
  (3, 6, 2025, 2,  400000,  220000, '2024-12-25'),
  (3, 7, 2025, 1,  350000,  342000, '2024-12-25'),
  (3, 7, 2025, 2,  250000,  138000, '2024-12-25'),
  (3, 11, 2025, 1, 110000,  108000, '2024-12-25'),
  (3, 11, 2025, 2, 110000,   55000, '2024-12-25'),
-- Юридический
  (4, 1, 2025, 1,  750000,  738000, '2024-12-23'),
  (4, 1, 2025, 2,  750000,  650000, '2024-12-23'),
  (4, 3, 2025, 1,   95000,   88000, '2024-12-23'),
  (4, 3, 2025, 2,  105000,   52000, '2024-12-23'),
-- Маркетинг
  (5, 1, 2025, 1,  860000,  845000, '2024-12-26'),
  (5, 1, 2025, 2,  860000,  740000, '2024-12-26'),
  (5, 8, 2025, 1,  350000,  332000, '2024-12-26'),
  (5, 8, 2025, 2,  480000,  265000, '2024-12-26'),
-- Кадры
  (6, 1, 2025, 1,  570000,  558000, '2024-12-23'),
  (6, 1, 2025, 2,  570000,  495000, '2024-12-23'),
  (6, 9, 2025, 1,  155000,  148000, '2024-12-23'),
  (6, 9, 2025, 2,  200000,   98000, '2024-12-23'),
  (6, 2, 2025, 1,   14000,   12800, '2024-12-23'),
  (6, 2, 2025, 2,   14000,    7200, '2024-12-23'),
-- АХО
  (7, 1, 2025, 1,  675000,  662000, '2024-12-24'),
  (7, 1, 2025, 2,  675000,  582000, '2024-12-24'),
  (7, 10, 2025, 1, 175000,  168000, '2024-12-24'),
  (7, 10, 2025, 2, 145000,   78000, '2024-12-24'),
  (7, 12, 2025, 1, 240000,  222000, '2024-12-24'),
  (7, 12, 2025, 2, 185000,   95000, '2024-12-24'),
  (7, 5, 2025, 1,  315000,  308000, '2024-12-24'),
  (7, 5, 2025, 2,  240000,  122000, '2024-12-24'),
-- Дирекция
  (8, 1, 2025, 1, 1755000, 1728000, '2024-12-18'),
  (8, 1, 2025, 2, 1755000, 1520000, '2024-12-18'),
  (8, 4, 2025, 1, 2100000, 2100000, '2024-12-18'),
  (8, 4, 2025, 2, 2100000, 1050000, '2024-12-18'),
  (8, 3, 2025, 1,  240000,  225000, '2024-12-18'),
  (8, 3, 2025, 2,  300000,  148000, '2024-12-18'),
  (8, 10, 2025, 1, 215000,  205000, '2024-12-18'),
  (8, 10, 2025, 2, 180000,   92000, '2024-12-18');

-- ============================================================
-- 9. ДОКУМЕНТЫ (~70 документов)
-- ============================================================
INSERT INTO document (doc_id, dept_id, item_id, type_id, doc_date, doc_amount, contr_inn, resp_emp_id) VALUES
-- 2023 Q1
  (1001, 1, 2, 1, '2023-01-15',  22400, '7701234567', 102),
  (1002, 1, 2, 8, '2023-01-20',   5200, '5012345678', 102),
  (1003, 1, 1, 3, '2023-02-01',    NULL, NULL,         101),
  (1004, 2, 3, 7, '2023-02-10', 115000, '7709876543', 201),
  (1005, 3, 6, 4, '2023-03-01', 487000, '7723456789', 301),
  (1006, 3, 7, 1, '2023-03-15', 275000, '7723456789', 302),
  (1007, 3, 11,1, '2023-03-20',  88000, '7799012345', 304),
  (1008, 7, 5, 1, '2023-01-25', 272000, '7756789012', 701),
  (1009, 8, 4, 4, '2023-01-01',1800000,'7756789012', 801),
-- 2023 Q2
  (1010, 2, 3, 2, '2023-04-15', 162000, '7709876543', 202),
  (1011, 3, 6, 1, '2023-05-10', 312000, '7723456789', 302),
  (1012, 3, 7, 1, '2023-06-01', 190000, '7723456789', 302),
  (1013, 5, 8, 4, '2023-04-20', 362000, '7867890123', 501),
  (1014, 6, 9, 2, '2023-05-05', 148000, '7812345678', 601),
  (1015, 4, 3, 7, '2023-06-12',  95000, '7709876543', 401),
  (1016, 8, 3, 7, '2023-05-20', 265000, '7709876543', 802),
  (1017, 1, 9, 2, '2023-06-15',  58500, '7812345678', 101),
-- 2023 Q3
  (1018, 3, 6, 1, '2023-07-05', 445000, '7723456789', 301),
  (1019, 3, 7, 1, '2023-08-10', 198000, '7723456789', 302),
  (1020, 5, 8, 1, '2023-07-20', 478000, '7867890123', 502),
  (1021, 7, 12,2, '2023-08-15', 318000, '7756789012', 701),
  (1022, 1, 9, 2, '2023-09-01',  31200, '7812345678', 101),
  (1023, 2, 3, 7, '2023-08-25', 128000, '7709876543', 203),
  (1024, 8, 3, 7, '2023-09-10', 195000, '7709876543', 802),
  (1025, 6, 9, 2, '2023-09-20', 102000, '7812345678', 601),
-- 2023 Q4
  (1026, 3, 6, 1, '2023-10-15', 712000, '7723456789', 301),
  (1027, 3, 7, 1, '2023-11-01', 362000, '7723456789', 302),
  (1028, 5, 8, 2, '2023-10-20', 512000, '7867890123', 501),
  (1029, 6, 9, 2, '2023-11-15', 195000, '7812345678', 601),
  (1030, 7, 12,2, '2023-12-01', 245000, '7756789012', 701),
  (1031, 8, 3, 7, '2023-11-20', 312000, '7709876543', 802),
  (1032, 8, 10,1, '2023-12-05', 195000, '7745678901', 803),
  (1033, 1, 9, 2, '2023-12-10',  47000, '7812345678', 101),
-- 2024 Q1
  (2001, 3, 6, 4, '2024-01-10', 578000, '7723456789', 301),
  (2002, 3, 7, 1, '2024-02-05', 315000, '7723456789', 302),
  (2003, 5, 8, 4, '2024-01-20', 285000, '7867890123', 501),
  (2004, 7, 12,2, '2024-02-15', 205000, '7756789012', 701),
  (2005, 7, 5, 1, '2024-01-25', 292000, '7756789012', 702),
  (2006, 2, 3, 7, '2024-03-01', 122000, '7709876543', 202),
  (2007, 4, 3, 7, '2024-02-28',  82000, '7709876543', 401),
  (2008, 8, 4, 1, '2024-01-01',1980000,'7756789012', 801),
  (2009, 6, 9, 2, '2024-03-15', 132000, '7812345678', 601),
-- 2024 Q2
  (2010, 3, 6, 1, '2024-04-15', 368000, '7723456789', 303),
  (2011, 3, 7, 1, '2024-05-01', 235000, '7723456789', 302),
  (2012, 5, 8, 2, '2024-05-20', 445000, '7867890123', 502),
  (2013, 6, 9, 2, '2024-06-10', 178000, '7812345678', 602),
  (2014, 8, 3, 7, '2024-05-15', 295000, '7709876543', 802),
  (2015, 2, 3, 2, '2024-06-05', 175000, '7709876543', 203),
  (2016, 4, 3, 2, '2024-05-25', 108000, '7731234567', 402),
  (2017, 1, 9, 2, '2024-06-20',  78500, '7812345678', 101),
-- 2024 Q3
  (2018, 3, 6, 1, '2024-07-10', 510000, '7723456789', 301),
  (2019, 3, 7, 1, '2024-08-01', 248000, '7723456789', 302),
  (2020, 5, 8, 1, '2024-07-25', 582000, '7867890123', 501),
  (2021, 7, 12,2, '2024-08-20', 372000, '7756789012', 701),
  (2022, 8, 3, 7, '2024-09-05', 215000, '7709876543', 803),
  (2023, 2, 3, 7, '2024-08-12', 138000, '7709876543', 203),
  (2024, 6, 9, 2, '2024-09-18', 125000, '7812345678', 601),
-- 2024 Q4
  (2025, 3, 6, 1, '2024-10-15', 825000, '7723456789', 301),
  (2026, 3, 7, 1, '2024-11-01', 438000, '7723456789', 302),
  (2027, 5, 8, 2, '2024-10-20', 628000, '7867890123', 503),
  (2028, 6, 9, 2, '2024-11-10', 232000, '7812345678', 601),
  (2029, 7, 12,2, '2024-12-01', 272000, '7756789012', 702),
  (2030, 8, 3, 7, '2024-11-20', 345000, '7709876543', 802),
  (2031, 8, 10,1, '2024-12-05', 215000, '7745678901', 803),
  (2032, 1, 9, 2, '2024-12-15',  57000, '7812345678', 101),
-- 2025 Q1
  (3001, 1, 2, 1, '2025-01-18',  27500, '5012345678', 102),
  (3002, 1, 9, 6, '2025-02-01',    NULL, NULL,         101),
  (3003, 2, 3, 7, '2025-02-10', 132000, '7709876543', 202),
  (3004, 3, 6, 4, '2025-01-15', 628000, '7723456789', 301),
  (3005, 3, 7, 1, '2025-02-20', 342000, '7723456789', 305),
  (3006, 3, 11,1, '2025-03-01', 108000, '7799012345', 304),
  (3007, 4, 3, 7, '2025-03-10',  88000, '7731234567', 402),
  (3008, 5, 8, 4, '2025-01-25', 332000, '7867890123', 501),
  (3009, 6, 9, 2, '2025-03-20', 148000, '7812345678', 602),
  (3010, 7, 12,2, '2025-02-15', 222000, '7756789012', 701),
  (3011, 7, 5, 1, '2025-01-28', 308000, '7756789012', 702),
  (3012, 8, 4, 1, '2025-01-01',2100000,'7756789012', 801),
  (3013, 8, 3, 7, '2025-03-05', 225000, '7709876543', 802),
-- 2025 Q2 (частично выполнен)
  (3014, 2, 3, 7, '2025-04-12',  85000, '7709876543', 203),
  (3015, 3, 6, 1, '2025-04-20', 220000, '7723456789', 302),
  (3016, 3, 7, 1, '2025-05-10', 138000, '7723456789', 302),
  (3017, 5, 8, 2, '2025-04-25', 265000, '7867890123', 503),
  (3018, 6, 9, 2, '2025-05-15',  98000, '7812345678', 601),
  (3019, 8, 4, 1, '2025-04-01',1050000,'7756789012', 801),
  (3020, 8, 3, 7, '2025-05-20', 148000, '7709876543', 803);

COMMIT;

```

## frontend/index.html

```html
<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Бухгалтерская система</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>

```

## frontend/src/App.vue

```html
<script setup>
</script>

<template>
  <RouterView />
</template>

```

## frontend/src/components/AppLayout.vue

```html
<script setup>
import Sidebar from './Sidebar.vue'
</script>

<template>
  <div class="flex min-h-screen bg-gray-50">
    <Sidebar />
    <main class="flex-1 overflow-auto">
      <RouterView />
    </main>
  </div>
</template>

```

## frontend/src/components/DataTable.vue

```html
<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  columns:  { type: Array,   required: true },
  rows:     { type: Array,   default: () => [] },
  total:    { type: Number,  default: 0 },
  page:     { type: Number,  default: 1 },
  pageSize: { type: Number,  default: 20 },
  loading:  { type: Boolean, default: false },
})

const emit = defineEmits(['update:page', 'add', 'edit', 'delete'])

const sortKey = ref('')
const sortDir = ref('asc')

function toggleSort(key) {
  if (sortKey.value === key) {
    sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortDir.value = 'asc'
  }
}

const sortedRows = computed(() => {
  if (!sortKey.value) return props.rows
  const col = props.columns.find(c => c.key === sortKey.value)
  return [...props.rows].sort((a, b) => {
    const va = col?.render ? col.render(a) : (a[sortKey.value] ?? '')
    const vb = col?.render ? col.render(b) : (b[sortKey.value] ?? '')
    if (va === vb) return 0
    const cmp = String(va).localeCompare(String(vb), 'ru', { numeric: true })
    return sortDir.value === 'asc' ? cmp : -cmp
  })
})

const totalPages = computed(() => Math.max(1, Math.ceil(props.total / props.pageSize)))

const pageNumbers = computed(() => {
  const tp = totalPages.value
  const cur = props.page
  if (tp <= 7) return Array.from({ length: tp }, (_, i) => i + 1)
  const set = new Set([1, tp, cur])
  if (cur > 1) set.add(cur - 1)
  if (cur < tp) set.add(cur + 1)
  return [...set].sort((a, b) => a - b)
})

function cellValue(col, row) {
  if (col.render) return col.render(row)
  const v = row[col.key]
  return v !== null && v !== undefined ? v : '—'
}
</script>

<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">

    <!-- Toolbar -->
    <div class="flex items-center justify-between px-5 py-3 border-b border-gray-100 bg-gray-50/60">
      <span class="text-sm text-gray-500">Всего записей: <strong class="text-gray-700">{{ total }}</strong></span>
      <button
        @click="$emit('add')"
        class="inline-flex items-center gap-1.5 px-3.5 py-1.5 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 active:bg-blue-800 transition-colors"
      >
        <span class="text-lg leading-none">+</span> Добавить
      </button>
    </div>

    <!-- Table -->
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-gray-100">
            <th
              v-for="col in columns"
              :key="col.key"
              class="px-4 py-2.5 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide whitespace-nowrap cursor-pointer select-none hover:bg-gray-50 transition-colors"
              @click="toggleSort(col.key)"
            >
              {{ col.label }}
              <span v-if="sortKey === col.key" class="ml-1 text-blue-500 font-bold">
                {{ sortDir === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
            <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide w-32">
              Действия
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td :colspan="columns.length + 1" class="py-12 text-center text-gray-400 text-sm">
              <span class="inline-block animate-pulse">Загрузка данных...</span>
            </td>
          </tr>
          <tr v-else-if="!sortedRows.length">
            <td :colspan="columns.length + 1" class="py-12 text-center text-gray-400 text-sm">
              Нет данных
            </td>
          </tr>
          <tr
            v-else
            v-for="(row, i) in sortedRows"
            :key="i"
            class="border-b border-gray-50 last:border-0 hover:bg-blue-50/30 transition-colors"
          >
            <td
              v-for="col in columns"
              :key="col.key"
              class="px-4 py-2.5 text-gray-700 whitespace-nowrap max-w-[220px] truncate"
              :title="String(cellValue(col, row))"
            >
              {{ cellValue(col, row) }}
            </td>
            <td class="px-4 py-2.5 text-right whitespace-nowrap">
              <button
                @click="$emit('edit', row)"
                class="text-blue-600 hover:text-blue-800 text-xs font-medium mr-3 transition-colors"
              >
                Изменить
              </button>
              <button
                @click="$emit('delete', row)"
                class="text-red-500 hover:text-red-700 text-xs font-medium transition-colors"
              >
                Удалить
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div class="flex items-center justify-between px-5 py-3 border-t border-gray-100 bg-gray-50/60">
      <span class="text-sm text-gray-500">
        Страница {{ page }} из {{ totalPages }}
      </span>
      <div class="flex items-center gap-1">
        <button
          :disabled="page <= 1"
          @click="$emit('update:page', page - 1)"
          class="px-2.5 py-1.5 text-sm rounded-lg border border-gray-200 bg-white hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >←</button>

        <template v-for="(num, idx) in pageNumbers" :key="num">
          <span
            v-if="idx > 0 && pageNumbers[idx - 1] < num - 1"
            class="px-1.5 text-gray-400 text-sm select-none"
          >…</span>
          <button
            @click="$emit('update:page', num)"
            class="px-2.5 py-1.5 text-sm rounded-lg border transition-colors min-w-[36px]"
            :class="num === page
              ? 'bg-blue-600 text-white border-blue-600 font-medium'
              : 'bg-white border-gray-200 hover:bg-gray-50 text-gray-700'"
          >{{ num }}</button>
        </template>

        <button
          :disabled="page >= totalPages"
          @click="$emit('update:page', page + 1)"
          class="px-2.5 py-1.5 text-sm rounded-lg border border-gray-200 bg-white hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >→</button>
      </div>
    </div>
  </div>
</template>

```

## frontend/src/components/FormModal.vue

```html
<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  title:      { type: String,  required: true },
  fields:     { type: Array,   required: true },
  modelValue: { type: Object,  default: () => ({}) },
  isEdit:     { type: Boolean, default: false },
  error:      { type: String,  default: '' },
})

const emit = defineEmits(['submit', 'close'])

const formData = ref({})

watch(
  () => props.modelValue,
  (val) => { formData.value = { ...(val || {}) } },
  { immediate: true, deep: true }
)

const visibleFields = computed(() =>
  props.fields.filter(f => !(f.createOnly && props.isEdit))
)

function handleSubmit() {
  emit('submit', { ...formData.value })
}
</script>

<template>
  <Teleport to="body">
    <div
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
      @mousedown.self="$emit('close')"
    >
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] flex flex-col">

        <!-- Header -->
        <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100">
          <h2 class="text-base font-semibold text-gray-800">{{ title }}</h2>
          <button
            @click="$emit('close')"
            class="w-7 h-7 flex items-center justify-center rounded-full text-gray-400 hover:bg-gray-100 hover:text-gray-600 transition-colors text-lg leading-none"
          >×</button>
        </div>

        <!-- Body -->
        <div class="overflow-y-auto flex-1 px-6 py-5">
          <div
            v-if="error"
            class="mb-4 px-4 py-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm"
          >
            {{ error }}
          </div>

          <div class="grid grid-cols-2 gap-x-5 gap-y-4">
            <div
              v-for="field in visibleFields"
              :key="field.key"
              :class="field.fullWidth ? 'col-span-2' : ''"
            >
              <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">
                {{ field.label }}
                <span v-if="field.required" class="text-red-400 normal-case font-normal ml-0.5">*</span>
              </label>

              <!-- Select -->
              <select
                v-if="field.type === 'select'"
                v-model="formData[field.key]"
                :required="field.required"
                :disabled="field.readOnly"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:text-gray-500"
              >
                <option :value="null">— не выбрано —</option>
                <option
                  v-for="opt in (field.options || [])"
                  :key="opt.value"
                  :value="opt.value"
                >{{ opt.label }}</option>
              </select>

              <!-- Checkbox -->
              <div v-else-if="field.type === 'checkbox'" class="flex items-center gap-2 mt-1">
                <input
                  type="checkbox"
                  v-model="formData[field.key]"
                  class="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span class="text-sm text-gray-600">{{ field.checkLabel || '' }}</span>
              </div>

              <!-- Textarea -->
              <textarea
                v-else-if="field.type === 'textarea'"
                v-model="formData[field.key]"
                :required="field.required"
                :disabled="field.readOnly"
                :placeholder="field.placeholder || ''"
                rows="3"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none disabled:bg-gray-100"
              />

              <!-- Default input -->
              <input
                v-else
                :type="field.type || 'text'"
                v-model="formData[field.key]"
                :required="field.required"
                :disabled="field.readOnly"
                :placeholder="field.placeholder || ''"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:text-gray-500"
              />
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="flex justify-end gap-3 px-6 py-4 border-t border-gray-100">
          <button
            type="button"
            @click="$emit('close')"
            class="px-4 py-2 text-sm text-gray-600 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >Отмена</button>
          <button
            type="button"
            @click="handleSubmit"
            class="px-5 py-2 text-sm text-white bg-blue-600 hover:bg-blue-700 active:bg-blue-800 rounded-lg transition-colors font-medium"
          >{{ isEdit ? 'Сохранить' : 'Создать' }}</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

```

## frontend/src/components/OlapChart.vue

```html
<script setup>
import { computed } from 'vue'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  PointElement,
  LineElement,
} from 'chart.js'
import { Bar, Pie, Line } from 'vue-chartjs'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  PointElement,
  LineElement,
)

const props = defineProps({
  type: { type: String, required: true }, // 'bar' | 'pie' | 'line' | 'stacked-bar'
  data: { type: Object, required: true },
  title: { type: String, default: '' },
})

const chartOptions = computed(() => {
  const base = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top' },
      title: props.title
        ? { display: true, text: props.title, font: { size: 14, weight: '600' } }
        : { display: false },
    },
  }
  if (props.type === 'stacked-bar') {
    return {
      ...base,
      scales: {
        x: { stacked: true },
        y: { stacked: true, beginAtZero: true },
      },
    }
  }
  if (props.type === 'bar' || props.type === 'line') {
    return {
      ...base,
      scales: { y: { beginAtZero: true } },
    }
  }
  return base
})
</script>

<template>
  <div class="bg-white border border-gray-200 rounded-xl shadow-sm p-4" style="height: 400px;">
    <Bar v-if="type === 'bar' || type === 'stacked-bar'" :data="data" :options="chartOptions" />
    <Pie v-else-if="type === 'pie'" :data="data" :options="chartOptions" />
    <Line v-else-if="type === 'line'" :data="data" :options="chartOptions" />
    <div v-else class="flex items-center justify-center h-full text-gray-400 text-sm">
      Неизвестный тип графика
    </div>
  </div>
</template>

```

## frontend/src/components/OlapControls.vue

```html
<script setup>
import { computed } from 'vue'

const props = defineProps({
  operation: { type: String, required: true },
  departments: { type: Array, default: () => [] },
  contractors: { type: Array, default: () => [] },
  items: { type: Array, default: () => [] },
  quarters: { type: Array, default: () => [] },
  selectedDeptId: { type: [Number, null], default: null },
  selectedContrInn: { type: [String, null], default: null },
  diceDeptId: { type: [Number, null], default: null },
  diceItemId: { type: [Number, null], default: null },
  diceQuarter: { type: [String, null], default: null },
})

const emit = defineEmits([
  'update:operation',
  'update:selectedDeptId',
  'update:selectedContrInn',
  'update:diceDeptId',
  'update:diceItemId',
  'update:diceQuarter',
  'apply',
])

const operations = [
  { key: 'rollup-dept',       label: 'Roll-up по отделу' },
  { key: 'rollup-item',       label: 'Roll-up по статье' },
  { key: 'rollup-quarter',    label: 'Roll-up по кварталу' },
  { key: 'slice-dept',        label: 'Срез по отделу' },
  { key: 'slice-contractor',  label: 'Срез по контрагенту' },
  { key: 'dice',              label: 'Dice' },
  { key: 'drilldown-dept',    label: 'Drill-down по отделу' },
  { key: 'cross-dept-item',   label: 'Кросс-таблица Отдел × Статья' },
]

const showDeptSelect = computed(() =>
  ['slice-dept', 'drilldown-dept'].includes(props.operation)
)
const showContractorSelect = computed(() => props.operation === 'slice-contractor')
const showDice = computed(() => props.operation === 'dice')

// Безопасные парсеры: Vue 3 убирает атрибут value при :value="null",
// из-за чего $event.target.value возвращает текст опции (truthy строку).
// Используем явную проверку на пустую строку.
function toIntOrNull(raw) {
  if (raw === '' || raw === null || raw === undefined) return null
  const n = Number(raw)
  return isNaN(n) ? null : n
}

function toStrOrNull(raw) {
  return (raw === '' || raw === null || raw === undefined) ? null : raw
}

function setOp(key) {
  emit('update:operation', key)
}
</script>

<template>
  <div class="bg-white border border-gray-200 rounded-xl shadow-sm p-5 mb-6">
    <h2 class="text-sm font-semibold text-gray-700 mb-3">Операция</h2>
    <div class="flex flex-wrap gap-2 mb-4">
      <button
        v-for="op in operations"
        :key="op.key"
        @click="setOp(op.key)"
        class="px-3 py-1.5 text-sm font-medium rounded-lg border transition-colors"
        :class="operation === op.key
          ? 'bg-blue-600 text-white border-blue-600'
          : 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'"
      >{{ op.label }}</button>
    </div>

    <!-- Фильтры -->
    <div class="flex flex-wrap items-end gap-4">
      <!-- Срез/Drill-down по отделу -->
      <div v-if="showDeptSelect" class="flex flex-col gap-1">
        <label class="text-xs font-medium text-gray-500">Отдел</label>
        <select
          :value="selectedDeptId ?? ''"
          @change="$emit('update:selectedDeptId', toIntOrNull($event.target.value))"
          class="border border-gray-300 rounded-lg px-3 py-2 text-sm min-w-[220px] focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">— выберите —</option>
          <option v-for="d in departments" :key="d.dept_id" :value="d.dept_id">
            {{ d.dept_name }}
          </option>
        </select>
      </div>

      <!-- Срез по контрагенту -->
      <div v-if="showContractorSelect" class="flex flex-col gap-1">
        <label class="text-xs font-medium text-gray-500">Контрагент</label>
        <select
          :value="selectedContrInn ?? ''"
          @change="$emit('update:selectedContrInn', toStrOrNull($event.target.value))"
          class="border border-gray-300 rounded-lg px-3 py-2 text-sm min-w-[260px] focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">— выберите —</option>
          <option v-for="c in contractors" :key="c.contr_inn" :value="c.contr_inn">
            {{ c.contr_name }} ({{ c.contr_inn }})
          </option>
        </select>
      </div>

      <!-- Dice -->
      <template v-if="showDice">
        <div class="flex flex-col gap-1">
          <label class="text-xs font-medium text-gray-500">Отдел</label>
          <select
            :value="diceDeptId ?? ''"
            @change="$emit('update:diceDeptId', toIntOrNull($event.target.value))"
            class="border border-gray-300 rounded-lg px-3 py-2 text-sm min-w-[200px] focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">— любой —</option>
            <option v-for="d in departments" :key="d.dept_id" :value="d.dept_id">
              {{ d.dept_name }}
            </option>
          </select>
        </div>

        <div class="flex flex-col gap-1">
          <label class="text-xs font-medium text-gray-500">Статья</label>
          <select
            :value="diceItemId ?? ''"
            @change="$emit('update:diceItemId', toIntOrNull($event.target.value))"
            class="border border-gray-300 rounded-lg px-3 py-2 text-sm min-w-[200px] focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">— любая —</option>
            <option v-for="it in items" :key="it.item_id" :value="it.item_id">
              {{ it.item_name }}
            </option>
          </select>
        </div>

        <div class="flex flex-col gap-1">
          <label class="text-xs font-medium text-gray-500">Квартал</label>
          <select
            :value="diceQuarter ?? ''"
            @change="$emit('update:diceQuarter', toStrOrNull($event.target.value))"
            class="border border-gray-300 rounded-lg px-3 py-2 text-sm min-w-[160px] focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">— любой —</option>
            <option v-for="q in quarters" :key="`${q.year}-${q.quarter}`" :value="`${q.year}-${q.quarter}`">
              {{ q.year }} Q{{ q.quarter }}
            </option>
          </select>
        </div>
      </template>

      <button
        @click="$emit('apply')"
        class="px-5 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors shadow-sm"
      >Применить</button>
    </div>
  </div>
</template>

```

## frontend/src/components/OlapTable.vue

```html
<script setup>
const props = defineProps({
  columns: { type: Array, required: true },
  rows: { type: Array, default: () => [] },
  emptyText: { type: String, default: 'Нет данных' },
  title: { type: String, default: '' },
})

const fmt = v =>
  v != null && v !== ''
    ? (typeof v === 'number' || !isNaN(Number(v)))
      ? Number(v).toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
      : v
    : '—'

function cellValue(row, col) {
  const val = row[col.key]
  if (col.format === 'number') return fmt(val)
  if (col.format === 'date' && val) return new Date(val).toLocaleDateString('ru-RU')
  return val ?? '—'
}

function cellClass(row, col) {
  if (col.format === 'number') return 'text-right text-gray-700'
  if (col.deviation) {
    const n = Number(row[col.key])
    if (n > 0) return 'text-right text-emerald-600 font-medium'
    if (n < 0) return 'text-right text-red-500 font-medium'
    return 'text-right text-gray-500'
  }
  return 'text-gray-700'
}
</script>

<template>
  <div class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm">
    <div v-if="title" class="px-4 py-3 border-b border-gray-100 bg-gray-50">
      <h3 class="text-sm font-semibold text-gray-700">{{ title }}</h3>
    </div>
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="bg-gray-50 border-b border-gray-100">
            <th
              v-for="col in columns"
              :key="col.key"
              class="px-4 py-2.5 text-xs font-semibold text-gray-500 uppercase tracking-wide"
              :class="col.format === 'number' ? 'text-right' : 'text-left'"
            >{{ col.label }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!rows.length">
            <td :colspan="columns.length" class="py-8 text-center text-gray-400">
              {{ emptyText }}
            </td>
          </tr>
          <tr
            v-for="(row, i) in rows"
            :key="i"
            class="border-b border-gray-50 last:border-0 hover:bg-blue-50/30 transition-colors"
          >
            <td
              v-for="col in columns"
              :key="col.key"
              class="px-4 py-2.5"
              :class="cellClass(row, col)"
            >{{ cellValue(row, col) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

```

## frontend/src/components/Sidebar.vue

```html
<script setup>
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()

const navItems = [
  { path: '/',            label: 'Дашборд',      icon: '▦' },
  { path: '/employees',   label: 'Сотрудники',   icon: '◉' },
  { path: '/departments', label: 'Отделы',        icon: '⊞' },
  { path: '/documents',   label: 'Документы',    icon: '◧' },
  { path: '/budget',      label: 'Бюджет',       icon: '◈' },
  { path: '/contractors', label: 'Контрагенты',  icon: '◎' },
  { path: '/positions',   label: 'Должности',    icon: '◉' },
  { path: '/olap',        label: 'OLAP-анализ',  icon: '◫' },
]

function isActive(path) {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}
</script>

<template>
  <aside class="w-56 bg-slate-900 text-white flex flex-col min-h-screen shrink-0">
    <div class="px-5 py-5 border-b border-slate-700">
      <h1 class="text-base font-bold text-white tracking-wide">Бухгалтерия</h1>
      <p class="text-xs text-slate-500 mt-0.5">Учётная система</p>
    </div>

    <nav class="flex-1 py-3">
      <RouterLink
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="flex items-center gap-3 px-5 py-2.5 text-sm transition-colors"
        :class="isActive(item.path)
          ? 'bg-blue-600 text-white font-medium'
          : 'text-slate-400 hover:bg-slate-800 hover:text-white'"
      >
        <span class="text-base w-4 text-center select-none">{{ item.icon }}</span>
        <span>{{ item.label }}</span>
      </RouterLink>
    </nav>

    <div class="px-5 py-4 border-t border-slate-700">
      <p class="text-xs text-slate-600">v0.1.0</p>
    </div>
  </aside>
</template>

```

## frontend/src/main.js

```js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'

createApp(App).use(router).mount('#app')

```

## frontend/src/router/index.js

```js
import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'
import Dashboard from '../views/Dashboard.vue'
import Employees from '../views/Employees.vue'
import Departments from '../views/Departments.vue'
import Documents from '../views/Documents.vue'
import Budget from '../views/Budget.vue'
import Contractors from '../views/Contractors.vue'
import Positions from '../views/Positions.vue'
import Olap from '../views/OlapView.vue'

const routes = [
  {
    path: '/',
    component: AppLayout,
    children: [
      { path: '', component: Dashboard },
      { path: 'employees', component: Employees },
      { path: 'departments', component: Departments },
      { path: 'documents', component: Documents },
      { path: 'budget', component: Budget },
      { path: 'contractors', component: Contractors },
      { path: 'positions', component: Positions },
      { path: 'olap', component: Olap },
    ],
  },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})

```

## frontend/src/services/api.js

```js
import axios from 'axios'

const http = axios.create({ baseURL: 'http://localhost:8000/api' })

export const api = {
  getAll(endpoint, page = 1, size = 20) {
    return http.get(`/${endpoint}`, { params: { page, size } }).then(r => r.data)
  },

  getOne(endpoint, id) {
    return http.get(`/${endpoint}/${id}`).then(r => r.data)
  },

  create(endpoint, data) {
    return http.post(`/${endpoint}`, data).then(r => r.data)
  },

  update(endpoint, id, data) {
    return http.put(`/${endpoint}/${id}`, data).then(r => r.data)
  },

  delete(endpoint, id) {
    return http.delete(`/${endpoint}/${id}`)
  },

  olap: {
    rollupByDept: () =>
      http.get('/olap/rollup-by-dept').then(r => r.data),
    rollupByItem: () =>
      http.get('/olap/rollup-by-item').then(r => r.data),
    rollupByQuarter: () =>
      http.get('/olap/rollup-by-quarter').then(r => r.data),
    crossDeptItem: () =>
      http.get('/olap/cross-dept-item').then(r => r.data),
    drilldownDept: (deptId) =>
      http.get('/olap/drilldown-dept', { params: { dept_id: deptId } }).then(r => r.data),
    sliceByDept: (deptId) =>
      http.get('/olap/slice-by-dept', { params: { dept_id: deptId } }).then(r => r.data),
    sliceByContractor: (contrInn) =>
      http.get('/olap/slice-by-contractor', { params: { contr_inn: contrInn } }).then(r => r.data),
    dice: (params) =>
      http.get('/olap/dice', { params }).then(r => r.data),
  },
}

```

## frontend/src/style.css

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

```

## frontend/src/views/Budget.vue

```html
<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../services/api'
import DataTable from '../components/DataTable.vue'
import FormModal from '../components/FormModal.vue'

const fmt = v => v != null ? Number(v).toLocaleString('ru-RU', { minimumFractionDigits: 2 }) : '—'

const columns = [
  { key: 'dept_name',      label: 'Отдел' },
  { key: 'item_name',      label: 'Статья' },
  { key: 'budget_year',    label: 'Год' },
  { key: 'budget_quarter', label: 'Квартал' },
  { key: 'plan_rub', label: 'План, ₽',    render: r => fmt(r.plan_rub) },
  { key: 'fact_rub', label: 'Факт, ₽',    render: r => fmt(r.fact_rub) },
  { key: 'deviation', label: 'Отклонение, ₽',
    render: r => {
      if (r.plan_rub == null || r.fact_rub == null) return '—'
      return fmt(Number(r.plan_rub) - Number(r.fact_rub))
    },
  },
  { key: 'approved_date', label: 'Дата утв.' },
]

const deptOptions = ref([])
const itemOptions = ref([])

const formFields = computed(() => [
  { key: 'dept_id',        label: 'Отдел',          type: 'select', required: true, createOnly: true, options: deptOptions.value },
  { key: 'item_id',        label: 'Статья бюджета', type: 'select', required: true, createOnly: true, options: itemOptions.value },
  { key: 'budget_year',    label: 'Год',            type: 'number', required: true, createOnly: true },
  { key: 'budget_quarter', label: 'Квартал (1–4)',  type: 'number', required: true, createOnly: true },
  { key: 'plan_rub',       label: 'План (руб.)',     type: 'number', required: true },
  { key: 'fact_rub',       label: 'Факт (руб.)',     type: 'number', required: true },
  { key: 'approved_date',  label: 'Дата утверждения', type: 'date' },
])

const rows     = ref([])
const total    = ref(0)
const page     = ref(1)
const pageSize = 20
const loading  = ref(false)
const error    = ref('')

const showModal  = ref(false)
const isEdit     = ref(false)
const formData   = ref({})
const currentRow = ref(null)
const saveError  = ref('')

// Composite key: dept_id/item_id/year/quarter
function budgetKey(row) {
  return `${row.dept_id}/${row.item_id}/${row.budget_year}/${row.budget_quarter}`
}

async function loadPage(p) {
  loading.value = true
  error.value   = ''
  try {
    const data = await api.getAll('budget', p, pageSize)
    rows.value  = data.items
    total.value = data.total
    page.value  = p
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const [depts, items] = await Promise.all([
    api.getAll('department',  1, 1000),
    api.getAll('budget-item', 1, 1000),
  ])
  deptOptions.value = depts.items.map(d => ({ value: d.dept_id, label: d.dept_name }))
  itemOptions.value = items.items.map(i => ({ value: i.item_id, label: i.item_name }))
  await loadPage(1)
})

function openAdd() {
  isEdit.value    = false
  formData.value  = {}
  saveError.value = ''
  showModal.value = true
}

function openEdit(row) {
  isEdit.value     = true
  currentRow.value = row
  formData.value   = { ...row }
  saveError.value  = ''
  showModal.value  = true
}

async function handleDelete(row) {
  if (!confirm(`Удалить запись бюджета (${row.dept_name}, ${row.item_name}, ${row.budget_year} кв.${row.budget_quarter})?`)) return
  try {
    await api.delete('budget', budgetKey(row))
    await loadPage(page.value)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка удаления'
  }
}

function pickFields(raw, edit) {
  const keys = formFields.value
    .filter(f => !(f.createOnly && edit))
    .map(f => f.key)
  return Object.fromEntries(keys.map(k => [k, raw[k] === '' ? null : raw[k]]))
}

async function handleSubmit(raw) {
  saveError.value = ''
  try {
    const data = pickFields(raw, isEdit.value)
    if (isEdit.value) {
      await api.update('budget', budgetKey(currentRow.value), data)
    } else {
      await api.create('budget', data)
    }
    showModal.value = false
    await loadPage(page.value)
  } catch (e) {
    saveError.value = e.response?.data?.detail || 'Ошибка сохранения'
  }
}
</script>

<template>
  <div class="p-8">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Бюджет</h1>
      <p class="text-sm text-gray-500 mt-1">Плановые и фактические расходы по отделам</p>
    </div>
    <div v-if="error" class="mb-4 px-4 py-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
      {{ error }}
    </div>
    <DataTable
      :columns="columns" :rows="rows" :total="total"
      :page="page" :page-size="pageSize" :loading="loading"
      @update:page="loadPage" @add="openAdd" @edit="openEdit" @delete="handleDelete"
    />
    <FormModal
      v-if="showModal"
      :title="isEdit ? 'Редактировать запись бюджета' : 'Добавить запись бюджета'"
      :fields="formFields" :model-value="formData"
      :is-edit="isEdit" :error="saveError"
      @submit="handleSubmit" @close="showModal = false"
    />
  </div>
</template>

```

## frontend/src/views/Contractors.vue

```html
<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../services/api'
import DataTable from '../components/DataTable.vue'
import FormModal from '../components/FormModal.vue'

const columns = [
  { key: 'contr_inn',     label: 'ИНН' },
  { key: 'contr_name',    label: 'Наименование' },
  { key: 'contr_address', label: 'Адрес' },
  { key: 'contr_phone',   label: 'Телефон' },
]

const formFields = computed(() => [
  { key: 'contr_inn',     label: 'ИНН',          type: 'text', required: true, createOnly: true },
  { key: 'contr_name',    label: 'Наименование',  type: 'text', required: true },
  { key: 'contr_address', label: 'Адрес',         type: 'text', fullWidth: true },
  { key: 'contr_phone',   label: 'Телефон',       type: 'text' },
])

const rows     = ref([])
const total    = ref(0)
const page     = ref(1)
const pageSize = 20
const loading  = ref(false)
const error    = ref('')

const showModal  = ref(false)
const isEdit     = ref(false)
const formData   = ref({})
const currentRow = ref(null)
const saveError  = ref('')

async function loadPage(p) {
  loading.value = true
  error.value   = ''
  try {
    const data = await api.getAll('contractor', p, pageSize)
    rows.value  = data.items
    total.value = data.total
    page.value  = p
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
}

onMounted(() => loadPage(1))

function openAdd() {
  isEdit.value    = false
  formData.value  = {}
  saveError.value = ''
  showModal.value = true
}

function openEdit(row) {
  isEdit.value     = true
  currentRow.value = row
  formData.value   = { ...row }
  saveError.value  = ''
  showModal.value  = true
}

async function handleDelete(row) {
  if (!confirm(`Удалить контрагента «${row.contr_name}»?`)) return
  try {
    await api.delete('contractor', row.contr_inn)
    await loadPage(page.value)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка удаления'
  }
}

function pickFields(raw, edit) {
  const keys = formFields.value
    .filter(f => !(f.createOnly && edit))
    .map(f => f.key)
  return Object.fromEntries(keys.map(k => [k, raw[k] === '' ? null : raw[k]]))
}

async function handleSubmit(raw) {
  saveError.value = ''
  try {
    const data = pickFields(raw, isEdit.value)
    if (isEdit.value) {
      await api.update('contractor', currentRow.value.contr_inn, data)
    } else {
      await api.create('contractor', data)
    }
    showModal.value = false
    await loadPage(page.value)
  } catch (e) {
    saveError.value = e.response?.data?.detail || 'Ошибка сохранения'
  }
}
</script>

<template>
  <div class="p-8">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Контрагенты</h1>
      <p class="text-sm text-gray-500 mt-1">Справочник организаций и ИП</p>
    </div>
    <div v-if="error" class="mb-4 px-4 py-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
      {{ error }}
    </div>
    <DataTable
      :columns="columns" :rows="rows" :total="total"
      :page="page" :page-size="pageSize" :loading="loading"
      @update:page="loadPage" @add="openAdd" @edit="openEdit" @delete="handleDelete"
    />
    <FormModal
      v-if="showModal"
      :title="isEdit ? 'Редактировать контрагента' : 'Добавить контрагента'"
      :fields="formFields" :model-value="formData"
      :is-edit="isEdit" :error="saveError"
      @submit="handleSubmit" @close="showModal = false"
    />
  </div>
</template>

```

## frontend/src/views/Dashboard.vue

```html
<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { api } from '../services/api'

const router = useRouter()

const cards = [
  { label: 'Сотрудники',     endpoint: 'employee',    path: '/employees',   color: 'blue' },
  { label: 'Отделы',          endpoint: 'department',  path: '/departments', color: 'indigo' },
  { label: 'Документы',       endpoint: 'document',    path: '/documents',   color: 'violet' },
  { label: 'Бюджет',          endpoint: 'budget',      path: '/budget',      color: 'emerald' },
  { label: 'Контрагенты',     endpoint: 'contractor',  path: '/contractors', color: 'amber' },
  { label: 'Должности',       endpoint: 'position',    path: '/positions',   color: 'sky' },
  { label: 'Статьи бюджета',  endpoint: 'budget-item', path: null,           color: 'teal' },
  { label: 'Типы документов', endpoint: 'doc-type',    path: null,           color: 'rose' },
]

const counts = ref({})
const loading = ref(true)

const colors = {
  blue:    { wrap: 'bg-blue-50 border-blue-200',     num: 'text-blue-600',    btn: 'bg-blue-600 hover:bg-blue-700' },
  indigo:  { wrap: 'bg-indigo-50 border-indigo-200', num: 'text-indigo-600',  btn: 'bg-indigo-600 hover:bg-indigo-700' },
  violet:  { wrap: 'bg-violet-50 border-violet-200', num: 'text-violet-600',  btn: 'bg-violet-600 hover:bg-violet-700' },
  emerald: { wrap: 'bg-emerald-50 border-emerald-200', num: 'text-emerald-600', btn: 'bg-emerald-600 hover:bg-emerald-700' },
  amber:   { wrap: 'bg-amber-50 border-amber-200',   num: 'text-amber-600',   btn: 'bg-amber-600 hover:bg-amber-700' },
  sky:     { wrap: 'bg-sky-50 border-sky-200',       num: 'text-sky-600',     btn: 'bg-sky-600 hover:bg-sky-700' },
  teal:    { wrap: 'bg-teal-50 border-teal-200',     num: 'text-teal-600',    btn: 'bg-teal-600 hover:bg-teal-700' },
  rose:    { wrap: 'bg-rose-50 border-rose-200',     num: 'text-rose-600',    btn: 'bg-rose-600 hover:bg-rose-700' },
}

onMounted(async () => {
  const results = await Promise.allSettled(
    cards.map(c => api.getAll(c.endpoint, 1, 1))
  )
  results.forEach((r, i) => {
    counts.value[cards[i].endpoint] = r.status === 'fulfilled' ? r.value.total : '?'
  })
  loading.value = false
})
</script>

<template>
  <div class="p-8">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-800">Дашборд</h1>
      <p class="text-sm text-gray-500 mt-1">Обзор данных учётной системы</p>
    </div>

    <!-- Stat cards -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-10">
      <div
        v-for="card in cards"
        :key="card.endpoint"
        class="rounded-xl border p-5 flex flex-col gap-3"
        :class="colors[card.color].wrap"
      >
        <p class="text-sm font-medium text-gray-600">{{ card.label }}</p>
        <p class="text-3xl font-bold tracking-tight" :class="colors[card.color].num">
          <span v-if="loading" class="opacity-30">—</span>
          <span v-else>{{ counts[card.endpoint] ?? '?' }}</span>
        </p>
        <button
          v-if="card.path"
          @click="router.push(card.path)"
          class="mt-auto text-xs text-white px-3 py-1.5 rounded-lg font-medium transition-colors"
          :class="colors[card.color].btn"
        >
          Перейти →
        </button>
        <span v-else class="mt-auto text-xs text-gray-400 italic">Справочник</span>
      </div>
    </div>

    <!-- Quick nav -->
    <div>
      <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Быстрый переход</h2>
      <div class="flex flex-wrap gap-2">
        <RouterLink
          v-for="item in [
            { path: '/employees',   label: 'Сотрудники' },
            { path: '/departments', label: 'Отделы' },
            { path: '/documents',   label: 'Документы' },
            { path: '/budget',      label: 'Бюджет' },
            { path: '/contractors', label: 'Контрагенты' },
            { path: '/positions',   label: 'Должности' },
            { path: '/olap',        label: 'OLAP-анализ' },
          ]"
          :key="item.path"
          :to="item.path"
          class="px-4 py-2 bg-white border border-gray-200 rounded-lg text-sm text-gray-700 hover:border-blue-400 hover:text-blue-600 transition-colors shadow-sm"
        >
          {{ item.label }}
        </RouterLink>
      </div>
    </div>
  </div>
</template>

```

## frontend/src/views/Departments.vue

```html
<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../services/api'
import DataTable from '../components/DataTable.vue'
import FormModal from '../components/FormModal.vue'

const columns = [
  { key: 'dept_id',         label: 'ID' },
  { key: 'dept_name',       label: 'Наименование' },
  { key: 'emp_count',       label: 'Сотрудников' },
  { key: 'floor_num',       label: 'Этаж' },
  { key: 'room_num',        label: 'Кабинет' },
  { key: 'dept_phone',      label: 'Телефон' },
  { key: 'head_emp_name',   label: 'Руководитель' },
  { key: 'created_date',    label: 'Создан' },
]

const empOptions = ref([])

const formFields = computed(() => [
  { key: 'dept_id',           label: 'ID',            type: 'number', required: true, createOnly: true },
  { key: 'dept_name',         label: 'Наименование',  type: 'text',   required: true, fullWidth: true },
  { key: 'emp_count',         label: 'Кол-во сотр.',  type: 'number' },
  { key: 'floor_num',         label: 'Этаж',          type: 'number' },
  { key: 'room_num',          label: 'Кабинет',       type: 'text' },
  { key: 'dept_phone',        label: 'Телефон',       type: 'text' },
  { key: 'dept_email',        label: 'Email',         type: 'email' },
  { key: 'created_date',      label: 'Дата создания', type: 'date' },
  { key: 'head_emp_id',       label: 'Руководитель',  type: 'select', options: empOptions.value },
  { key: 'head_appoint_date', label: 'Дата назначения', type: 'date' },
])

const rows     = ref([])
const total    = ref(0)
const page     = ref(1)
const pageSize = 20
const loading  = ref(false)
const error    = ref('')

const showModal  = ref(false)
const isEdit     = ref(false)
const formData   = ref({})
const currentRow = ref(null)
const saveError  = ref('')

async function loadPage(p) {
  loading.value = true
  error.value   = ''
  try {
    const data = await api.getAll('department', p, pageSize)
    rows.value  = data.items
    total.value = data.total
    page.value  = p
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const emps = await api.getAll('employee', 1, 1000)
  empOptions.value = emps.items.map(e => ({
    value: e.emp_id,
    label: `${e.last_name} ${e.first_name}${e.middle_name ? ' ' + e.middle_name : ''}`,
  }))
  await loadPage(1)
})

function openAdd() {
  isEdit.value    = false
  formData.value  = { emp_count: 0 }
  saveError.value = ''
  showModal.value = true
}

function openEdit(row) {
  isEdit.value     = true
  currentRow.value = row
  formData.value   = { ...row }
  saveError.value  = ''
  showModal.value  = true
}

async function handleDelete(row) {
  if (!confirm(`Удалить отдел «${row.dept_name}»?`)) return
  try {
    await api.delete('department', row.dept_id)
    await loadPage(page.value)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка удаления'
  }
}

function pickFields(raw, edit) {
  const keys = formFields.value
    .filter(f => !(f.createOnly && edit))
    .map(f => f.key)
  return Object.fromEntries(keys.map(k => [k, raw[k] === '' ? null : raw[k]]))
}

async function handleSubmit(raw) {
  saveError.value = ''
  try {
    const data = pickFields(raw, isEdit.value)
    if (isEdit.value) {
      await api.update('department', currentRow.value.dept_id, data)
    } else {
      await api.create('department', data)
    }
    showModal.value = false
    await loadPage(page.value)
  } catch (e) {
    saveError.value = e.response?.data?.detail || 'Ошибка сохранения'
  }
}
</script>

<template>
  <div class="p-8">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Отделы</h1>
      <p class="text-sm text-gray-500 mt-1">Структурные подразделения организации</p>
    </div>
    <div v-if="error" class="mb-4 px-4 py-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
      {{ error }}
    </div>
    <DataTable
      :columns="columns" :rows="rows" :total="total"
      :page="page" :page-size="pageSize" :loading="loading"
      @update:page="loadPage" @add="openAdd" @edit="openEdit" @delete="handleDelete"
    />
    <FormModal
      v-if="showModal"
      :title="isEdit ? 'Редактировать отдел' : 'Добавить отдел'"
      :fields="formFields" :model-value="formData"
      :is-edit="isEdit" :error="saveError"
      @submit="handleSubmit" @close="showModal = false"
    />
  </div>
</template>

```

## frontend/src/views/Documents.vue

```html
<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../services/api'
import DataTable from '../components/DataTable.vue'
import FormModal from '../components/FormModal.vue'

const fmt = v => v != null ? Number(v).toLocaleString('ru-RU', { minimumFractionDigits: 2 }) : '—'

const columns = [
  { key: 'doc_id',        label: 'ID' },
  { key: 'doc_date',      label: 'Дата' },
  { key: 'type_name',     label: 'Тип' },
  { key: 'dept_name',     label: 'Отдел' },
  { key: 'item_name',     label: 'Статья' },
  { key: 'contr_name',    label: 'Контрагент' },
  { key: 'resp_emp_name', label: 'Ответственный' },
  { key: 'doc_amount', label: 'Сумма, ₽', render: r => fmt(r.doc_amount) },
]

const deptOptions     = ref([])
const itemOptions     = ref([])
const typeOptions     = ref([])
const contrOptions    = ref([])
const empOptions      = ref([])

const formFields = computed(() => [
  { key: 'doc_id',      label: 'ID',              type: 'number', required: true, createOnly: true },
  { key: 'doc_date',    label: 'Дата',            type: 'date',   required: true },
  { key: 'dept_id',     label: 'Отдел',           type: 'select', required: true, options: deptOptions.value },
  { key: 'type_id',     label: 'Тип документа',   type: 'select', required: true, options: typeOptions.value },
  { key: 'item_id',     label: 'Статья бюджета',  type: 'select', required: true, options: itemOptions.value },
  { key: 'resp_emp_id', label: 'Ответственный',   type: 'select', required: true, options: empOptions.value },
  { key: 'contr_inn',   label: 'Контрагент',      type: 'select', options: contrOptions.value },
  { key: 'doc_amount',  label: 'Сумма',           type: 'number' },
])

const rows     = ref([])
const total    = ref(0)
const page     = ref(1)
const pageSize = 20
const loading  = ref(false)
const error    = ref('')

const showModal  = ref(false)
const isEdit     = ref(false)
const formData   = ref({})
const currentRow = ref(null)
const saveError  = ref('')

async function loadPage(p) {
  loading.value = true
  error.value   = ''
  try {
    const data = await api.getAll('document', p, pageSize)
    rows.value  = data.items
    total.value = data.total
    page.value  = p
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const [depts, items, types, contrs, emps] = await Promise.all([
    api.getAll('department',  1, 1000),
    api.getAll('budget-item', 1, 1000),
    api.getAll('doc-type',    1, 1000),
    api.getAll('contractor',  1, 1000),
    api.getAll('employee',    1, 1000),
  ])
  deptOptions.value  = depts.items.map(d => ({ value: d.dept_id,      label: d.dept_name }))
  itemOptions.value  = items.items.map(i => ({ value: i.item_id,      label: i.item_name }))
  typeOptions.value  = types.items.map(t => ({ value: t.type_id,      label: t.type_name }))
  contrOptions.value = contrs.items.map(c => ({ value: c.contr_inn,   label: `${c.contr_inn} — ${c.contr_name}` }))
  empOptions.value   = emps.items.map(e => ({
    value: e.emp_id,
    label: `${e.last_name} ${e.first_name}`,
  }))
  await loadPage(1)
})

function openAdd() {
  isEdit.value    = false
  formData.value  = {}
  saveError.value = ''
  showModal.value = true
}

function openEdit(row) {
  isEdit.value     = true
  currentRow.value = row
  formData.value   = { ...row }
  saveError.value  = ''
  showModal.value  = true
}

async function handleDelete(row) {
  if (!confirm(`Удалить документ #${row.doc_id}?`)) return
  try {
    await api.delete('document', row.doc_id)
    await loadPage(page.value)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка удаления'
  }
}

function pickFields(raw, edit) {
  const keys = formFields.value
    .filter(f => !(f.createOnly && edit))
    .map(f => f.key)
  return Object.fromEntries(keys.map(k => [k, raw[k] === '' ? null : raw[k]]))
}

async function handleSubmit(raw) {
  saveError.value = ''
  try {
    const data = pickFields(raw, isEdit.value)
    if (isEdit.value) {
      await api.update('document', currentRow.value.doc_id, data)
    } else {
      await api.create('document', data)
    }
    showModal.value = false
    await loadPage(page.value)
  } catch (e) {
    saveError.value = e.response?.data?.detail || 'Ошибка сохранения'
  }
}
</script>

<template>
  <div class="p-8">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Документы</h1>
      <p class="text-sm text-gray-500 mt-1">Бухгалтерские и финансовые документы</p>
    </div>
    <div v-if="error" class="mb-4 px-4 py-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
      {{ error }}
    </div>
    <DataTable
      :columns="columns" :rows="rows" :total="total"
      :page="page" :page-size="pageSize" :loading="loading"
      @update:page="loadPage" @add="openAdd" @edit="openEdit" @delete="handleDelete"
    />
    <FormModal
      v-if="showModal"
      :title="isEdit ? 'Редактировать документ' : 'Добавить документ'"
      :fields="formFields" :model-value="formData"
      :is-edit="isEdit" :error="saveError"
      @submit="handleSubmit" @close="showModal = false"
    />
  </div>
</template>

```

## frontend/src/views/Employees.vue

```html
<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../services/api'
import DataTable from '../components/DataTable.vue'
import FormModal from '../components/FormModal.vue'

const columns = [
  { key: 'emp_id',    label: 'ID' },
  { key: 'full_name', label: 'ФИО',
    render: r => [r.last_name, r.first_name, r.middle_name].filter(Boolean).join(' ') },
  { key: 'position_name', label: 'Должность' },
  { key: 'dept_name',     label: 'Отдел' },
  { key: 'salary', label: 'Зарплата, ₽',
    render: r => r.salary != null ? Number(r.salary).toLocaleString('ru-RU') : '—' },
  { key: 'hire_date', label: 'Дата найма' },
]

const deptOptions     = ref([])
const positionOptions = ref([])

const formFields = computed(() => [
  { key: 'emp_id',      label: 'ID',            type: 'number', required: true, createOnly: true },
  { key: 'last_name',   label: 'Фамилия',       type: 'text',   required: true },
  { key: 'first_name',  label: 'Имя',           type: 'text',   required: true },
  { key: 'middle_name', label: 'Отчество',       type: 'text' },
  { key: 'dept_id',     label: 'Отдел',         type: 'select', required: true, options: deptOptions.value },
  { key: 'position_id', label: 'Должность',     type: 'select', required: true, options: positionOptions.value },
  { key: 'salary',      label: 'Зарплата',      type: 'number', required: true },
  { key: 'hire_date',   label: 'Дата найма',    type: 'date',   required: true },
  { key: 'birth_date',  label: 'Дата рождения', type: 'date' },
  { key: 'education',   label: 'Образование',   type: 'text' },
  { key: 'inn',         label: 'ИНН',           type: 'text' },
  { key: 'snils',       label: 'СНИЛС',         type: 'text' },
  { key: 'emp_phone',   label: 'Телефон',       type: 'text' },
  { key: 'emp_email',   label: 'Email',         type: 'email' },
])

const rows     = ref([])
const total    = ref(0)
const page     = ref(1)
const pageSize = 20
const loading  = ref(false)
const error    = ref('')

const showModal  = ref(false)
const isEdit     = ref(false)
const formData   = ref({})
const currentRow = ref(null)
const saveError  = ref('')

async function loadPage(p) {
  loading.value = true
  error.value   = ''
  try {
    const data = await api.getAll('employee', p, pageSize)
    rows.value  = data.items
    total.value = data.total
    page.value  = p
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const [depts, positions] = await Promise.all([
    api.getAll('department', 1, 1000),
    api.getAll('position', 1, 1000),
  ])
  deptOptions.value     = depts.items.map(d => ({ value: d.dept_id, label: d.dept_name }))
  positionOptions.value = positions.items.map(p => ({ value: p.position_id, label: p.position_name }))
  await loadPage(1)
})

function openAdd() {
  isEdit.value    = false
  formData.value  = {}
  saveError.value = ''
  showModal.value = true
}

function openEdit(row) {
  isEdit.value     = true
  currentRow.value = row
  formData.value   = { ...row }
  saveError.value  = ''
  showModal.value  = true
}

async function handleDelete(row) {
  if (!confirm(`Удалить сотрудника #${row.emp_id} — ${row.last_name} ${row.first_name}?`)) return
  try {
    await api.delete('employee', row.emp_id)
    await loadPage(page.value)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка удаления'
  }
}

function pickFields(raw, edit) {
  const keys = formFields.value
    .filter(f => !(f.createOnly && edit))
    .map(f => f.key)
  return Object.fromEntries(keys.map(k => [k, raw[k] === '' ? null : raw[k]]))
}

async function handleSubmit(raw) {
  saveError.value = ''
  try {
    const data = pickFields(raw, isEdit.value)
    if (isEdit.value) {
      await api.update('employee', currentRow.value.emp_id, data)
    } else {
      await api.create('employee', data)
    }
    showModal.value = false
    await loadPage(page.value)
  } catch (e) {
    saveError.value = e.response?.data?.detail || 'Ошибка сохранения'
  }
}
</script>

<template>
  <div class="p-8">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Сотрудники</h1>
      <p class="text-sm text-gray-500 mt-1">Управление кадровым составом</p>
    </div>
    <div v-if="error" class="mb-4 px-4 py-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
      {{ error }}
    </div>
    <DataTable
      :columns="columns" :rows="rows" :total="total"
      :page="page" :page-size="pageSize" :loading="loading"
      @update:page="loadPage" @add="openAdd" @edit="openEdit" @delete="handleDelete"
    />
    <FormModal
      v-if="showModal"
      :title="isEdit ? 'Редактировать сотрудника' : 'Добавить сотрудника'"
      :fields="formFields" :model-value="formData"
      :is-edit="isEdit" :error="saveError"
      @submit="handleSubmit" @close="showModal = false"
    />
  </div>
</template>

```

## frontend/src/views/Olap.vue

```html
<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../services/api'

const activeTab = ref('dept')

const tabs = [
  { key: 'dept',    label: 'По отделам' },
  { key: 'item',    label: 'По статьям' },
  { key: 'quarter', label: 'По кварталам' },
  { key: 'drill',   label: 'Детализация по отделу' },
]

// ── Rollup by dept ─────────────────────────────────────────────────────────────
const deptData   = ref([])
const deptLoad   = ref(false)

async function loadDept() {
  deptLoad.value = true
  try { deptData.value = await api.olap.rollupByDept() }
  catch { deptData.value = [] }
  finally { deptLoad.value = false }
}

// ── Rollup by item ─────────────────────────────────────────────────────────────
const itemData = ref([])
const itemLoad = ref(false)

async function loadItem() {
  itemLoad.value = true
  try { itemData.value = await api.olap.rollupByItem() }
  catch { itemData.value = [] }
  finally { itemLoad.value = false }
}

// ── Rollup by quarter ──────────────────────────────────────────────────────────
const quarterData = ref([])
const quarterLoad = ref(false)

async function loadQuarter() {
  quarterLoad.value = true
  try { quarterData.value = await api.olap.rollupByQuarter() }
  catch { quarterData.value = [] }
  finally { quarterLoad.value = false }
}

// ── Drilldown by dept ──────────────────────────────────────────────────────────
const deptOptions    = ref([])
const selectedDeptId = ref(null)
const drillData      = ref(null)
const drillLoad      = ref(false)

async function loadDrilldown() {
  if (!selectedDeptId.value) return
  drillLoad.value = true
  drillData.value = null
  try { drillData.value = await api.olap.drilldownDept(selectedDeptId.value) }
  catch { drillData.value = null }
  finally { drillLoad.value = false }
}

// ── Init ───────────────────────────────────────────────────────────────────────
onMounted(async () => {
  const depts = await api.getAll('department', 1, 1000)
  deptOptions.value = depts.items.map(d => ({ value: d.dept_id, label: d.dept_name }))
  await Promise.all([loadDept(), loadItem(), loadQuarter()])
})

function setTab(key) {
  activeTab.value = key
}

const fmt = v =>
  v != null
    ? Number(v).toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    : '—'

function deviationClass(val) {
  const n = Number(val)
  if (n > 0) return 'text-emerald-600 font-medium'
  if (n < 0) return 'text-red-500 font-medium'
  return 'text-gray-500'
}
</script>

<template>
  <div class="p-8">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-800">OLAP-анализ</h1>
      <p class="text-sm text-gray-500 mt-1">Многомерный анализ бюджета и документов</p>
    </div>

    <!-- Tabs -->
    <div class="flex gap-1 mb-6 bg-gray-100 p-1 rounded-xl w-fit">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        @click="setTab(tab.key)"
        class="px-4 py-2 text-sm font-medium rounded-lg transition-colors"
        :class="activeTab === tab.key
          ? 'bg-white text-blue-600 shadow-sm'
          : 'text-gray-500 hover:text-gray-700'"
      >{{ tab.label }}</button>
    </div>

    <!-- ── Rollup by Dept ─────────────────────────────────────────────────────── -->
    <div v-show="activeTab === 'dept'">
      <div v-if="deptLoad" class="py-10 text-center text-gray-400 text-sm animate-pulse">Загрузка...</div>
      <div v-else class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-gray-50 border-b border-gray-100">
              <th class="px-4 py-2.5 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Отдел</th>
              <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide">Σ План, ₽</th>
              <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide">Σ Факт, ₽</th>
              <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide">Отклонение, ₽</th>
              <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide">Документов</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!deptData.length">
              <td colspan="5" class="py-8 text-center text-gray-400">Нет данных</td>
            </tr>
            <tr
              v-for="row in deptData"
              :key="row.dept_id"
              class="border-b border-gray-50 last:border-0 hover:bg-blue-50/30 transition-colors"
            >
              <td class="px-4 py-2.5 font-medium text-gray-800">{{ row.dept_name }}</td>
              <td class="px-4 py-2.5 text-right text-gray-700">{{ fmt(row.total_plan) }}</td>
              <td class="px-4 py-2.5 text-right text-gray-700">{{ fmt(row.total_fact) }}</td>
              <td class="px-4 py-2.5 text-right" :class="deviationClass(row.deviation)">{{ fmt(row.deviation) }}</td>
              <td class="px-4 py-2.5 text-right text-gray-600">{{ row.doc_count }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── Rollup by Item ─────────────────────────────────────────────────────── -->
    <div v-show="activeTab === 'item'">
      <div v-if="itemLoad" class="py-10 text-center text-gray-400 text-sm animate-pulse">Загрузка...</div>
      <div v-else class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-gray-50 border-b border-gray-100">
              <th class="px-4 py-2.5 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Статья</th>
              <th class="px-4 py-2.5 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Категория</th>
              <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide">Σ План, ₽</th>
              <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide">Σ Факт, ₽</th>
              <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide">Отклонение, ₽</th>
              <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide">Документов</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!itemData.length">
              <td colspan="6" class="py-8 text-center text-gray-400">Нет данных</td>
            </tr>
            <tr
              v-for="row in itemData"
              :key="row.item_id"
              class="border-b border-gray-50 last:border-0 hover:bg-blue-50/30 transition-colors"
            >
              <td class="px-4 py-2.5 font-medium text-gray-800">{{ row.item_name }}</td>
              <td class="px-4 py-2.5 text-gray-500 text-xs">{{ row.item_category || '—' }}</td>
              <td class="px-4 py-2.5 text-right text-gray-700">{{ fmt(row.total_plan) }}</td>
              <td class="px-4 py-2.5 text-right text-gray-700">{{ fmt(row.total_fact) }}</td>
              <td class="px-4 py-2.5 text-right" :class="deviationClass(row.deviation)">{{ fmt(row.deviation) }}</td>
              <td class="px-4 py-2.5 text-right text-gray-600">{{ row.doc_count }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── Rollup by Quarter ──────────────────────────────────────────────────── -->
    <div v-show="activeTab === 'quarter'">
      <div v-if="quarterLoad" class="py-10 text-center text-gray-400 text-sm animate-pulse">Загрузка...</div>
      <div v-else class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-gray-50 border-b border-gray-100">
              <th class="px-4 py-2.5 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Год</th>
              <th class="px-4 py-2.5 text-left text-xs font-semibold text-gray-500 uppercase tracking-wide">Квартал</th>
              <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide">Σ План, ₽</th>
              <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide">Σ Факт, ₽</th>
              <th class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase tracking-wide">Отклонение, ₽</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!quarterData.length">
              <td colspan="5" class="py-8 text-center text-gray-400">Нет данных</td>
            </tr>
            <tr
              v-for="row in quarterData"
              :key="`${row.budget_year}-${row.budget_quarter}`"
              class="border-b border-gray-50 last:border-0 hover:bg-blue-50/30 transition-colors"
            >
              <td class="px-4 py-2.5 font-medium text-gray-800">{{ row.budget_year }}</td>
              <td class="px-4 py-2.5 text-gray-600">Q{{ row.budget_quarter }}</td>
              <td class="px-4 py-2.5 text-right text-gray-700">{{ fmt(row.total_plan) }}</td>
              <td class="px-4 py-2.5 text-right text-gray-700">{{ fmt(row.total_fact) }}</td>
              <td class="px-4 py-2.5 text-right" :class="deviationClass(row.deviation)">{{ fmt(row.deviation) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── Drilldown by Dept ──────────────────────────────────────────────────── -->
    <div v-show="activeTab === 'drill'">
      <div class="flex items-center gap-3 mb-5">
        <label class="text-sm font-medium text-gray-600">Выберите отдел:</label>
        <select
          v-model="selectedDeptId"
          class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 min-w-[220px]"
        >
          <option :value="null">— выберите —</option>
          <option v-for="opt in deptOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
        </select>
        <button
          @click="loadDrilldown"
          :disabled="!selectedDeptId"
          class="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >Загрузить</button>
      </div>

      <div v-if="drillLoad" class="py-10 text-center text-gray-400 text-sm animate-pulse">Загрузка...</div>

      <div v-else-if="drillData" class="space-y-6">
        <!-- Summary -->
        <div class="grid grid-cols-4 gap-4">
          <div class="bg-blue-50 border border-blue-200 rounded-xl p-4">
            <p class="text-xs text-gray-500 mb-1">Отдел</p>
            <p class="font-semibold text-gray-800 text-sm">{{ drillData.department?.dept_name }}</p>
          </div>
          <div class="bg-emerald-50 border border-emerald-200 rounded-xl p-4">
            <p class="text-xs text-gray-500 mb-1">Σ План</p>
            <p class="font-bold text-emerald-700">{{ fmt(drillData.summary?.total_plan) }} ₽</p>
          </div>
          <div class="bg-amber-50 border border-amber-200 rounded-xl p-4">
            <p class="text-xs text-gray-500 mb-1">Σ Факт</p>
            <p class="font-bold text-amber-700">{{ fmt(drillData.summary?.total_fact) }} ₽</p>
          </div>
          <div class="bg-violet-50 border border-violet-200 rounded-xl p-4">
            <p class="text-xs text-gray-500 mb-1">Сотрудников / Документов</p>
            <p class="font-bold text-violet-700">
              {{ drillData.summary?.employee_count }} / {{ drillData.summary?.doc_count }}
            </p>
          </div>
        </div>

        <!-- Employees -->
        <div v-if="drillData.employees?.length" class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm">
          <div class="px-4 py-3 border-b border-gray-100 bg-gray-50">
            <h3 class="text-sm font-semibold text-gray-700">Сотрудники ({{ drillData.employees.length }})</h3>
          </div>
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-gray-100">
                <th class="px-4 py-2 text-left text-xs font-semibold text-gray-500 uppercase">ФИО</th>
                <th class="px-4 py-2 text-left text-xs font-semibold text-gray-500 uppercase">Должность</th>
                <th class="px-4 py-2 text-right text-xs font-semibold text-gray-500 uppercase">Зарплата, ₽</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="e in drillData.employees"
                :key="e.emp_id"
                class="border-b border-gray-50 last:border-0 hover:bg-blue-50/20"
              >
                <td class="px-4 py-2 text-gray-800">{{ e.last_name }} {{ e.first_name }}</td>
                <td class="px-4 py-2 text-gray-600 text-xs">{{ e.position_name }}</td>
                <td class="px-4 py-2 text-right text-gray-700">{{ fmt(e.salary) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Budget -->
        <div v-if="drillData.budget?.length" class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm">
          <div class="px-4 py-3 border-b border-gray-100 bg-gray-50">
            <h3 class="text-sm font-semibold text-gray-700">Бюджет ({{ drillData.budget.length }} строк)</h3>
          </div>
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-gray-100">
                <th class="px-4 py-2 text-left text-xs font-semibold text-gray-500 uppercase">Статья</th>
                <th class="px-4 py-2 text-left text-xs font-semibold text-gray-500 uppercase">Период</th>
                <th class="px-4 py-2 text-right text-xs font-semibold text-gray-500 uppercase">План, ₽</th>
                <th class="px-4 py-2 text-right text-xs font-semibold text-gray-500 uppercase">Факт, ₽</th>
                <th class="px-4 py-2 text-right text-xs font-semibold text-gray-500 uppercase">Откл., ₽</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="b in drillData.budget"
                :key="`${b.item_id}-${b.budget_year}-${b.budget_quarter}`"
                class="border-b border-gray-50 last:border-0 hover:bg-blue-50/20"
              >
                <td class="px-4 py-2 text-gray-800">{{ b.item_name }}</td>
                <td class="px-4 py-2 text-gray-500 text-xs">{{ b.budget_year }} Q{{ b.budget_quarter }}</td>
                <td class="px-4 py-2 text-right text-gray-700">{{ fmt(b.plan_rub) }}</td>
                <td class="px-4 py-2 text-right text-gray-700">{{ fmt(b.fact_rub) }}</td>
                <td class="px-4 py-2 text-right" :class="deviationClass(Number(b.plan_rub) - Number(b.fact_rub))">
                  {{ fmt(Number(b.plan_rub) - Number(b.fact_rub)) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div v-else-if="!drillLoad && !drillData && selectedDeptId" class="py-10 text-center text-gray-400 text-sm">
        Нет данных
      </div>
      <div v-else-if="!selectedDeptId" class="py-10 text-center text-gray-400 text-sm">
        Выберите отдел для детализации
      </div>
    </div>
  </div>
</template>

```

## frontend/src/views/OlapView.vue

```html
<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import { api } from '../services/api'
import OlapControls from '../components/OlapControls.vue'
import OlapTable from '../components/OlapTable.vue'
import OlapChart from '../components/OlapChart.vue'

const API_BASE = 'http://localhost:8000/api'

// ── Состояние ────────────────────────────────────────────────────────────────
const operation = ref('rollup-dept')

const departments = ref([])
const contractors = ref([])
const items = ref([])
const quarters = ref([])

const selectedDeptId = ref(null)
const selectedContrInn = ref(null)
const diceDeptId = ref(null)
const diceItemId = ref(null)
const diceQuarter = ref(null)

const loading = ref(false)
const error = ref('')
const result = ref(null)

// ── Загрузка справочников ────────────────────────────────────────────────────
async function loadDictionaries() {
  try {
    const [deps, contrs, itms, qs] = await Promise.all([
      api.getAll('department', 1, 1000),
      api.getAll('contractor', 1, 1000),
      api.getAll('budget-item', 1, 1000),
      api.olap.rollupByQuarter(),
    ])
    departments.value = deps.items || []
    contractors.value = contrs.items || []
    items.value = itms.items || []
    quarters.value = (qs || []).map(q => ({
      year: q.budget_year,
      quarter: q.budget_quarter,
    }))
  } catch (e) {
    console.error('Ошибка загрузки справочников:', e)
  }
}

// ── Применить операцию ───────────────────────────────────────────────────────
async function apply() {
  loading.value = true
  error.value = ''
  result.value = null
  try {
    switch (operation.value) {
      case 'rollup-dept':
        result.value = await api.olap.rollupByDept()
        break
      case 'rollup-item':
        result.value = await api.olap.rollupByItem()
        break
      case 'rollup-quarter':
        result.value = await api.olap.rollupByQuarter()
        break
      case 'slice-dept':
        if (!selectedDeptId.value) { error.value = 'Выберите отдел'; break }
        result.value = await api.olap.sliceByDept(selectedDeptId.value)
        break
      case 'slice-contractor':
        if (!selectedContrInn.value) { error.value = 'Выберите контрагента'; break }
        result.value = await api.olap.sliceByContractor(selectedContrInn.value)
        break
      case 'dice': {
        const params = {}
        if (diceDeptId.value != null) params.dept_id = diceDeptId.value
        if (diceItemId.value != null) params.item_id = diceItemId.value
        if (diceQuarter.value) {
          const [y, q] = diceQuarter.value.split('-')
          params.budget_year = Number(y)
          params.budget_quarter = Number(q)
        }
        result.value = await api.olap.dice(params)
        break
      }
      case 'drilldown-dept':
        if (!selectedDeptId.value) { error.value = 'Выберите отдел'; break }
        result.value = await api.olap.drilldownDept(selectedDeptId.value)
        break
      case 'cross-dept-item':
        result.value = await api.olap.crossDeptItem()
        break
    }
  } catch (e) {
    error.value = 'Ошибка загрузки данных: ' + (e?.message || 'unknown')
    console.error(e)
  } finally {
    loading.value = false
  }
}

// ── Колонки таблицы ──────────────────────────────────────────────────────────
const tableColumns = computed(() => {
  switch (operation.value) {
    case 'rollup-dept':
      return [
        { key: 'dept_name', label: 'Отдел' },
        { key: 'total_plan', label: 'Σ План, ₽', format: 'number' },
        { key: 'total_fact', label: 'Σ Факт, ₽', format: 'number' },
        { key: 'deviation', label: 'Отклонение, ₽', format: 'number', deviation: true },
        { key: 'doc_count', label: 'Документов', format: 'number' },
      ]
    case 'rollup-item':
      return [
        { key: 'item_name', label: 'Статья' },
        { key: 'item_category', label: 'Категория' },
        { key: 'total_plan', label: 'Σ План, ₽', format: 'number' },
        { key: 'total_fact', label: 'Σ Факт, ₽', format: 'number' },
        { key: 'deviation', label: 'Отклонение, ₽', format: 'number', deviation: true },
        { key: 'doc_count', label: 'Документов', format: 'number' },
      ]
    case 'rollup-quarter':
      return [
        { key: 'budget_year', label: 'Год' },
        { key: 'budget_quarter', label: 'Квартал' },
        { key: 'total_plan', label: 'Σ План, ₽', format: 'number' },
        { key: 'total_fact', label: 'Σ Факт, ₽', format: 'number' },
        { key: 'deviation', label: 'Отклонение, ₽', format: 'number', deviation: true },
      ]
    default:
      return []
  }
})

// Строки для таблицы основной операции
const tableRows = computed(() => {
  if (!result.value) return []
  if (['rollup-dept', 'rollup-item', 'rollup-quarter'].includes(operation.value)) {
    return result.value
  }
  return []
})

// ── Данные для графика ───────────────────────────────────────────────────────
const chartInfo = computed(() => {
  if (!result.value) return null

  if (operation.value === 'rollup-dept') {
    const data = result.value
    return {
      type: 'bar',
      title: 'План vs Факт по отделам',
      data: {
        labels: data.map(r => r.dept_name),
        datasets: [
          {
            label: 'План',
            data: data.map(r => Number(r.total_plan)),
            backgroundColor: 'rgba(59, 130, 246, 0.7)',
          },
          {
            label: 'Факт',
            data: data.map(r => Number(r.total_fact)),
            backgroundColor: 'rgba(16, 185, 129, 0.7)',
          },
        ],
      },
    }
  }

  if (operation.value === 'rollup-item') {
    const data = result.value
    const palette = [
      '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
      '#ec4899', '#14b8a6', '#f97316', '#6366f1', '#84cc16',
    ]
    return {
      type: 'pie',
      title: 'Доли расходов по статьям (факт)',
      data: {
        labels: data.map(r => r.item_name),
        datasets: [{
          data: data.map(r => Number(r.total_fact)),
          backgroundColor: data.map((_, i) => palette[i % palette.length]),
        }],
      },
    }
  }

  if (operation.value === 'rollup-quarter') {
    const data = result.value
    return {
      type: 'line',
      title: 'Динамика бюджета по кварталам',
      data: {
        labels: data.map(r => `${r.budget_year} Q${r.budget_quarter}`),
        datasets: [
          {
            label: 'План',
            data: data.map(r => Number(r.total_plan)),
            borderColor: '#3b82f6',
            backgroundColor: 'rgba(59, 130, 246, 0.15)',
            tension: 0.3,
            fill: true,
          },
          {
            label: 'Факт',
            data: data.map(r => Number(r.total_fact)),
            borderColor: '#10b981',
            backgroundColor: 'rgba(16, 185, 129, 0.15)',
            tension: 0.3,
            fill: true,
          },
        ],
      },
    }
  }

  if (operation.value === 'cross-dept-item') {
    const pivot = result.value
    const itemsSet = new Set()
    pivot.forEach(d => Object.keys(d.items || {}).forEach(n => itemsSet.add(n)))
    const itemNames = Array.from(itemsSet)
    const palette = [
      '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
      '#ec4899', '#14b8a6', '#f97316', '#6366f1', '#84cc16',
    ]
    const datasets = itemNames.map((name, i) => ({
      label: name,
      data: pivot.map(d => Number(d.items?.[name]?.total_fact || 0)),
      backgroundColor: palette[i % palette.length],
    }))
    return {
      type: 'stacked-bar',
      title: 'Кросс-таблица Отдел × Статья (факт)',
      data: {
        labels: pivot.map(d => d.dept_name),
        datasets,
      },
    }
  }

  return null
})

// ── Кросс-таблица ────────────────────────────────────────────────────────────
const crossItemNames = computed(() => {
  if (operation.value !== 'cross-dept-item' || !result.value) return []
  const set = new Set()
  result.value.forEach(d => Object.keys(d.items || {}).forEach(n => set.add(n)))
  return Array.from(set)
})

function crossCell(dept, itemName) {
  const cell = dept.items?.[itemName]
  if (!cell) return '—'
  return Number(cell.total_fact).toLocaleString('ru-RU', {
    minimumFractionDigits: 0, maximumFractionDigits: 0,
  })
}

// ── Форматирование ───────────────────────────────────────────────────────────
const fmt = v =>
  v != null
    ? Number(v).toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    : '—'

function deviationClass(val) {
  const n = Number(val)
  if (n > 0) return 'text-emerald-600 font-medium'
  if (n < 0) return 'text-red-500 font-medium'
  return 'text-gray-500'
}

// ── Экспорт ──────────────────────────────────────────────────────────────────
const exportMap = {
  'rollup-dept': 'rollup-by-dept',
  'rollup-item': 'rollup-by-item',
  'rollup-quarter': 'rollup-by-quarter',
  'cross-dept-item': 'cross-dept-item',
  'slice-dept': 'slice-by-dept',
  'slice-contractor': 'slice-by-contractor',
}

const canExport = computed(() => !!exportMap[operation.value])

async function exportFile(format) {
  const reportType = exportMap[operation.value]
  if (!reportType) return

  const params = { format }
  if (operation.value === 'slice-dept') {
    if (!selectedDeptId.value) { error.value = 'Выберите отдел'; return }
    params.dept_id = selectedDeptId.value
  }
  if (operation.value === 'slice-contractor') {
    if (!selectedContrInn.value) { error.value = 'Выберите контрагента'; return }
    params.contr_inn = selectedContrInn.value
  }

  try {
    const resp = await axios.get(`${API_BASE}/export/${reportType}`, {
      params,
      responseType: 'blob',
    })
    const blob = new Blob([resp.data], {
      type: format === 'csv'
        ? 'text/csv;charset=utf-8'
        : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${reportType}.${format}`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  } catch (e) {
    error.value = 'Не удалось скачать файл'
    console.error(e)
  }
}

// ── Init ─────────────────────────────────────────────────────────────────────
// Операции, не требующие фильтров — применяем сразу при переключении вкладки
const AUTO_APPLY_OPS = new Set(['rollup-dept', 'rollup-item', 'rollup-quarter', 'cross-dept-item'])

onMounted(async () => {
  await loadDictionaries()
  await apply()
})

watch(operation, () => {
  // Сбрасываем предыдущий результат чтобы не показывать чужие данные
  result.value = null
  error.value = ''
  if (AUTO_APPLY_OPS.has(operation.value)) {
    apply()
  }
})
</script>

<template>
  <div class="p-8">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-800">OLAP-анализ</h1>
      <p class="text-sm text-gray-500 mt-1">Многомерный анализ бюджета и документов</p>
    </div>

    <!-- Панель управления -->
    <OlapControls
      v-model:operation="operation"
      :departments="departments"
      :contractors="contractors"
      :items="items"
      :quarters="quarters"
      v-model:selectedDeptId="selectedDeptId"
      v-model:selectedContrInn="selectedContrInn"
      v-model:diceDeptId="diceDeptId"
      v-model:diceItemId="diceItemId"
      v-model:diceQuarter="diceQuarter"
      @apply="apply"
    />

    <!-- Кнопки экспорта -->
    <div v-if="canExport" class="flex gap-2 mb-4">
      <button
        @click="exportFile('csv')"
        class="px-4 py-2 bg-white border border-gray-300 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 transition-colors"
      >Скачать CSV</button>
      <button
        @click="exportFile('xlsx')"
        class="px-4 py-2 bg-white border border-gray-300 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 transition-colors"
      >Скачать Excel</button>
    </div>

    <!-- Ошибка -->
    <div v-if="error" class="mb-4 px-4 py-3 bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg">
      {{ error }}
    </div>

    <!-- Загрузка -->
    <div v-if="loading" class="py-10 text-center text-gray-400 text-sm animate-pulse">
      Загрузка...
    </div>

    <!-- Результат -->
    <div v-else-if="result" class="space-y-6">
      <!-- График (для Roll-up и кросс-таблицы) -->
      <OlapChart
        v-if="chartInfo"
        :type="chartInfo.type"
        :data="chartInfo.data"
        :title="chartInfo.title"
      />

      <!-- Таблица для Roll-up операций -->
      <OlapTable
        v-if="tableColumns.length"
        :columns="tableColumns"
        :rows="tableRows"
      />

      <!-- Срез по отделу -->
      <template v-if="operation === 'slice-dept' && result.department">
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-4">
          <p class="text-xs text-gray-500 mb-1">Отдел</p>
          <p class="font-semibold text-gray-800">{{ result.department.dept_name }}</p>
        </div>
        <OlapTable
          title="Бюджет"
          :columns="[
            { key: 'item_name', label: 'Статья' },
            { key: 'budget_year', label: 'Год' },
            { key: 'budget_quarter', label: 'Квартал' },
            { key: 'plan_rub', label: 'План, ₽', format: 'number' },
            { key: 'fact_rub', label: 'Факт, ₽', format: 'number' },
          ]"
          :rows="result.budget"
        />
        <OlapTable
          title="Документы"
          :columns="[
            { key: 'doc_id', label: 'ID' },
            { key: 'doc_date', label: 'Дата', format: 'date' },
            { key: 'type_name', label: 'Тип' },
            { key: 'item_name', label: 'Статья' },
            { key: 'doc_amount', label: 'Сумма, ₽', format: 'number' },
            { key: 'contr_name', label: 'Контрагент' },
            { key: 'resp_emp_name', label: 'Ответственный' },
          ]"
          :rows="result.documents"
        />
      </template>

      <!-- Срез по контрагенту -->
      <template v-if="operation === 'slice-contractor' && result.contractor">
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-4">
          <p class="text-xs text-gray-500 mb-1">Контрагент</p>
          <p class="font-semibold text-gray-800">{{ result.contractor.contr_name }}</p>
          <p class="text-xs text-gray-500 mt-1">ИНН: {{ result.contractor.contr_inn }}</p>
        </div>
        <OlapTable
          title="Документы"
          :columns="[
            { key: 'doc_id', label: 'ID' },
            { key: 'doc_date', label: 'Дата', format: 'date' },
            { key: 'type_name', label: 'Тип' },
            { key: 'dept_name', label: 'Отдел' },
            { key: 'item_name', label: 'Статья' },
            { key: 'doc_amount', label: 'Сумма, ₽', format: 'number' },
            { key: 'resp_emp_name', label: 'Ответственный' },
          ]"
          :rows="result.documents"
        />
      </template>

      <!-- Dice -->
      <template v-if="operation === 'dice'">
        <OlapTable
          title="Бюджет (по фильтрам)"
          :columns="[
            { key: 'dept_name', label: 'Отдел' },
            { key: 'item_name', label: 'Статья' },
            { key: 'budget_year', label: 'Год' },
            { key: 'budget_quarter', label: 'Квартал' },
            { key: 'plan_rub', label: 'План, ₽', format: 'number' },
            { key: 'fact_rub', label: 'Факт, ₽', format: 'number' },
          ]"
          :rows="result.budget || []"
        />
        <OlapTable
          title="Документы (по фильтрам)"
          :columns="[
            { key: 'doc_id', label: 'ID' },
            { key: 'doc_date', label: 'Дата', format: 'date' },
            { key: 'dept_name', label: 'Отдел' },
            { key: 'item_name', label: 'Статья' },
            { key: 'type_name', label: 'Тип' },
            { key: 'doc_amount', label: 'Сумма, ₽', format: 'number' },
            { key: 'contr_name', label: 'Контрагент' },
          ]"
          :rows="result.documents || []"
        />
      </template>

      <!-- Drill-down по отделу -->
      <template v-if="operation === 'drilldown-dept' && result.department">
        <div class="grid grid-cols-4 gap-4">
          <div class="bg-blue-50 border border-blue-200 rounded-xl p-4">
            <p class="text-xs text-gray-500 mb-1">Отдел</p>
            <p class="font-semibold text-gray-800 text-sm">{{ result.department.dept_name }}</p>
          </div>
          <div class="bg-emerald-50 border border-emerald-200 rounded-xl p-4">
            <p class="text-xs text-gray-500 mb-1">Σ План</p>
            <p class="font-bold text-emerald-700">{{ fmt(result.summary?.total_plan) }} ₽</p>
          </div>
          <div class="bg-amber-50 border border-amber-200 rounded-xl p-4">
            <p class="text-xs text-gray-500 mb-1">Σ Факт</p>
            <p class="font-bold text-amber-700">{{ fmt(result.summary?.total_fact) }} ₽</p>
          </div>
          <div class="bg-violet-50 border border-violet-200 rounded-xl p-4">
            <p class="text-xs text-gray-500 mb-1">Сотрудников / Документов</p>
            <p class="font-bold text-violet-700">
              {{ result.summary?.employee_count }} / {{ result.summary?.doc_count }}
            </p>
          </div>
        </div>

        <OlapTable
          v-if="result.employees?.length"
          :title="`Сотрудники (${result.employees.length})`"
          :columns="[
            { key: 'last_name', label: 'Фамилия' },
            { key: 'first_name', label: 'Имя' },
            { key: 'position_name', label: 'Должность' },
            { key: 'salary', label: 'Зарплата, ₽', format: 'number' },
          ]"
          :rows="result.employees"
        />
        <OlapTable
          v-if="result.budget?.length"
          :title="`Бюджет (${result.budget.length})`"
          :columns="[
            { key: 'item_name', label: 'Статья' },
            { key: 'budget_year', label: 'Год' },
            { key: 'budget_quarter', label: 'Квартал' },
            { key: 'plan_rub', label: 'План, ₽', format: 'number' },
            { key: 'fact_rub', label: 'Факт, ₽', format: 'number' },
          ]"
          :rows="result.budget"
        />
        <OlapTable
          v-if="result.documents?.length"
          :title="`Документы (${result.documents.length})`"
          :columns="[
            { key: 'doc_id', label: 'ID' },
            { key: 'doc_date', label: 'Дата', format: 'date' },
            { key: 'type_name', label: 'Тип' },
            { key: 'item_name', label: 'Статья' },
            { key: 'doc_amount', label: 'Сумма, ₽', format: 'number' },
            { key: 'contr_name', label: 'Контрагент' },
            { key: 'resp_emp_name', label: 'Ответственный' },
          ]"
          :rows="result.documents"
        />
      </template>

      <!-- Кросс-таблица -->
      <template v-if="operation === 'cross-dept-item'">
        <div class="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm">
          <div class="px-4 py-3 border-b border-gray-100 bg-gray-50">
            <h3 class="text-sm font-semibold text-gray-700">Отдел × Статья (факт, ₽)</h3>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="bg-gray-50 border-b border-gray-100">
                  <th class="px-4 py-2.5 text-left text-xs font-semibold text-gray-500 uppercase sticky left-0 bg-gray-50">Отдел</th>
                  <th
                    v-for="name in crossItemNames"
                    :key="name"
                    class="px-4 py-2.5 text-right text-xs font-semibold text-gray-500 uppercase whitespace-nowrap"
                  >{{ name }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="!result.length">
                  <td :colspan="crossItemNames.length + 1" class="py-8 text-center text-gray-400">
                    Нет данных
                  </td>
                </tr>
                <tr
                  v-for="dept in result"
                  :key="dept.dept_id"
                  class="border-b border-gray-50 last:border-0 hover:bg-blue-50/30 transition-colors"
                >
                  <td class="px-4 py-2.5 font-medium text-gray-800 sticky left-0 bg-white">
                    {{ dept.dept_name }}
                  </td>
                  <td
                    v-for="name in crossItemNames"
                    :key="name"
                    class="px-4 py-2.5 text-right text-gray-700"
                  >{{ crossCell(dept, name) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </template>
    </div>

    <div v-else class="py-10 text-center text-gray-400 text-sm">
      Выберите операцию и нажмите «Применить»
    </div>
  </div>
</template>

```

## frontend/src/views/Positions.vue

```html
<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../services/api'
import DataTable from '../components/DataTable.vue'
import FormModal from '../components/FormModal.vue'

const columns = [
  { key: 'position_id',    label: 'ID' },
  { key: 'position_name',  label: 'Наименование' },
  { key: 'position_grade', label: 'Грейд' },
  { key: 'min_salary', label: 'Мин. зарплата, ₽',
    render: r => r.min_salary != null ? Number(r.min_salary).toLocaleString('ru-RU') : '—' },
]

const formFields = computed(() => [
  { key: 'position_id',    label: 'ID',             type: 'number', required: true, createOnly: true },
  { key: 'position_name',  label: 'Наименование',   type: 'text',   required: true },
  { key: 'position_grade', label: 'Грейд',          type: 'text' },
  { key: 'min_salary',     label: 'Мин. зарплата',  type: 'number', required: true },
])

const rows     = ref([])
const total    = ref(0)
const page     = ref(1)
const pageSize = 20
const loading  = ref(false)
const error    = ref('')

const showModal  = ref(false)
const isEdit     = ref(false)
const formData   = ref({})
const currentRow = ref(null)
const saveError  = ref('')

async function loadPage(p) {
  loading.value = true
  error.value   = ''
  try {
    const data = await api.getAll('position', p, pageSize)
    rows.value  = data.items
    total.value = data.total
    page.value  = p
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка загрузки'
  } finally {
    loading.value = false
  }
}

onMounted(() => loadPage(1))

function openAdd() {
  isEdit.value    = false
  formData.value  = {}
  saveError.value = ''
  showModal.value = true
}

function openEdit(row) {
  isEdit.value    = true
  currentRow.value = row
  formData.value  = { ...row }
  saveError.value = ''
  showModal.value = true
}

async function handleDelete(row) {
  if (!confirm(`Удалить должность «${row.position_name}»?`)) return
  try {
    await api.delete('position', row.position_id)
    await loadPage(page.value)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка удаления'
  }
}

function pickFields(raw, edit) {
  const keys = formFields.value
    .filter(f => !(f.createOnly && edit))
    .map(f => f.key)
  return Object.fromEntries(keys.map(k => [k, raw[k] === '' ? null : raw[k]]))
}

async function handleSubmit(raw) {
  saveError.value = ''
  try {
    const data = pickFields(raw, isEdit.value)
    if (isEdit.value) {
      await api.update('position', currentRow.value.position_id, data)
    } else {
      await api.create('position', data)
    }
    showModal.value = false
    await loadPage(page.value)
  } catch (e) {
    saveError.value = e.response?.data?.detail || 'Ошибка сохранения'
  }
}
</script>

<template>
  <div class="p-8">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Должности</h1>
      <p class="text-sm text-gray-500 mt-1">Справочник должностей и грейдов</p>
    </div>
    <div v-if="error" class="mb-4 px-4 py-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
      {{ error }}
    </div>
    <DataTable
      :columns="columns" :rows="rows" :total="total"
      :page="page" :page-size="pageSize" :loading="loading"
      @update:page="loadPage" @add="openAdd" @edit="openEdit" @delete="handleDelete"
    />
    <FormModal
      v-if="showModal"
      :title="isEdit ? 'Редактировать должность' : 'Добавить должность'"
      :fields="formFields" :model-value="formData"
      :is-edit="isEdit" :error="saveError"
      @submit="handleSubmit" @close="showModal = false"
    />
  </div>
</template>

```

## frontend/tailwind.config.js

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

```

## frontend/vite.config.js

```js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
})

```

## generate_report.py

```py
"""Генерация отчёта по лабораторной работе в формате .docx."""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


OUT_PATH = r"C:\Users\sbogo\Databases_App\Отчёт_по_лабораторной.docx"


def set_default_font(doc: Document):
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(14)
    rpr = style.element.get_or_add_rPr()
    rFonts = rpr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rpr.append(rFonts)
    rFonts.set(qn("w:ascii"), "Times New Roman")
    rFonts.set(qn("w:hAnsi"), "Times New Roman")
    rFonts.set(qn("w:cs"), "Times New Roman")
    rFonts.set(qn("w:eastAsia"), "Times New Roman")


def add_heading(doc: Document, text: str, level: int = 1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.name = "Times New Roman"
        run.font.color.rgb = RGBColor(0, 0, 0)
        if level == 1:
            run.font.size = Pt(16)
        elif level == 2:
            run.font.size = Pt(14)
        else:
            run.font.size = Pt(13)
    return h


def add_para(doc: Document, text: str, bold: bool = False, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.first_line_indent = Cm(1.25)
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)
    run.bold = bold
    return p


def add_bullet(doc: Document, text: str):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)


def add_screenshot_note(doc: Document, caption: str, what_to_capture: str):
    """Пометка для вставки скриншота."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(f"[ МЕСТО ДЛЯ СКРИНШОТА: {caption} ]")
    run.bold = True
    run.italic = True
    run.font.size = Pt(13)
    run.font.name = "Times New Roman"
    run.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.line_spacing = 1.5
    run2 = p2.add_run(f"Что снять: {what_to_capture}")
    run2.italic = True
    run2.font.size = Pt(12)
    run2.font.name = "Times New Roman"
    run2.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    # подпись рисунка
    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p3.paragraph_format.line_spacing = 1.5
    run3 = p3.add_run(f"Рисунок — {caption}")
    run3.italic = True
    run3.font.size = Pt(13)
    run3.font.name = "Times New Roman"


def add_table(doc: Document, headers: list[str], rows: list[list[str]]):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER

    hdr_cells = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = ""
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)

    for ridx, row in enumerate(rows, start=1):
        for cidx, val in enumerate(row):
            cell = t.rows[ridx].cells[cidx]
            cell.text = ""
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(str(val))
            r.font.name = "Times New Roman"
            r.font.size = Pt(12)
    return t


def build():
    doc = Document()
    set_default_font(doc)

    for section in doc.sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(3)
        section.right_margin = Cm(1.5)

    # ── Цель работы ──────────────────────────────────────────────────────────
    add_heading(doc, "1. Цель работы", level=1)
    add_para(
        doc,
        "Цель лабораторной работы — спроектировать и реализовать клиент-серверное "
        "приложение для работы с реляционной базой данных, поддерживающее базовые "
        "CRUD-операции над всеми сущностями предметной области, а также "
        "многомерный (OLAP) анализ данных с возможностью построения аналитических "
        "отчётов, визуализации результатов и экспорта выборок во внешние форматы.",
    )

    # ── Постановка задачи ────────────────────────────────────────────────────
    add_heading(doc, "2. Постановка задачи", level=1)
    add_para(doc, "В рамках работы необходимо решить следующие задачи:")
    add_bullet(doc, "Разработать схему реляционной базы данных, отражающую выбранную предметную область (документооборот и бюджетирование организации).")
    add_bullet(doc, "Реализовать серверную часть, предоставляющую REST API для работы с данными.")
    add_bullet(doc, "Реализовать клиентскую часть — одностраничное веб-приложение с удобным интерфейсом для конечного пользователя.")
    add_bullet(doc, "Обеспечить полный набор CRUD-операций (создание, чтение, изменение, удаление) для всех основных сущностей.")
    add_bullet(doc, "Реализовать OLAP-операции: roll-up, slice, dice, drill-down, cross-tabulation.")
    add_bullet(doc, "Добавить визуализацию аналитических данных (диаграммы).")
    add_bullet(doc, "Предусмотреть возможность экспорта отчётов во внешние форматы (CSV, XLSX).")

    # ── Предметная область ───────────────────────────────────────────────────
    add_heading(doc, "3. Описание предметной области", level=1)
    add_para(
        doc,
        "Предметная область — автоматизация учёта документооборота и бюджетирования "
        "в организации. Система позволяет вести учёт сотрудников и отделов, фиксировать "
        "бюджетные планы и фактические расходы в разрезе статей и кварталов, регистрировать "
        "документы, связанные с контрагентами, а также формировать аналитические отчёты "
        "для принятия управленческих решений.",
    )
    add_para(doc, "В базе данных выделены следующие основные сущности:")
    add_bullet(doc, "«Должность» (position) — справочник должностей с указанием грейда и минимального оклада.")
    add_bullet(doc, "«Отдел» (department) — структурное подразделение организации с указанием руководителя.")
    add_bullet(doc, "«Сотрудник» (employee) — работники организации, привязанные к отделу и должности.")
    add_bullet(doc, "«Статья бюджета» (budget_item) — справочник статей расходов с категорией.")
    add_bullet(doc, "«Тип документа» (doc_type) — справочник типов документов, срок хранения и признак обязательного согласования.")
    add_bullet(doc, "«Контрагент» (contractor) — внешние организации-партнёры, идентифицируемые по ИНН.")
    add_bullet(doc, "«Бюджет» (budget) — плановые и фактические суммы по отделу, статье, году и кварталу.")
    add_bullet(doc, "«Документ» (document) — первичные документы с привязкой к отделу, статье, типу, контрагенту и ответственному сотруднику.")

    # ── Схема БД ─────────────────────────────────────────────────────────────
    add_heading(doc, "4. Схема базы данных", level=1)
    add_para(
        doc,
        "База данных реализована в СУБД PostgreSQL и включает 8 таблиц, связанных "
        "отношениями «один-ко-многим» через внешние ключи. Таблица department "
        "содержит внешний ключ на employee (руководитель отдела), что формирует "
        "циклическую зависимость, разрешаемую порядком вставки данных.",
    )
    add_screenshot_note(
        doc,
        caption="ER-диаграмма базы данных",
        what_to_capture="Откройте pgAdmin → ПКМ по БД Laba3 → «ERD for database» (или вкладка ERD Tool) и сделайте скриншот диаграммы со всеми таблицами и связями. Альтернативно — постройте диаграмму в dbdiagram.io.",
    )
    add_para(doc, "Соответствие сущностей и таблиц базы данных приведено в таблице 1.")

    add_table(
        doc,
        headers=["Таблица", "Назначение", "Ключевые поля"],
        rows=[
            ["position", "Справочник должностей", "position_id (PK)"],
            ["doc_type", "Справочник типов документов", "type_id (PK)"],
            ["budget_item", "Справочник статей бюджета", "item_id (PK)"],
            ["contractor", "Справочник контрагентов", "contr_inn (PK)"],
            ["department", "Отделы организации", "dept_id (PK), head_emp_id (FK)"],
            ["employee", "Сотрудники", "emp_id (PK), dept_id (FK), position_id (FK)"],
            ["budget", "План и факт по бюджету", "(dept_id, item_id, budget_year, budget_quarter) (PK)"],
            ["document", "Первичные документы", "doc_id (PK), dept_id, item_id, type_id, contr_inn, resp_emp_id (FK)"],
        ],
    )

    add_screenshot_note(
        doc,
        caption="Структура таблиц в pgAdmin",
        what_to_capture="Раскройте в pgAdmin дерево БД Laba3 → Schemas → public → Tables и сделайте скриншот, где видны все 8 таблиц. Дополнительно можно снять структуру одной-двух ключевых таблиц (employee, budget) с их столбцами.",
    )

    # ── Используемые технологии ─────────────────────────────────────────────
    add_heading(doc, "5. Используемые технологии", level=1)
    add_para(doc, "При реализации приложения использованы следующие технологии:")
    add_bullet(doc, "СУБД: PostgreSQL 16 — хранение данных, поддержка транзакций и сложных аналитических запросов.")
    add_bullet(doc, "Язык серверной части: Python 3.12.")
    add_bullet(doc, "Фреймворк REST API: FastAPI — декларативное описание маршрутов, автоматическая OpenAPI-документация.")
    add_bullet(doc, "Драйвер БД: asyncpg — асинхронный доступ к PostgreSQL с пулом соединений.")
    add_bullet(doc, "Валидация данных: Pydantic v2 — модели запросов/ответов.")
    add_bullet(doc, "Язык клиентской части: JavaScript.")
    add_bullet(doc, "Фреймворк SPA: Vue 3 с Composition API.")
    add_bullet(doc, "Маршрутизация: Vue Router.")
    add_bullet(doc, "Стилизация: Tailwind CSS.")
    add_bullet(doc, "Сборщик: Vite.")
    add_bullet(doc, "Экспорт XLSX: библиотека openpyxl.")

    # ── Архитектура ─────────────────────────────────────────────────────────
    add_heading(doc, "6. Архитектура приложения", level=1)
    add_para(
        doc,
        "Приложение построено по трёхзвенной архитектуре «клиент — сервер — база "
        "данных». Клиент и сервер взаимодействуют по HTTP через REST API, "
        "обмениваясь данными в формате JSON. Сервер соединяется с PostgreSQL через "
        "пул асинхронных соединений asyncpg. Такая схема обеспечивает разделение "
        "представления, бизнес-логики и хранения данных.",
    )
    add_screenshot_note(
        doc,
        caption="Схема архитектуры приложения",
        what_to_capture="Нарисуйте блок-схему из трёх блоков: «Браузер (Vue SPA)» → «FastAPI-сервер» → «PostgreSQL». Можно сделать в draw.io, Miro или PowerPoint и вставить сюда.",
    )
    add_para(
        doc,
        "Серверная часть разделена на модули-роутеры по каждой сущности "
        "(position, department, employee, budget, document, contractor, "
        "doc_type, budget_item), а также отдельные модули olap (аналитические "
        "запросы) и export (выгрузка отчётов в CSV/XLSX).",
    )
    add_para(
        doc,
        "Клиентская часть состоит из страниц-представлений для каждой сущности "
        "(Departments, Employees, Documents, Budget, Contractors, Positions), "
        "дашборда и страницы OLAP-анализа. Общие компоненты вынесены: "
        "DataTable (универсальная таблица), FormModal (модальная форма), "
        "Sidebar (боковое меню), OlapChart, OlapTable, OlapControls.",
    )

    # ── Запуск приложения ───────────────────────────────────────────────────
    add_heading(doc, "7. Запуск приложения", level=1)
    add_para(doc, "Серверная часть запускается командой uvicorn main:app --reload из каталога backend, клиентская — npm run dev из каталога frontend. Сервер поднимается на порту 8000, клиент — на 5173.")
    add_screenshot_note(
        doc,
        caption="Запуск backend-сервера",
        what_to_capture="Терминал с запущенным uvicorn, где видны строки «Application startup complete» и «Uvicorn running on http://127.0.0.1:8000».",
    )
    add_screenshot_note(
        doc,
        caption="Запуск frontend-сервера",
        what_to_capture="Терминал с запущенным Vite, где видны строки «VITE v… ready in …» и адрес http://localhost:5173.",
    )
    add_screenshot_note(
        doc,
        caption="Swagger UI — автоматическая документация API",
        what_to_capture="Откройте в браузере http://127.0.0.1:8000/docs и сделайте скриншот списка эндпоинтов (видны разделы position, department, employee, budget, document, olap, export и т. д.).",
    )

    # ── Интерфейс и CRUD ─────────────────────────────────────────────────────
    add_heading(doc, "8. Пользовательский интерфейс и CRUD-операции", level=1)

    add_heading(doc, "8.1. Главная страница (Dashboard)", level=2)
    add_para(
        doc,
        "Главная страница содержит сводную информацию по организации: количество "
        "сотрудников, отделов, документов, контрагентов, а также ссылки на "
        "основные разделы приложения.",
    )
    add_screenshot_note(
        doc,
        caption="Главная страница приложения",
        what_to_capture="Откройте http://localhost:5173/ и сделайте скриншот дашборда с плитками счётчиков и боковым меню.",
    )

    add_heading(doc, "8.2. Раздел «Отделы»", level=2)
    add_para(
        doc,
        "Раздел «Отделы» предоставляет полный набор CRUD-операций: просмотр списка "
        "отделов с пагинацией, добавление нового отдела, редактирование и удаление "
        "существующих. Для каждого отдела отображается название, количество "
        "сотрудников, этаж, телефон и руководитель.",
    )
    add_screenshot_note(
        doc,
        caption="Список отделов",
        what_to_capture="Перейдите в раздел «Отделы», сделайте скриншот таблицы со всеми столбцами и кнопками управления (Добавить / Редактировать / Удалить).",
    )
    add_screenshot_note(
        doc,
        caption="Форма добавления/редактирования отдела",
        what_to_capture="Нажмите «Добавить» или «Редактировать» у любого отдела и сделайте скриншот модальной формы со всеми полями.",
    )

    add_heading(doc, "8.3. Раздел «Сотрудники»", level=2)
    add_para(
        doc,
        "Раздел «Сотрудники» позволяет вести учёт работников с указанием ФИО, "
        "отдела, должности, оклада, даты приёма, контактных данных. Реализованы "
        "поиск и сортировка по столбцам.",
    )
    add_screenshot_note(
        doc,
        caption="Список сотрудников",
        what_to_capture="Скриншот страницы «Сотрудники» с таблицей (желательно с применённым поиском или сортировкой).",
    )
    add_screenshot_note(
        doc,
        caption="Форма добавления сотрудника",
        what_to_capture="Скриншот модальной формы создания сотрудника со всеми полями (ФИО, отдел, должность, оклад и т. д.).",
    )

    add_heading(doc, "8.4. Раздел «Должности»", level=2)
    add_screenshot_note(
        doc,
        caption="Справочник должностей",
        what_to_capture="Скриншот страницы «Должности» с таблицей должностей (ID, название, грейд, минимальный оклад).",
    )

    add_heading(doc, "8.5. Раздел «Контрагенты»", level=2)
    add_screenshot_note(
        doc,
        caption="Справочник контрагентов",
        what_to_capture="Скриншот страницы «Контрагенты» с ИНН, наименованиями, адресами и телефонами.",
    )

    add_heading(doc, "8.6. Раздел «Бюджет»", level=2)
    add_para(
        doc,
        "Раздел «Бюджет» отражает плановые и фактические суммы расходов по "
        "отделам и статьям в разрезе года и квартала. Для каждой записи "
        "вычисляется отклонение «План − Факт».",
    )
    add_screenshot_note(
        doc,
        caption="Таблица бюджета",
        what_to_capture="Скриншот страницы «Бюджет» с таблицей план/факт по отделам и статьям.",
    )

    add_heading(doc, "8.7. Раздел «Документы»", level=2)
    add_para(
        doc,
        "Раздел «Документы» содержит первичные документы со связями: отдел, "
        "статья бюджета, тип документа, контрагент, ответственный сотрудник. "
        "Поддерживается создание нового документа, редактирование и удаление.",
    )
    add_screenshot_note(
        doc,
        caption="Список документов",
        what_to_capture="Скриншот страницы «Документы» с таблицей и применёнными фильтрами/сортировкой.",
    )
    add_screenshot_note(
        doc,
        caption="Удаление документа — окно подтверждения",
        what_to_capture="Нажмите «Удалить» у любой записи и сделайте скриншот окна подтверждения удаления.",
    )

    # ── OLAP ────────────────────────────────────────────────────────────────
    add_heading(doc, "9. OLAP-анализ данных", level=1)
    add_para(
        doc,
        "На странице «OLAP» реализованы основные операции многомерного анализа "
        "данных над бюджетом и документами. Измерения: отдел, статья бюджета, "
        "контрагент, год, квартал. Меры: плановая сумма, фактическая сумма, "
        "отклонение и количество документов.",
    )

    add_heading(doc, "9.1. Roll-up (агрегация)", level=2)
    add_para(
        doc,
        "Операция roll-up выполняет агрегацию мер по выбранному измерению. "
        "Реализованы три варианта: по отделам, по статьям бюджета, по "
        "кварталам. Запрос строится с помощью GROUP BY и агрегирующих "
        "функций SUM и COUNT.",
    )
    add_screenshot_note(
        doc,
        caption="Roll-up по отделам",
        what_to_capture="Раздел OLAP → вкладка «Roll-up по отделам». Скриншот таблицы (отдел, план, факт, отклонение, количество документов).",
    )
    add_screenshot_note(
        doc,
        caption="Roll-up по статьям бюджета",
        what_to_capture="Раздел OLAP → вкладка «Roll-up по статьям». Скриншот таблицы со статьями и их суммами.",
    )
    add_screenshot_note(
        doc,
        caption="Roll-up по кварталам",
        what_to_capture="Раздел OLAP → вкладка «Roll-up по кварталам». Скриншот с разбивкой по годам и кварталам.",
    )

    add_heading(doc, "9.2. Slice (срез)", level=2)
    add_para(
        doc,
        "Операция slice фиксирует одно измерение, возвращая срез "
        "многомерного куба. Реализованы срезы по конкретному отделу и по "
        "конкретному контрагенту: для выбранного значения выводятся все "
        "связанные бюджетные записи и документы.",
    )
    add_screenshot_note(
        doc,
        caption="Slice по отделу",
        what_to_capture="В разделе OLAP выберите «Срез по отделу», укажите конкретный отдел и сделайте скриншот результата (карточка отдела, его бюджет и документы).",
    )
    add_screenshot_note(
        doc,
        caption="Slice по контрагенту",
        what_to_capture="В разделе OLAP выберите «Срез по контрагенту», укажите конкретного контрагента и сделайте скриншот результата.",
    )

    add_heading(doc, "9.3. Dice (фильтрация по нескольким измерениям)", level=2)
    add_para(
        doc,
        "Операция dice позволяет задать фильтр сразу по нескольким измерениям "
        "(отдел, статья, год, квартал, контрагент). В SQL это реализовано "
        "через динамическое формирование WHERE-условия с параметрами.",
    )
    add_screenshot_note(
        doc,
        caption="Dice — применение нескольких фильтров",
        what_to_capture="В разделе OLAP → «Dice» задайте одновременно несколько фильтров (например, отдел + год + квартал) и сделайте скриншот окна с выбранными фильтрами и результирующей таблицей.",
    )

    add_heading(doc, "9.4. Drill-down (детализация)", level=2)
    add_para(
        doc,
        "Операция drill-down предоставляет детализированную информацию по "
        "выбранному отделу: сводная статистика, список сотрудников отдела, "
        "бюджет и документы. Переход от агрегата к деталям выполняется в один клик.",
    )
    add_screenshot_note(
        doc,
        caption="Drill-down по отделу",
        what_to_capture="В OLAP-разделе откройте детализацию по отделу. Скриншот должен включать сводную панель (total_plan, total_fact, deviation, количество сотрудников/документов) и таблицы сотрудников и документов.",
    )

    add_heading(doc, "9.5. Cross-tab (кросс-таблица «Отдел × Статья»)", level=2)
    add_para(
        doc,
        "Кросс-таблица отображает суммарные плановые и фактические значения "
        "в разрезе двух измерений одновременно — отдел и статья бюджета. "
        "Позволяет быстро выявить, на какие статьи и в каких отделах "
        "приходится основная доля расходов.",
    )
    add_screenshot_note(
        doc,
        caption="Кросс-таблица «Отдел × Статья»",
        what_to_capture="В разделе OLAP → «Cross-tab» сделайте скриншот сводной таблицы «Отдел × Статья» со значениями плана и факта.",
    )

    # ── Визуализация ────────────────────────────────────────────────────────
    add_heading(doc, "10. Визуализация данных (диаграммы)", level=1)
    add_para(
        doc,
        "Для наглядного представления результатов OLAP-анализа в приложении "
        "реализованы диаграммы (компонент OlapChart). Они позволяют сравнить "
        "план и факт по отделам и статьям, оценить структуру расходов и "
        "динамику по кварталам.",
    )
    add_screenshot_note(
        doc,
        caption="Диаграмма «План vs Факт по отделам»",
        what_to_capture="В OLAP-разделе переключитесь в режим диаграммы для roll-up по отделам и сделайте скриншот столбчатой (или круговой) диаграммы.",
    )
    add_screenshot_note(
        doc,
        caption="Диаграмма «Динамика по кварталам»",
        what_to_capture="Скриншот диаграммы по кварталам, где видна динамика плана/факта во времени.",
    )

    # ── Экспорт ─────────────────────────────────────────────────────────────
    add_heading(doc, "11. Экспорт отчётов", level=1)
    add_para(
        doc,
        "Для всех аналитических отчётов предусмотрен экспорт в форматы CSV "
        "и XLSX. Выгрузка выполняется на стороне сервера (модуль export.py): "
        "SQL-запрос формирует строки с русскоязычными заголовками столбцов, "
        "затем они сериализуются в нужный формат (openpyxl для XLSX, "
        "встроенная библиотека csv для CSV) и отдаются клиенту через "
        "StreamingResponse с заголовком Content-Disposition.",
    )
    add_screenshot_note(
        doc,
        caption="Кнопки экспорта отчёта",
        what_to_capture="В разделе OLAP сделайте скриншот панели с кнопками «Экспорт CSV» / «Экспорт XLSX».",
    )
    add_screenshot_note(
        doc,
        caption="Выгруженный XLSX-файл",
        what_to_capture="Откройте выгруженный файл (например, rollup-by-dept.xlsx) в MS Excel и сделайте скриншот содержимого со всеми столбцами и заголовками на русском языке.",
    )
    add_screenshot_note(
        doc,
        caption="Выгруженный CSV-файл",
        what_to_capture="Откройте выгруженный CSV в текстовом редакторе (или Excel) и сделайте скриншот содержимого.",
    )

    # ── Тестирование ────────────────────────────────────────────────────────
    add_heading(doc, "12. Тестирование и проверка корректности", level=1)
    add_para(
        doc,
        "Для наполнения БД использован сценарий seed_data.sql, добавляющий "
        "репрезентативный набор данных: 15 должностей, 8 типов документов, "
        "12 статей бюджета, 10 контрагентов, отделы, сотрудников, бюджетные "
        "записи и документы. Проверка корректности выполнена на следующих "
        "сценариях:",
    )
    add_bullet(doc, "создание, изменение и удаление записей во всех разделах;")
    add_bullet(doc, "соблюдение ограничений целостности — при попытке удаления справочника, на который ссылаются другие записи, сервер возвращает ошибку;")
    add_bullet(doc, "корректность агрегации: суммы roll-up совпадают с суммами детальных срезов;")
    add_bullet(doc, "корректность фильтрации dice при произвольной комбинации параметров;")
    add_bullet(doc, "корректность выгрузки: содержимое CSV/XLSX совпадает с отображаемой в интерфейсе таблицей.")

    add_screenshot_note(
        doc,
        caption="Пример валидации — ошибка при некорректных данных",
        what_to_capture="Попробуйте создать запись с некорректными данными (пустое обязательное поле, дубликат PK) и сделайте скриншот сообщения об ошибке от API или в интерфейсе.",
    )
    add_screenshot_note(
        doc,
        caption="Результат SQL-запроса в pgAdmin",
        what_to_capture="Выполните в pgAdmin запрос вида SELECT COUNT(*) FROM employee; или произвольный JOIN-запрос и сделайте скриншот результата, чтобы подтвердить соответствие данных в БД и в UI.",
    )

    # ── Выводы ──────────────────────────────────────────────────────────────
    add_heading(doc, "13. Выводы", level=1)
    add_para(
        doc,
        "В ходе выполнения лабораторной работы разработано полнофункциональное "
        "клиент-серверное приложение для работы с реляционной базой данных "
        "PostgreSQL. Реализованы все поставленные задачи:",
    )
    add_bullet(doc, "спроектирована схема БД из восьми взаимосвязанных таблиц, отражающая предметную область документооборота и бюджетирования;")
    add_bullet(doc, "реализован REST API на FastAPI с полным набором CRUD-операций для каждой сущности;")
    add_bullet(doc, "разработан клиент на Vue 3 с удобным интерфейсом: таблицы с поиском и сортировкой, модальные формы ввода, навигация;")
    add_bullet(doc, "реализованы OLAP-операции (roll-up, slice, dice, drill-down, cross-tab) с использованием агрегирующих SQL-запросов;")
    add_bullet(doc, "добавлена визуализация аналитических данных в виде диаграмм;")
    add_bullet(doc, "реализован экспорт отчётов в форматы CSV и XLSX.")
    add_para(
        doc,
        "Таким образом, цель лабораторной работы достигнута: приобретены "
        "практические навыки проектирования реляционных БД, разработки "
        "серверной и клиентской частей приложения, написания аналитических "
        "SQL-запросов для OLAP-анализа и организации экспорта данных.",
    )

    doc.save(OUT_PATH)
    print(f"Saved: {OUT_PATH}")


if __name__ == "__main__":
    build()

```
