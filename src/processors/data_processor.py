import logging
from pandas import DataFrame
from typing import Union

from processors.data_checker import DataChecker
from utils.storage_handler import StorageHandler


logger = logging.getLogger("app")


class DataProcessor(DataChecker):
    def __init__(self, table: str):
        self.table = table
        self.storage = StorageHandler(self.table)
        super().__init__()
        print(self.table)
        self.error_summary = {"rows_inserted": 0, "rows_failed": 0, "errors": ""}

    def process(self) -> dict:
        logger.info("recieving data")
        raw_table, error = self.storage.get_csv(self.table)
        if error:
            self.error_summary["errors"] = error
            return self.error_summary
        print(error)
        summary = self.check(data)
        return summary

    def load_backup(self) -> dict:
        logger.info(f"loading backup from {self.path}")

    def load_table(self) -> dict:
        logger.info(f"loading table from {self.path}, {self.table}")
