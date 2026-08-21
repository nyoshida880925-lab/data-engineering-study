import pendulum

from airflow.sdk import dag, task

@dag(
    dag_id="matches_etl_dag",
    schedule=None,
    start_date=pendulum.datetime(2026, 1, 1, tz="Asia/Tokyo"),
    catchup=False,
    tags=["data-engineering-study"],
)
def matches_etl():
    @task
    def extract():
        print("Extract: match data")

        return [
            {
                "match_id": 1,
                "home_team": "Sapporo",
                "home_goals": 3,
            },
            {
                "match_id": 2,
                "home_team": "Kofu",
                "home_goals": 2,
            },
            {
                "match_id": 3,
                "home_team": "Sapporo",
                "home_goals": 1,
            },
        ]

    @task
    def transform(matches):
        print("Transform: aggregate home goals")

        summary = {}

        for match in matches:
            team = match["home_team"]
            goals = match["home_goals"]

            summary[team] = summary.get(team, 0) + goals

        return summary

    @task
    def load(summary):
        print("Load: transformed result")

        for team, goals in summary.items():
            print(f"{team}: {goals}")

    extracted = extract()
    transformed = transform(extracted)

    load(transformed)

matches_etl()
