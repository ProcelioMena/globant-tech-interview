

class QueryMixin:

    def employees_per_quarter(self) -> str:
        """
        Query to get the number of employees hired for each job and department in 2021 divided by quarters.
        Ordered alphabetically by department and job.
        """
        return """
        WITH parsed_employees AS (
            SELECT
                id,
                name,
                PARSE_DATETIME('%Y-%m-%dT%H:%M:%SZ', datetime) AS parsed_datetime,
                job_id,
                department_id
            FROM
                jobs_insights.hired_employees
            WHERE
                EXTRACT(YEAR FROM PARSE_DATETIME('%Y-%m-%dT%H:%M:%SZ', datetime)) = 2021
        )

        SELECT
            d.department,
            j.job,
            SUM(CASE WHEN EXTRACT(QUARTER FROM pe.parsed_datetime) = 1 THEN 1 ELSE 0 END) AS Q1,
            SUM(CASE WHEN EXTRACT(QUARTER FROM pe.parsed_datetime) = 2 THEN 1 ELSE 0 END) AS Q2,
            SUM(CASE WHEN EXTRACT(QUARTER FROM pe.parsed_datetime) = 3 THEN 1 ELSE 0 END) AS Q3,
            SUM(CASE WHEN EXTRACT(QUARTER FROM pe.parsed_datetime) = 4 THEN 1 ELSE 0 END) AS Q4
        FROM
            parsed_employees pe
        JOIN
            jobs_insights.jobs j ON pe.job_id = j.id
        JOIN
            jobs_insights.departments d ON pe.department_id = d.id
        GROUP BY
            d.department, j.job
        ORDER BY
            d.department, j.job;
        """


    def departments_above_mean(self) -> str:
        """
        Query to get list of ides, name and number of employees hired of each department that hired more employees than
        the mean of employees hired in 2021 for all the departments, order by the number of employees hired (desc).
        """
        return """
        WITH DepartmentHires AS (
        SELECT
            d.id AS department_id,
            d.department,
            COUNT(he.id) AS hired
        FROM
            jobs_insights.departments d
        LEFT JOIN
            jobs_insights.hired_employees he ON d.id = he.department_id
        WHERE
            EXTRACT(YEAR FROM PARSE_DATETIME('%Y-%m-%dT%H:%M:%SZ', he.datetime)) = 2021
        GROUP BY
            d.id, d.department
        ),
        MeanHires AS (
            SELECT
                AVG(hired) AS mean_hires
            FROM
                DepartmentHires
        )

        SELECT
            dh.department_id AS id,
            dh.department,
            dh.hired
        FROM
            DepartmentHires dh
        JOIN
            MeanHires mh ON dh.hired > mh.mean_hires
        ORDER BY
            dh.hired DESC;
        """
