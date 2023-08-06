from minirony.manager import *

environment_manager = EnvironmentManager()


class SparkManagerFactory:
    __PROD_CREDENTIAL = "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider"
    __DEV_CREDENTIAL = "org.apache.hadoop.fs.s3a.TemporaryAWSCredentialsProvider"

    def get_spark_manager() -> SparkManager():
        if environment_manager.get_enviroment() == environment_manager.PROD:
            return SparkProdManager(SparkManagerFactory.__PROD_CREDENTIAL)
        else:
            jars = environment_manager.get_jar_files()
            aws_credentials = environment_manager.get_aws_credentials()
            return SparkDevManager(
                jars,
                aws_credentials,
                SparkManagerFactory.__DEV_CREDENTIAL,
            )

    def get_spark_app_name(step: str, entity: str):
        return f"{entity.lower()}-{environment_manager.get_enviroment().lower()}-{step}-spark-{environment_manager.get_client()}"


class BucketManagerFactory:
    def __init__(self):
        self.bucket_manager = None

    def get_bucket_manager(self):
        self.bucket_manager = BucketManager(
            environment_manager.get_checkpoint_bucket(),
            environment_manager.get_landingzone_bucket(),
            environment_manager.get_bronze_bucket(),
            environment_manager.get_silver_bucket(),
        )
        return self.bucket_manager
