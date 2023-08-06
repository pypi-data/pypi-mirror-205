from datetime import datetime
from dateutil.relativedelta import relativedelta
from minirony.data_transfer import AWSCredentials
from pyspark.sql.functions import date_format
from pyspark.sql import SparkSession, functions
from pyspark import SparkConf
import os
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Attr
from dateutil.relativedelta import relativedelta


class DirectoryManager:
    def get_current_directory():
        return os.path.dirname(os.path.abspath(__file__))


class EnvironmentManager:
    DEV = "DEV"
    PROD = "PROD"

    def __init__(self):
        self.__create_aws_credentials()

    def get_jar_files(self):
        jars_files = [
            "com.amazonaws:aws-java-sdk-s3control:1.11.534",
            "com.amazonaws:aws-java-sdk-core:1.11.534",
            "com.amazonaws:aws-java-sdk-dynamodb:1.11.534",
            "com.amazonaws:aws-java-sdk-kms:1.11.534",
            "com.amazonaws:aws-java-sdk-s3:1.11.534",
            "io.delta:delta-core_2.12:1.0.0",
            "org.apache.hadoop:hadoop-aws:3.1.2",
            "net.snowflake:snowflake-ingest-sdk:1.0.2-beta.4",
            "net.snowflake:snowflake-jdbc:3.13.22",
            "net.snowflake:spark-snowflake_2.12:2.11.0-spark_3.1",
        ]
        jars = ",".join(jars_files)
        return jars

    def get_checkpoint_bucket(self):
        return os.getenv("CHECKPOINT_BUCKET")

    def get_landingzone_bucket(self):
        return os.getenv("LANDING_ZONE_BUCKET")

    def get_bronze_bucket(self):
        return os.getenv("BRONZE_BUCKET")

    def get_silver_bucket(self):
        return os.getenv("SILVER_BUCKET")

    def get_entity(self):
        return os.getenv("ENTITY")

    def get_window_id_key(self):
        return os.getenv("WINDOW_ID_KEY")

    def get_equal_condition(self):
        return os.getenv("EQUAL_CONDITION")

    def get_partition_by(self):
        return os.getenv("PARTITION_BY", "")

    def get_date_partition_by(self):
        return os.getenv("DATE_PARTITION_BY", "")

    def get_schema(self):
        return os.getenv("SCHEMA")

    def get_drop_columns(self):
        return os.getenv("DROP_COLUMNS")

    def get_enviroment(self):
        return os.getenv("KINDENVIRONMENT", EnvironmentManager.DEV)

    def get_client(self):
        return os.getenv("CLIENT", "A3Data")

    def get_dynamo_table(self):
        return os.getenv("DYNAMO_LOGFEP_TABLE")

    def get_dynamo_key(self):
        return os.getenv("DYNAMO_LOGFEP_KEY")

    def get_aws_credentials(self):
        return self.__aws_credentials

    def get_job_type(self):
        return os.getenv("JOB_TYPE")

    def __create_aws_credentials(self):
        boto_session = boto3.Session(profile_name=os.getenv("AWS_PROFILE"))
        boto_aws_credentials = boto_session.get_credentials()
        self.__aws_credentials = AWSCredentials(
            boto_aws_credentials.access_key,
            boto_aws_credentials.secret_key,
            boto_aws_credentials.token,
        )

    def get_job_type(self):
        return os.getenv("JOB_TYPE")


class SparkManager:
    def get_session(self, app_name, s3a_protocol):
        spark_config = self.create_config(s3a_protocol)
        spark_builder = SparkSession.builder.appName(app_name).config(conf=spark_config)
        return spark_builder.getOrCreate()

    def create_config(self, s3a_protocol):
        spark_config = SparkConf()
        spark_config.set("spark.hadoop.fs.s3a.aws.credentials.provider", s3a_protocol)
        spark_config.set("spark.shuffle.service.enabled", "false")
        spark_config.set("spark.dynamicAllocation.enabled", "false")
        spark_config.set("spark.sql.debug.maxToStringFields", 100000)
        spark_config.set(
            "spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension"
        )
        spark_config.set("spark.sql.legacy.parquet.int96RebaseModeInRead", "CORRECTED")
        spark_config.set("spark.sql.legacy.parquet.int96RebaseModeInWrite", "CORRECTED")
        spark_config.set(
            "spark.sql.legacy.parquet.datetimeRebaseModeInRead", "CORRECTED"
        )
        spark_config.set(
            "spark.sql.legacy.parquet.datetimeRebaseModeInWrite", "CORRECTED"
        )
        spark_config.set("spark.driver.memory", "6g")
        spark_config.set("spark.sql.shuffle.partitions", "100")
        spark_config.set("spark.default.parallelism", "100")
        return spark_config


