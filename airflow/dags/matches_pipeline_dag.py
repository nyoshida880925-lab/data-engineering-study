import boto3
import pendulum

from airflow.providers.amazon.aws.operators.athena import AthenaOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.sdk import dag, task

AWS_REGION = "ap-northeast-1"
BUCKET = "data-engineering-study-nyoshida880925-2026"
DATABASE = "data_engineering_study"
SEASON = "2024"

SOURCE_KEY = (
    f"processed/python-pipeline/matches/"
    f"season={SEASON}/matches.parquet"
)

SUMMARY_ROOT = (
    f"s3://{BUCKET}/"
    f"processed/glue-job/matches-summary"
)

ATHENA_RESULTS = f"s3://{BUCKET}/athena-results/"

@dag(
    dag_id="matches_pipeline_dag",
    schedule=None,
    start_date=pendulum.datetime(
        2026,
        1,
        1,
        tz="Asia/Tokyo",
    ),
    catchup=False,
    tags=[
        "data-engineering-study",
        "aws",
        "s3",
        "glue",
        "athena",
    ],
)
def matches_pipeline():

    wait_for_source = S3KeySensor(
        task_id="wait_for_source",
        bucket_name=BUCKET,
        bucket_key=SOURCE_KEY,
        aws_conn_id=None,
        region_name=AWS_REGION,
        poke_interval=10,
        timeout=60,
    )

    run_glue_job = GlueJobOperator(
        task_id="run_matches_summary_glue_job",
        job_name="matches-summary-job",
        script_location=(
            f"s3://{BUCKET}/scripts/glue/matches_summary.py"
        ),
        iam_role_name=(
            "AWSGlueServiceRole-data-engineering-study"
        ),
        script_args={
            "--SOURCE_DATABASE": DATABASE,
            "--SOURCE_TABLE": "matches",
            "--SEASON": SEASON,
            "--OUTPUT_PATH": SUMMARY_ROOT,
        },
        aws_conn_id=None,
        region_name=AWS_REGION,
        wait_for_completion=True,
        update_config=False,
        stop_job_run_on_kill=True,
    )

    create_summary_table = AthenaOperator(
        task_id="create_summary_table",
        query=f"""
            CREATE EXTERNAL TABLE IF NOT EXISTS matches_summary (
                home_team string,
                home_matches bigint,
                home_goals bigint
            )
            PARTITIONED BY (
                season string
            )
            STORED AS PARQUET
            LOCATION '{SUMMARY_ROOT}/'
        """,
        database=DATABASE,
        output_location=ATHENA_RESULTS,
        workgroup="primary",
        aws_conn_id=None,
        region_name=AWS_REGION,
    )

    register_partition = AthenaOperator(
        task_id="register_partition",
        query=f"""
            ALTER TABLE matches_summary
            ADD IF NOT EXISTS
            PARTITION (
                season='{SEASON}'
            )
            LOCATION '{SUMMARY_ROOT}/season={SEASON}/'
        """,
        database=DATABASE,
        output_location=ATHENA_RESULTS,
        workgroup="primary",
        aws_conn_id=None,
        region_name=AWS_REGION,
    )

    validate_summary = AthenaOperator(
        task_id="validate_summary",
        query=f"""
            SELECT
                COUNT(*) AS team_count,
                SUM(home_matches) AS home_matches,
                SUM(home_goals) AS home_goals
            FROM matches_summary
            WHERE season = '{SEASON}'
        """,
        database=DATABASE,
        output_location=ATHENA_RESULTS,
        workgroup="primary",
        aws_conn_id=None,
        region_name=AWS_REGION,
    )

    @task
    def check_validation_result(
        query_execution_id: str,
    ):
        athena = boto3.client(
            "athena",
            region_name=AWS_REGION,
        )

        response = athena.get_query_results(
            QueryExecutionId=query_execution_id,
        )

        rows = response["ResultSet"]["Rows"]

        header = [
            value.get("VarCharValue", "")
            for value in rows[0]["Data"]
        ]

        values = [
            value.get("VarCharValue", "")
            for value in rows[1]["Data"]
        ]

        result = dict(zip(header, values))

        print("Athena validation result:")
        print(result)

        team_count = int(result["team_count"])
        home_matches = int(result["home_matches"])
        home_goals = int(result["home_goals"])

        if team_count <= 0:
            raise ValueError(
                "team_count must be greater than 0"
            )

        if home_matches <= 0:
            raise ValueError(
                "home_matches must be greater than 0"
            )

        print("Validation succeeded.")
        print(f"team_count   = {team_count}")
        print(f"home_matches = {home_matches}")
        print(f"home_goals   = {home_goals}")

        return result

    wait_for_source >> run_glue_job
    run_glue_job >> create_summary_table
    create_summary_table >> register_partition
    register_partition >> validate_summary

    check_validation_result(
        validate_summary.output
    )

matches_pipeline()
