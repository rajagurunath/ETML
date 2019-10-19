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
    """
    Reads data from any of the supported Airflow hooks
    into Kafka topics

    """
    __name__="BaseDataReader"
    def __init__(self,
                airflow_hook="sqlite_default",
                readSql=None,
                tablename="train",
                topic_column=None,
                *args, **kwargs):
        self.hook_name=airflow_hook
        self.readSql=readSql
        self.tablename=tablename
        self.topic_column=topic_column
        self.kafkaParams=json.loads(Variable.get("kafka_details"))
        self.hook=BaseHook.get_hook(self.hook_name)
        self.kafkaProducer=KafkaProducer(**self.kafkaParams)
        super().__init__(*args, **kwargs)
    def transfer_data_from_hook_into_kafka(self,readSql=None,
                    tablename="train",topic_column="Embarked"):
        """
        Reads data from AirflowHook and publish to kafka (topics given has one of the
        column in tabular data)
        """
        self.log.info("Getting connection from %s",self.hook_name)
        conn=self.hook.get_conn()
        if readSql==None:
            readSql="select * from {}".format(tablename)
        self.log.info('Executing: %s', self.readSql)
        df_iter=pd.io.sql.read_sql(readSql,conn,chunksize=10000)
        self.log.info("Starting kafka Producer")
        self.log.info("calculating number of rows in each topic -%s",
                                        self.topic_column)
        #vc=next(df_iter)[self.topic_column].value_counts()
        for idx,df in   enumerate(df_iter,start=1):
            if idx==1:
                vc=df[self.topic_column].value_counts()
            else:
                vc+=df[self.topic_column].value_counts()
            for _dict in df.to_dict("index").items():
                self.kafkaProducer.send(_dict[1][topic_column],_dict[1])
        finalvc=vc.to_frame()
        table=tabulate.tabulate(finalvc, headers='keys', tablefmt='psql')
        self.log.info("published kafka topic stats")
        self.log.info(table)
        return "Data published"
    def execute(self,context):

        return


class BaseDataWriter(BaseOperator):
    """
    Writes data from kafka Topics to any
    of the Airflow hooks
    """
    __name__="BaseDataReader"
    def __init__(self,airflow_hook="sqlite_default"):
        self.kafkaParams=json.loads(Variable.get("kafka_details"))
        self.hook=BaseHook.get_hook(airflow_hook)
        self.kafkaProducer=KafkaProducer(**self.kafkaParams)
    def transfer_data_kafka_into_hook(self,readSql=None,
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
