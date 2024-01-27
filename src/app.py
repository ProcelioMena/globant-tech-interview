from fastapi import FastAPI, APIRouter
from logging import Logger
from pathlib import Path

router = APIRouter()

logger = Logger("app")


@router.get("/", status_code=200)
def root() -> dict:
    logger.info("root")
    return {"Globant Service": "Globant service is up and running"}


app = FastAPI(title="Globant service", openapi_url="/openapi.json")
app.include_router(router)

logger.info("Globant API successfully booted...")

print(Path(__file__).stem)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(f"{Path(__file__).stem}:app", host="0.0.0.0", port=8080, reload=True, log_level="info",
                reload_dirs="/app/")
