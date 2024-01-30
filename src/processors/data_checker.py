import logging
from pandas import DataFrame


logger = logging.getLogger("app")


class DataChecker:

    def __init__(self, table: str):
        self.table = table
        self.rows_failed = 0

    def check(self, raw_data: DataFrame, schema: dict) -> DataFrame:
        logger.info("check")
        no_duplicates = raw_data.dropna(how="any").drop_duplicates()
        self.rows_failed = len(raw_data) - len(no_duplicates)
        checked = no_duplicates.astype(schema).reset_index(drop=True)
        return checked
