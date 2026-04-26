### `backend/database.py`

```python
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

### `backend/main.py`

```python
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

### `backend/models.py`

```python
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

### `backend/routers/__init__.py`

```python

```

### `backend/routers/budget.py`

```python
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

### `backend/routers/budget_item.py`

```python
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

### `backend/routers/contractor.py`

```python
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

### `backend/routers/department.py`

```python
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

### `backend/routers/doc_type.py`

```python
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

### `backend/routers/document.py`

```python
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

### `backend/routers/employee.py`

```python
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

### `backend/routers/export.py`

```python
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

### `backend/routers/olap.py`

```python
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

### `backend/routers/position.py`

```python
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

### `frontend/index.html`

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

### `frontend/postcss.config.js`

```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### `frontend/src/App.vue`

```vue
<script setup>
</script>

<template>
  <RouterView />
</template>
```

### `frontend/src/components/AppLayout.vue`

```vue
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

### `frontend/src/components/DataTable.vue`

```vue
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

### `frontend/src/components/FormModal.vue`

```vue
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

### `frontend/src/components/Sidebar.vue`

```vue
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

### `frontend/src/main.js`

```javascript
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'

createApp(App).use(router).mount('#app')
```

### `frontend/src/router/index.js`

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'
import Dashboard from '../views/Dashboard.vue'
import Employees from '../views/Employees.vue'
import Departments from '../views/Departments.vue'
import Documents from '../views/Documents.vue'
import Budget from '../views/Budget.vue'
import Contractors from '../views/Contractors.vue'
import Positions from '../views/Positions.vue'
import Olap from '../views/Olap.vue'

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

### `frontend/src/services/api.js`

```javascript
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

### `frontend/src/style.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### `frontend/src/views/Budget.vue`

```vue
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

### `frontend/src/views/Contractors.vue`

```vue
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

### `frontend/src/views/Dashboard.vue`

```vue
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

### `frontend/src/views/Departments.vue`

```vue
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

### `frontend/src/views/Documents.vue`

```vue
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

### `frontend/src/views/Employees.vue`

```vue
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

### `frontend/src/views/Olap.vue`

```vue
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

### `frontend/src/views/Positions.vue`

```vue
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

### `frontend/tailwind.config.js`

```javascript
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

### `frontend/vite.config.js`

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
})
```
