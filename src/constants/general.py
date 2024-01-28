from google.cloud.bigquery import enums


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

metrics = {
    "employees_per_quarter": "https://lookerstudio.google.com/reporting/585edf33-942e-422f-8355-a5d6060ac7af",
    "departments_above_mean": "https://lookerstudio.google.com/reporting/2df18dfa-f253-4f76-856e-d6daff05723f"
}
