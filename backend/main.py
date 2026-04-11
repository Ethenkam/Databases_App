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
