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
