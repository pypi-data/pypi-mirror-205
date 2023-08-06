from functools import reduce
from minirony.provider import SchemaProvider

schema_provider = SchemaProvider()


class ReaderDataHelper(object):
    def __init__(self, spark_session, dataframe_column_helper) -> None:
        self.spark_session = spark_session
        self.dataframe_column_helper = dataframe_column_helper

    def create_view_and_df_from_csv(self, view_name, path):
        params = {
            "inferSchema": True,
            "header": True,
            "sep": ";",
            "encoding": "UTF-8",
        }

        df = self.spark_session.read.csv(path, **params)
        df = self.dataframe_column_helper.prepare_columns(df)
        df.createOrReplaceTempView(view_name)
        return df

    def create_view_and_df_from_json(self, view_name, path):
        params = {"multiLine": True}

        df = self.spark_session.read.json(path, **params)
        df.createOrReplaceTempView(view_name)
        return df

    def create_view_and_df_from_delta(self, view_name, path):
        df = self.spark_session.read.format("delta").load(path)
        df.createOrReplaceTempView(view_name)
        return df


class DataframeColumnHelper(object):
    def __init__(self) -> None:
        self.accepted_operations = ["I", "U"]
        self.drop_columns = "header__change_seq;header__change_oper;header__change_mask;header__stream_position;header__operation;header__transaction_id;header__timestamp".split()

    def prepare_columns(self, df):
        df = self.rename_columns(df)
        if "header__change_oper" in df.columns:
            df = self.filter_and_drop_columns(df)
        return df

    def rename_columns(self, df):
        oldColumns = df.schema.names
        return reduce(
            lambda data, idx: data.withColumnRenamed(
                oldColumns[idx],
                oldColumns[idx].split(":")[0],
            ),
            range(len(oldColumns)),
            df,
        )

    def filter_and_drop_columns(self, df):
        create_option_column_df = df.withColumn("OP", df.header__change_oper)
        option_accepted_df = create_option_column_df.filter(
            create_option_column_df.OP.isin(self.accepted_operations)
        )
        return option_accepted_df.drop(*self.drop_columns)


class DataframeManipulationHelper(object):
    def __init__(self, spark_session) -> None:
        self.spark_session = spark_session

    def print_dataframe(self, df, cols=None, lines=10):
        df.printSchema()
        if cols != None:
            df = df.sort(*cols)
        print(df.count())
        print(df.show(n=lines, truncate=False))

    def create_view_and_df_from_query(self, table_name, query):
        df = self.spark_session.sql(query)
        df.createOrReplaceTempView(table_name)
        return df


class AWSS3DatasourceHelper(object):
    def __init__(self, reader_helper, sources) -> None:
        self.reader_helper = reader_helper
        self.sources = sources

    def create_all_dataframes(self):
        for source_key, source in self.sources.items():
            if source["TYPE"] == "JSON":
                self.reader_helper.create_view_and_df_from_json(
                    source_key, source["PATH"]
                )
            elif source["TYPE"] == "CSV":
                self.reader_helper.create_view_and_df_from_csv(
                    source_key, source["PATH"]
                )
            elif source["TYPE"] == "DELTA":
                self.reader_helper.create_view_and_df_from_delta(
                    source_key, source["PATH"]
                )
