from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("SimpleWSLJob") \
    .master("spark://localhost:7077") \
    .getOrCreate()

df = spark.read.csv("/home/mani/data/sample.csv", header=True, inferSchema=True)
df.show()

spark.stop()
