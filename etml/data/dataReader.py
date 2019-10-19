__author__="Gurunath"
__doc__="""

This module should read Airflow supported Databases based on hooks into pandas Dataframe (intermediate)
and transfers the data into kafka topics which will used by subsequent Operators
"""
import json
from airflow.models import BaseOperator
from airflow.models import Variable
from kafka import KafkaConsumer
from airflow.hooks.base_hook import BaseHook
import pandas as pd
from kafka import KafkaProducer

class BaseDataReader(BaseOperator):
    __name__="BaseDataReader"
    def __init__(self,airflow_hook="sqlite_default"):
        self.kafkaParams=json.loads(Variable.get("kafka_details"))
        self.hook=BaseHook.get_hook(airflow_hook)
        self.kafkaProducer=KafkaProducer(**self.kafkaParams)
    def transfer_data_from_hook_into_kafka(self,readSql=None,
                    tablename="train",topic_column="Embarked"):
        """
        Reads data from AirflowHook and publish to kafka (topics given has one of the
        column in tabular data)
        """
        conn=self.hook.get_conn()
        if readSql==None:
            readSql="select * from {}".format(tablename)
        df_iter=pd.io.sql.read_sql(readSql,conn,chunksize=10000)
        for df in df_iter:
            for _dict in df.to_dict("index").items():
                self.kafkaProducer.send(_dict[1][topic_column],_dict[1])

        return
    def execute():
        return
