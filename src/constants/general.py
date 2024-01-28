from google.cloud.bigquery import SchemaField, enums


BQ_TYPES = enums.SqlTypeNames

table_data = {
    "jobs": {
        "pd_schema": {"id": "int64", "job": "object"},
        "bq_schema": [SchemaField("id", BQ_TYPES.INTEGER), SchemaField("job", BQ_TYPES.STRING)],
        "columns": ["id", "job"]
    },
    "departments": {
        "pd_schema": {"id": "int64", "department": "object"},
        "bq_schema": [SchemaField("id", BQ_TYPES.INTEGER), SchemaField("department", BQ_TYPES.STRING)],
        "columns": ["id", "department"]
    },
    "hired_employees": {
        "pd_schema": {"id": "int64", "name": "object", "datetime": "datetime64", "job_id": "int64",
                          "department_id": "int64"},
        "bq_schema": [SchemaField("id", BQ_TYPES.INTEGER), SchemaField("name", BQ_TYPES.STRING),
             SchemaField("datetime", BQ_TYPES.DATETIME), SchemaField("job_id", BQ_TYPES.INTEGER)],
        "columns": ["id", "name", "datetime", "job_id", "department_id"]
    }
}
