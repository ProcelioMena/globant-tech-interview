import logging
from pandas import DataFrame
from typing import Union

from processors.data_checker import DataChecker
from utils.bigquery_handler import BigQueryHandler
from utils.storage_handler import StorageHandler
from constants import table_data


logger = logging.getLogger("app")


class DataProcessor(DataChecker):
    def __init__(self, table: str):
        self.storage = StorageHandler(table)
        self.bq = BigQueryHandler(table)
        super().__init__(table)
        self.summary = {"rows_inserted": 0, "rows_failed": self.rows_failed, "errors": ""}
        self.table = table if table in table_data else None
        if not self.table:
            self.summary["errors"] = f"Table {table} not found, tables available: {list(table_data.keys())}"
        else:
            self.pd_schema = table_data[self.table]["pd_schema"]
            self.columns = table_data[self.table]["columns"]
            self.bq_schema = table_data[self.table]["bq_schema"]
            

    def process(self) -> dict:
        logger.info("processing data")
        if not self.summary["errors"]:
            logger.info("recieving data")
            raw_table, error = self.storage.get_csv(self.table, self.columns)
            if error:
                self.summary["errors"] = error
                return self.summary
            checked_data = self.check(raw_table, self.pd_schema)
            self.summary["rows_inserted"] = self.bq.load_table(checked_data, self.bq_schema)
            self.bq.backup_table()
        return self.summary
