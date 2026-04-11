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
