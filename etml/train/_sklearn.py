from mlflow import tracking
from airflow.models import BaseOperator
from kafka import KafkaConsumer


class BaseTrainer(BaseOperator):
    __name__="BaseTrainer"
    def __init__(self):
        self.mlflow=mlflow.tracking
    def readFromKafka(self,**kwargs):
        return
    def writeToKafka(self,**kwargs):
        return
    def execute(self,**kwargs):
        return
    def saveModel(self,**kwargs):
        return

class BasePredictor(BaseOperator):
    pass

