from datetime import timedelta

import pendulum

from airflow.sdk import dag, get_current_context, task
from airflow.timetabels.interval import CronDataIntervalTimetable

@dag(
    dag_id="airflow_operations_dag",

    # 毎日 02:00 JST
    schedule=CronDataIntervalTimetable(
        "0 2 * * *",
        timezone="Asia/Tokyo",
    ),

    start_date=pendulum.datetime(
        2026,
        8,
        20,
        tz="Asia/Tokyo",
    ),

    # start_dateから現在までを自動で大量実行しない
    catchup=False,

    # 同じDAGを同時に複数実行しない
    max_active_runs=1,

    # DAG全体が10分を超えたら異常とみなす
    dagrun_timeout=timedelta(minutes=10),

    tags=[
        "data-engineering-study",
        "operations",
    ],
)
def airflow_operations():

    @task(
        # 一時的な障害なら最大2回再試行
        retries=2,
        retry_delay=timedelta(seconds=10),
    )
    def process_interval():
        context = get_current_context()

        data_interval_start = context["data_interval_start"]
        data_interval_end = context["data_interval_end"]

        ti = context["ti"]

        print("Processing data interval")
        print(f"start      = {data_interval_start}")
        print(f"end        = {data_interval_end}")
        print(f"logical    = {context['logical_date']}")
        print(f"try_number = {ti.try_number}")

        return {
            "start": data_interval_start.isoformat(),
            "end": data_interval_end.isoformat(),
        }

    @task(
        # Validation失敗は再試行しても直らない可能性が高いため
        # このTaskではRetryしない
        retries=0,
    )
    def validate_interval(interval):
        start = pendulum.parse(interval["start"])
        end = pendulum.parse(interval["end"])

        if start >= end:
            raise ValueError(
                "data_interval_start must be earlier "
                "than data_interval_end"
            )

        print("Validation succeeded.")
        print(f"start = {start}")
        print(f"end   = {end}")

    interval = process_interval()
    validate_interval(interval)

airflow_operations()
