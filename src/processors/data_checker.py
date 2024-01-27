import logging
from pandas import DataFrame


logger = logging.getLogger("app")


class DataChecker:

    def check(self, data: DataFrame) -> DataFrame:
        logger.info("check")
        return {"rows_inserted" : 1, "rows_failed": 0}
