from pyspark.sql import SparkSession

 
lista = ["com.amazonaws:aws-java-sdk-s3control:1.11.534"
,"com.amazonaws:aws-java-sdk-core:1.11.534"
,"com.amazonaws:aws-java-sdk-dynamodb:1.11.534"
,"com.amazonaws:aws-java-sdk-kms:1.11.534"
,"com.amazonaws:aws-java-sdk-s3:1.11.534"
,"io.delta:delta-core_2.12:1.0.0"
,"org.apache.hadoop:hadoop-aws:3.1.2"
,"net.snowflake:snowflake-ingest-sdk:1.0.2-beta.4"
,"net.snowflake:snowflake-jdbc:3.13.22"
,"net.snowflake:spark-snowflake_2.12:2.11.0-spark_3.1"]

concat = ','.join(lista)

def localjars():
    spark = (
        SparkSession
            .builder
            .appName("multiJars")
            .config("spark.jars.packages", concat)
            .getOrCreate()
        )
    return spark