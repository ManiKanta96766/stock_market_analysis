from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, lag, avg, stddev, when, row_number, lit
)
from pyspark.sql.window import Window
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator
import time

def main():
    # ==========================
    # 1. START SPARK SESSION
    # ==========================
    spark = SparkSession.builder \
        .appName("Stock Market Analysis") \
        .master("local[*]") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .config("spark.sql.shuffle.partitions", "10") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")  # Reduce verbosity
    start_time = time.time()

    print("\n=== STOCK MARKET ANALYSIS PIPELINE ===\n")

    # ==========================
    # 2. LOAD AND PREPARE DATA
    # ==========================
    csv_path = "file:///C:/Users/MANIKANTA/OneDrive/Desktop/stock_market_analysis/spark-job/stocks.csv"
    df = spark.read.csv(csv_path, header=True, inferSchema=True)
    
    print(f"📊 Data loaded: {df.count()} rows, {len(df.columns)} columns")

    # Rename columns
    rename_map = {
        "AAPL.Open": "Open", "AAPL.High": "High", "AAPL.Low": "Low",
        "AAPL.Close": "Close", "AAPL.Volume": "Volume", "AAPL.Adjusted": "Adjusted"
    }
    
    for old, new in rename_map.items():
        if old in df.columns:
            df = df.withColumnRenamed(old, new)

    # ==========================
    # 3. FEATURE ENGINEERING
    # ==========================
    print("\n🔧 Engineering features...")
    
    # Add partition column to avoid window warnings (group all data into one partition explicitly)
    df = df.withColumn("partition", lit(1))
    window_spec = Window.partitionBy("partition").orderBy("Date")
    
    # Basic features
    df = df.withColumn("PrevClose", lag("Close", 1).over(window_spec))
    df = df.withColumn("Return", (col("Close") - col("PrevClose")) / col("PrevClose"))
    
    # Moving averages
    df = df.withColumn("MA7", avg("Close").over(window_spec.rowsBetween(-6, 0)))
    df = df.withColumn("MA14", avg("Close").over(window_spec.rowsBetween(-13, 0)))
    
    # Volatility and additional features
    df = df.withColumn("Volatility", stddev("Return").over(window_spec.rowsBetween(-13, 0)))
    df = df.withColumn("PriceRange", col("High") - col("Low"))
    df = df.withColumn("Direction", when(col("Return") > 0, 1).otherwise(0))
    
    # Remove nulls and cache for performance
    df = df.na.drop().cache()
    print(f"✅ Features engineered: {df.count()} clean rows")

    # ==========================
    # 4. MACHINE LEARNING
    # ==========================
    print("\n🤖 Training machine learning model...")
    
    feature_cols = ["Open", "High", "Low", "Volume", "PriceRange", 
                   "PrevClose", "MA7", "MA14", "Return", "Volatility"]
    
    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
    lr = LinearRegression(featuresCol="features", labelCol="Close", 
                         regParam=0.01, elasticNetParam=0.8)
    
    pipeline = Pipeline(stages=[assembler, lr])
    model = pipeline.fit(df)
    
    # ==========================
    # 5. PREDICTIONS & EVALUATION
    # ==========================
    predictions = model.transform(df)
    
    evaluator = RegressionEvaluator(labelCol="Close", predictionCol="prediction", metricName="rmse")
    rmse = evaluator.evaluate(predictions)
    
    lr_model = model.stages[-1]
    r2 = lr_model.summary.r2
    
    # ==========================
    # 6. RESULTS SUMMARY
    # ==========================
    print("\n" + "="*50)
    print("📈 FINAL RESULTS SUMMARY")
    print("="*50)
    print(f"📍 Dataset: {predictions.count()} trading days")
    print(f"🎯 Model RMSE: ${rmse:.4f}")
    print(f"📊 Model R²: {r2:.4f}")
    print(f"⏱️  Execution time: {time.time() - start_time:.2f} seconds")
    print("="*50)
    
    # Show sample predictions
    print("\n🔍 Sample Predictions (First 10 days):")
    predictions.select("Date", "Close", "prediction", "Return", "Direction") \
              .orderBy("Date") \
              .show(10, truncate=False)
    
    # Show performance metrics
    print("📋 Performance Metrics:")
    predictions.select("Close", "prediction", "Return") \
              .describe() \
              .show()

    # ==========================
    # 7. TRADING INSIGHTS
    # ==========================
    print("\n💡 TRADING INSIGHTS:")
    total_days = predictions.count()
    up_days = predictions.filter(col("Direction") == 1).count()
    down_days = predictions.filter(col("Direction") == 0).count()
    
    print(f"📅 Up days: {up_days} ({up_days/total_days*100:.1f}%)")
    print(f"📅 Down days: {down_days} ({down_days/total_days*100:.1f}%)")
    print(f"📈 Average daily return: {predictions.agg(avg('Return')).collect()[0][0]*100:.3f}%")
    
    spark.stop()
    print("\n✅ Pipeline completed successfully!")

if __name__ == "__main__":
    main()