import pendulum

from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.sdk import dag, task

@dag(
    dag_id="matches_glue_dag",
    schedule=None,
    start_date=pendulum.datetime(2026, 1, 1, tz="Asia/Tokyo"),
    catchup=False,
    tags=["data-engineering-study", "aws", "glue"],
)
def matches_glue():
    run_glue_job = GlueJobOperator(
        task_id="run_matches_summary_glue_job",

        job_name="matches-summary-job",

        script_location=(
            "s3://data-engineering-study-nyoshida880925-2026/"
            "scripts/glue/matches_summary.py"
        ),

        iam_role_name="AWSGlueServiceRole-data-engineering-study",

        script_args={
            "--SOURCE_DATABASE": "data_engineering_study",
            "--SOURCE_TABLE": "matches",
            "--SEASON": "2025",
            "--OUTPUT_PATH": (
                "s3://data-engineering-study-nyoshida880925-2026/"
                "processed/glue-job/matches-summary"
            ),
        },

        aws_conn_id=None,
        region_name="ap-northeast-1",

        wait_for_completion=True,
        update_config=False,
        stop_job_run_on_kill=True,
    )

    @task
    def report_completion(glue_job_run_id: str):
        print("Glue Job completed.")
        print(f"Glue Job Run ID: {glue_job_run_id}")

    report_completion(run_glue_job.output)

matches_glue()
