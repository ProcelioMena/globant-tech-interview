from fastapi import FastAPI, APIRouter
from logging import Logger
from pathlib import Path
from typing import Literal

from constants import metrics
from processors.data_processor import DataProcessor
from utils.bigquery_handler import TableHandler, QueryHandler

router = APIRouter()
logger = Logger("app")


@router.get("/", status_code=200)
def root() -> dict:
    logger.info("root")
    return {"Globant Service": "Globant service is up and running"}


@router.get("/process", status_code=200)
def process(table: str) -> dict:
    logger.info("processing data")
    summary = DataProcessor(table).process()
    return {"rows_inserted": summary["rows_inserted"], "rows_failed": summary["rows_failed"],
            "errors": summary["errors"]}


@router.get("/restore", status_code=200)
def backup(table: str) -> str:
    logger.info("restor back up data")
    sumamry = TableHandler(table).restore()
    return sumamry


@router.get("/employees_per_quarter", status_code=200)
def employees_per_quarter() -> str:
    logger.info("employees_per_quarter")
    return QueryHandler("employees_per_quarter").execute()


@router.get("/departments_above_mean", status_code=200)
def departments_above_mean() -> str:
    logger.info("departments_above_mean")
    return QueryHandler("departments_above_mean").execute()


@router.get("/reports", status_code=200)
def reports(metric: Literal["employees_per_quarter", "departments_above_mean"]) -> str:
    logger.info("reports")
    return f"Reports are exposed here: {metrics[metric]}"


app = FastAPI(title="Globant service", openapi_url="/openapi.json")
app.include_router(router)

logger.info("Globant API successfully booted...")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(f"{Path(__file__).stem}:app", host="0.0.0.0", port=8080, reload=True, log_level="info",
                reload_dirs="/app/")
