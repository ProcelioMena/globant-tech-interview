from google.cloud import storage
from io import BytesIO
from pandas import DataFrame, read_csv
from typing import Optional, Union

from typing import List


class StorageHandler():
    """
    Class for handling storage of data in gcs
    """

    def __init__(self, table: str):
        """
        Constructor for StorageHandler
        :param table: table to handle
        """
        self.table = table
        self.client = storage.Client()
        self.bucket_name = "globant-tech-interview"
        self.raw_prefix = "raw/"

    def get_csv(self, table: str, columns: List[str]) -> Union[Optional[DataFrame], str]:
        """
        Get csv from given table
        :param table: table to load
        :return: data
        """
        blobs = list(self.client.list_blobs(self.bucket_name, prefix=f"{self.raw_prefix}{table}/"))
        if len(blobs) <= 1:
            return None, f"No file found in the raw folder for table {table}"
        else:
            blob = blobs[-1]
            data = blob.download_as_string()
            raw_table = read_csv(BytesIO(data), names=columns, header=None)
            return raw_table, None

