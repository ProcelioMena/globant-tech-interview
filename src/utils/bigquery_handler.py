import logging
from google.cloud import bigquery, storage
from pandas import DataFrame

from utils.query_mixin import QueryMixin


logger = logging.getLogger("app")


class TableHandler():
    """
    Class to handle the data flow for a table
    """

    def __init__(self, table: str):
        """
        Constructor for StorageHandler
        :param table: table to handle
        """
        self.table = table
        self.client = bigquery.Client()
        self.dataset_id = "jobs_insights"
        self.bucket = "globant-tech-interview"
        self.table_id = f"globant-tech-interview.{self.dataset_id}.{self.table}"

    def load_table(self, data: DataFrame) -> int:
        """
        Load table into bigquery
        :param data: data to load
        :param schema: schema of the data
        :return: None
        """
        logger.info(f"loading table {self.table}")
        print(data.dtypes)
        job = self.client.load_table_from_dataframe(data, self.table_id)
        job.result()
        return job.output_rows

    def backup_table(self):
        """
        Backup table to gcs using ExtractJobConfig with avro format.
        """
        logger.info(f"backing up table {self.table}")
        destination_uri = f"gs://{self.bucket}/backup/{self.table}/{self.table}.avro"
        extract_job = self.client.extract_table(
            self.table_id,
            destination_uri,
            job_config=bigquery.ExtractJobConfig(
                destination_format="AVRO",
                compression="SNAPPY",
            ),
        )
        extract_job.result()

    def restore(self) -> str:
        """
        Restore table from gcs using load_table_from_uri, write_disposition="WRITE_TRUNCATE"
        :return: Message with the number of rows loaded
        """
        logger.info(f"restoring table {self.table}")
        destination_uri = f"gs://{self.bucket}/backup/{self.table}/{self.table}.avro"
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE",
            source_format=bigquery.SourceFormat.AVRO,
        )
        load_job = self.client.load_table_from_uri(
            destination_uri, self.table_id, job_config=job_config
        )
        load_job.result()
        destination_table = self.client.get_table(self.table_id)
        summary = f"Loaded {destination_table.num_rows} rows from {destination_uri} to {self.table_id}"
        logger.info(summary)
        return summary


class QueryHandler(QueryMixin):

    def __init__(self, query_name: str):
        """
        Constructor for QueryHandler
        :param query_name: query to execute
        """
        self.query_name = query_name
        self.client = bigquery.Client()
        self.dataset_id = "globant-tech-interview.jobs_insights"
        self.query = getattr(self, query_name)()

    def execute(self):
        """
        Execute the self.query parameter in biquery and save the result as a new table in the self.dataset_id dataset,
        the table name is the same as the query name.
        If the table already exists, write disposition is set to WRITE_TRUNCATE
        """
        logger.info(f"executing query {self.query_name}")
        job_config = bigquery.QueryJobConfig(destination=self.dataset_id + "." + self.query_name,
            write_disposition="WRITE_TRUNCATE")
        query_job = self.client.query(self.query, job_config=job_config)
        query_job.result()
        message = f"Query {self.query_name} executed successfully"
        logger.info(message)
        return message
