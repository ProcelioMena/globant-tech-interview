from google.cloud.bigquery import SchemaField, enums


BQ_TYPES = enums.SqlTypeNames

table_data = {
    "jobs": {
        "pd_schema": {"id": "int64", "job": "object"},
        "columns": ["id", "job"]
    },
    "departments": {
        "pd_schema": {"id": "int64", "department": "object"},
        "columns": ["id", "department"]
    },
    "hired_employees": {
        "pd_schema": {"id": "int64", "name": "object", "datetime": "object", "job_id": "int64",
                          "department_id": "int64"},
        "columns": ["id", "name", "datetime", "job_id", "department_id"]
    }
}
