try:
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.getOrCreate()
except Exception as e:
    print("Failed to create SparkSession, trying DatabricksSession")
    from databricks.connect import DatabricksSession
    from databricks.sdk.core import Config

    config = Config(profile="aws-e2-demo")
    spark = DatabricksSession.builder.sdkConfig(config).getOrCreate()
