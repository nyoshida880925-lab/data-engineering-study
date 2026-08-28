from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("data-engineering-study")
    .master("local[*]")
    .getOrCreate()
)

data = [
    ("Hokkaido Consadole Sapporo", 3),
    ("Vegalta Sendai", 1),
]

df = spark.createDataFrame(
    data,
    ["team", "points"]
)

df.show()

spark.stop()