class SparkDevManager(SparkManager):
    def __init__(self, jars, aws_credentials, s3a_protocol):
        self.s3a_protocol = s3a_protocol
        self.__spark_session = None
        self.jars = jars
        self.aws_credentials = aws_credentials

    def get_session(self, app_name):
        spark_config = self.create_config(self.s3a_protocol)
        spark_config.set("spark.jars.packages", self.jars)
        spark_builder = SparkSession.builder.appName(app_name).config(conf=spark_config)
        self.__spark_session = spark_builder.getOrCreate()

        self.__spark_session.sparkContext.setLogLevel("ERROR")

        self.__set_credentials()

        return self.__spark_session

    def __set_credentials(self):
        hadoop_configuration = self.__spark_session._jsc.hadoopConfiguration()
        hadoop_configuration.set("fs.s3a.access.key", self.aws_credentials.access_key)
        hadoop_configuration.set("fs.s3a.secret.key", self.aws_credentials.secret_key)
        hadoop_configuration.set("fs.s3a.session.token", self.aws_credentials.token)


class SparkProdManager(SparkManager):
    def __init__(self, s3a_protocol):
        self.s3a_protocol = s3a_protocol
        self.__spark_session = None

    def get_session(self, app_name):
        self.__spark_session = super().get_session(app_name, self.s3a_protocol)

        # self.__spark_session.sparkContext.setLogLevel("ERROR")

        return self.__spark_session


class BucketManager:
    def __init__(
        self,
        checkpoint_bucket,
        landingzone_bucket,
        bronze_bucket,
        silver_bucket,
    ):
        self.checkpoint_bucket = checkpoint_bucket
        self.landingzone_bucket = landingzone_bucket
        self.bronze_bucket = bronze_bucket
        self.silver_bucket = silver_bucket


class ProcessingManager:
    WITHOUT_PARTITION = "WITHOUT"

    def adapt_partition(df, date_partition=None, partition=None):
        if date_partition == "" and partition == "":
            return (df, ProcessingManager.WITHOUT_PARTITION)

        if date_partition == "":
            return (df, partition)

        date_columns_df = (
            df.withColumn("Ano", date_format(date_partition, "y"))
            .withColumn("Mes", date_format(date_partition, "MM"))
            .withColumn("Dia", date_format(date_partition, "dd"))
        )

        return (date_columns_df, ["Ano", "Mes", "Dia"])


class BotoManager:
    @staticmethod
    def get_dynamodb():
        return boto3.resource("dynamodb", region_name="us-east-2")


class DynamoDbManager:
    def __init__(self, dynamodb):
        self.dynamodb = dynamodb

    def find_item(self, table_name, field, value):
        table = self.dynamodb.Table(table_name)
        result = table.get_item(Key={field: value})
        result_field = "Item"
        if result_field not in result:
            return 0
        return result[result_field]

    def update_item(self, table_name, key, attributes):
        table = self.dynamodb.Table(table_name)
        result = table.put_item(Item=attributes)
        return result

    def scan(self, table_name):
        table = self.dynamodb.Table(table_name)
        result = table.scan(
            FilterExpression=Attr("DWSchema").exists(),
            ProjectionExpression="CodigoTransacao, DWSchema",
        )

        response = result["Items"]
        while "LastEvaluatedKey" in result:
            result = table.scan(
                FilterExpression=Attr("DWSchema").exists(),
                ProjectionExpression="CodigoTransacao, DWSchema",
                ExclusiveStartKey=result["LastEvaluatedKey"],
            )
            response.extend(result["Items"])

        return response


environment_manager = EnvironmentManager()


class DatetimeManager(object):
    __RECORRENTE = "RECORRENTE"
    __DIARIO = "DIARIO"
    __MENSAL = "MENSAL"

    def __init__(self) -> None:
        self.job_type = environment_manager.get_job_type()

        today = datetime.now()
        today_utm = today + relativedelta(hours=-3)
        first_day_month = today_utm.replace(day=1)

        if self.job_type == DatetimeManager.__RECORRENTE:
            self.initial_date = today_utm
            self.end_date = today_utm
            self.base_date_client = first_day_month

        elif self.job_type == DatetimeManager.__DIARIO:
            self.initial_date = first_day_month
            self.end_date = today_utm
            self.base_date_client = first_day_month

        elif self.job_type == DatetimeManager.__MENSAL:
            previous_month_date = today + relativedelta(months=-1, hours=-3)
            previous_beginning_date = previous_month_date.replace(day=1)
            last_day_month = previous_beginning_date + relativedelta(day=31)
            self.initial_date = previous_beginning_date
            self.end_date = last_day_month
            self.base_date_client = previous_beginning_date

        print(self.initial_date)
        print(self.end_date)
        print(self.base_date_client)

    def get_cdc_date():
        datetime_str = "16/08/22 09:00:00"
        datetime_value = datetime.strptime(datetime_str, "%d/%m/%y %H:%M:%S")
        return functions.lit(datetime_value)
