from fastapi import FastAPI, APIRouter
from logging import Logger
from pathlib import Path

from processors.data_processor import DataProcessor

router = APIRouter()
logger = Logger("app")


@router.get("/", status_code=200)
def root() -> dict:
    logger.info("root")
    return {"Globant Service": "Globant service is up and running"}


@router.get("/process", status_code=200)
def process(table: str) -> dict:
    logger.info("processing data")
    operation_summary = DataProcessor(table).process()
    return {"rows_inserted": operation_summary["rows_inserted"], "rows_failed": operation_summary["rows_failed"],
            "errors": operation_summary["errors"]}


app = FastAPI(title="Globant service", openapi_url="/openapi.json")
app.include_router(router)

logger.info("Globant API successfully booted...")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(f"{Path(__file__).stem}:app", host="0.0.0.0", port=8080, reload=True, log_level="info",
                reload_dirs="/app/")