import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import functions as F

args = getResolvedOptions(
    sys.argv,
    [
        "JOB_NAME",
        "SOURCE_DATABASE",
        "SOURCE_TABLE",
        "SEASON",
        "OUTPUT_PATH",
    ],
)

sc = SparkContext.getOrCreate()
glue_context = GlueContext(sc)

job = Job(glue_context)
job.init(args["JOB_NAME"], args)

season = args["SEASON"]

matches = glue_context.create_dynamic_frame.from_catalog(
    database=args["SOURCE_DATABASE"],
    table_name=args["SOURCE_TABLE"],
    push_down_predicate=f"season == '{season}'",
    transformation_ctx="matches",
)

matches_df = matches.toDF()

summary_df = (
    matches_df
    .groupBy("home_team")
    .agg(
        F.count("*").alias("home_matches"),
        F.sum("home_goals").alias("home_goals"),
    )
)

output_path = (
    f"{args['OUTPUT_PATH'].rstrip('/')}"
    f"/season={season}/"
)

summary_df.write \
    .mode("overwrite") \
    .parquet(output_path)

print(f"Output: {output_path}")
print(f"Teams: {summary_df.count()}")

job.commit()