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
